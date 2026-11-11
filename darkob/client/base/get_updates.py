import asyncio
from typing import TYPE_CHECKING

from ...data import Data

if TYPE_CHECKING:
    import darkob

class GetUpdates:
    def _spawn_ws_update(self, coro):
        """Run one update under a concurrency ceiling.

        Every inbound WebSocket message used to create a task with no
        bound, so a busy account could spawn thousands of live tasks.
        """
        semaphore = getattr(self, "_update_semaphore", None)
        if semaphore is None:
            limit = int(getattr(self, "max_concurrent_updates", 32) or 32)
            semaphore = asyncio.Semaphore(max(1, limit))
            self._update_semaphore = semaphore

        tasks = getattr(self, "_update_tasks", None)
        if tasks is None:
            tasks = set()
            self._update_tasks = tasks

        async def _guarded():
            async with semaphore:
                await coro

        task = asyncio.create_task(_guarded())
        tasks.add(task)
        task.add_done_callback(tasks.discard)
        return task

    def _update_key(self, name: str, update: dict):
        """Identity for exactly-known messages, or None for unknown shapes.

        Avoid guessing from text alone: two people can legitimately send the
        same message in one chat. Only server-provided unique identifiers
        justify de-duplication during a reconnect recovery.
        """
        if not isinstance(update, dict):
            return None
        nested = update.get("new_message")
        sources = [update]
        if isinstance(nested, dict):
            sources.append(nested)
        for source in sources:
            for field in ("message_id", "id"):
                value = source.get(field)
                if value is not None:
                    return str(name) + ":" + str(value)
        return None

    def _record_seen_update(self, key) -> None:
        if key is None:
            return
        seen = getattr(self, "_seen_update_ids", None)
        if seen is None:
            seen = set()
            self._seen_update_ids = seen
        # Keep memory bounded on long-running bots. This is a recovery cache,
        # not the full account history, so the low-water mark is deliberate.
        if len(seen) >= 8192:
            seen.clear()
        seen.add(key)

    def _update_time(self, update: dict):
        if not isinstance(update, dict):
            return None
        nested = update.get("new_message")
        sources = [update]
        if isinstance(nested, dict):
            sources.append(nested)
        for source in sources:
            value = source.get("time")
            if value is None:
                continue
            try:
                return int(value)
            except (TypeError, ValueError):
                continue
        return None

    def _advance_update_state(self, update_time) -> None:
        if update_time is None:
            return
        current = getattr(self, "_updates_state", 0) or 0
        if update_time > current:
            self._updates_state = update_time

    async def _dispatch_if_new(self, name: str, update: dict,
                               user_guid=None) -> bool:
        """Dispatch once, while learning the timestamp used on recovery."""
        key = self._update_key(name, update)
        seen = getattr(self, "_seen_update_ids", set())
        if key in seen:
            self.logger.debug("Skipping duplicate recovered update %s", key)
            return False

        payload = dict(update)
        payload["client"] = self
        if user_guid is not None:
            payload["user_guid"] = user_guid
        await self.connection.handle_update(name, payload)

        self._record_seen_update(key)
        self._advance_update_state(self._update_time(update))
        return True

    async def _drain_updates(self, payload) -> int:
        """Consume Data's map of update lists or a typed list of updates.

        API responses may be wrapped in ``data`` more than once. Unknown dict
        values are not coerced into fabricated update names. A typed message
        item supplies its own event name; the map form supplies the key name.
        """
        if isinstance(payload, Data):
            payload = payload.original_data

        if isinstance(payload, dict):
            dispatched = 0
            for name, updates in payload.items():
                if name == "client":
                    continue
                if isinstance(updates, list):
                    for update in updates:
                        if isinstance(update, dict):
                            dispatched += await self._dispatch_if_new(
                                name, update
                            )
                elif name == "data" and isinstance(updates, (dict, list)):
                    dispatched += await self._drain_updates(updates)
            return dispatched

        if isinstance(payload, list):
            dispatched = 0
            for update in payload:
                if isinstance(update, dict):
                    name = update.get("type")
                    if isinstance(name, str) and name:
                        dispatched += await self._dispatch_if_new(name, update)
                    else:
                        self.logger.debug(
                            "Ignoring an update without a type during recovery"
                        )
            return dispatched

        return 0

    async def _recover_chats_updates(self) -> int:
        """Fetch missed updates and feed them through the normal dispatch path."""
        state = getattr(self, "_updates_state", 0) or None
        result = await self.get_chats_updates(state=state)
        return await self._drain_updates(result)

    async def get_updates(self: "darkob.Messenger"):
        """
        Listen for updates from Rubika's WebSocket.

        Returns:
            None
        """
        import aiohttp

        existing = getattr(self, "_keep_socket_task", None)
        if existing is None or existing.done():
            self._keep_socket_task = asyncio.create_task(self._keep_socket())

        first_connection = True
        while True:
            if not first_connection:
                # Reconnected: dispatch anything missed while disconnected.
                # Calling get_chats_updates without consuming its result loses
                # those updates even though the request itself succeeded.
                try:
                    recovered = await self._recover_chats_updates()
                    if recovered:
                        self.logger.info(
                            "Recovered %d missed update(s) after reconnect.",
                            recovered,
                        )
                except Exception as exc:
                    self.logger.warning("Gap recovery failed: %s", exc)
            first_connection = False

            try:
                async with self.connection.session.ws_connect(
                    self.connection.wss_url, proxy=self.proxy
                ) as ws:
                    self.connection.ws = ws

                    await ws.send_json({
                        "method": "handShake",
                        "auth": self.auth,
                        "api_version": "6",
                        "data": "",
                    })

                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            self._spawn_ws_update(
                                self._handle_text_message(msg.json())
                            )
                        elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                            self.logger.warning("WebSocket connection lost; initiating reconnect...")
                            break

            except (aiohttp.ServerTimeoutError, TimeoutError, aiohttp.ClientError) as e:
                self.logger.warning(f"WebSocket connection lost: {e}. Attempting reconnection in 3 seconds...")
                await asyncio.sleep(3)

    async def _keep_socket(self: "darkob.Messenger") -> None:
        while True:
            if self.connection.session.closed:
                break

            try:
                await asyncio.sleep(10)

                if self.connection.ws and not self.connection.ws.closed:
                    await self.connection.ws.send_json({})
                    await self._recover_chats_updates()
                else:
                    self.logger.warning("WebSocket disconnected or already closed.")
            except Exception as e:
                self.logger.warning(f"WebSocket keep-alive failed: {e}", exc_info=True)

    async def _handle_text_message(self: "darkob.Messenger", msg_data: dict) -> None:
        from ..core.cipher import Cipher

        data_enc = msg_data.get("data_enc") or msg_data.get("messenger")
        if not data_enc:
            self.logger.debug("Missing update data in message", extra={"data": msg_data})
            return

        if isinstance(data_enc, dict):
            try:
                user_guid = msg_data.get("user_guid")
                tasks = [
                    self._dispatch_if_new(name, update, user_guid)
                    for name, updates in data_enc.items()
                    if isinstance(updates, list)
                    for update in updates
                ]
                await asyncio.gather(*tasks)
            except Exception as e:
                self.logger.error(f"Channel update error: {e}", extra={"data": msg_data}, exc_info=True)
            return

        try:
            decrypted_data = Cipher.decrypt(data_enc, key=self.key)
            user_guid = decrypted_data.pop("user_guid")

            tasks = [
                self._dispatch_if_new(name, update, user_guid)
                for name, updates in decrypted_data.items()
                if isinstance(updates, list)
                for update in updates
            ]

            await asyncio.gather(*tasks)
        except Exception as e:
            self.logger.error(
                f"Failed to handle WebSocket message: {e}",
                extra={"data": msg_data},
                exc_info=True
            )
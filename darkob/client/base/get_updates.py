import asyncio
import logging
from typing import TYPE_CHECKING

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
                # Reconnected: pull anything missed while the socket was
                # down before resuming the live stream.
                try:
                    await self.get_chats_updates()
                    self.logger.info("Recovered missed updates after reconnect.")
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
                    await self.get_chats_updates()
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
                    self.connection.handle_update(
                        name, {**update, "client": self, "user_guid": user_guid}
                    )
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
                self.connection.handle_update(
                    name, {**update, "client": self, "user_guid": user_guid}
                )
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
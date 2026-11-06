import asyncio
import hmac
import json
import logging
import time
from typing import Any, Dict

from aiohttp import web

import darkob
from ..metrics import metrics as _metrics
from ..types.incoming import Events

logger = logging.getLogger(__name__)

WARNING_TEXT = (
    "Webhook is running without 'webhook_secret'. Anyone who learns the URL "
    "can inject fake updates into this bot. Set Bot(webhook_secret=...) and "
    "pass it as ?secret=... in the webhook_url."
)


class Updates:
    # -- update plumbing --------------------------------------------------

    def _spawn_update(self: "darkob.Bot", coro) -> "asyncio.Task":
        """Run an update in the background under a concurrency ceiling.

        Webhook and polling paths used to call ``asyncio.create_task`` for
        every update with no bound, so a burst could create thousands of
        live tasks. The semaphore caps how many run at once.
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

    def _parse_raw_update(self: "darkob.Bot", raw: Dict[str, Any]) -> "Events":

        return Events(data=raw, bot=self)

    async def _safe_feed(self: "darkob.Bot", event):
        """The single funnel every incoming update passes through.

        Polling and webhook both end up here, so plugin hooks, conversation
        resolution and metrics only have to be wired once. Before this, the
        polling loop called ``_registry.feed`` directly and therefore skipped
        both pending ``ask()`` calls and any plugin hook.
        """
        manager = getattr(self, "plugin_manager", None)
        tracked = _metrics.enabled
        started = time.perf_counter() if tracked else 0.0
        if tracked:
            _metrics.increment("darkob.updates")

        try:
            # A plugin that consumes the update stops everything below it.
            if manager is not None and manager.active:
                if await manager.run_on_update(event):
                    return

            conversations = getattr(self, "_conversations", None)
            if conversations is not None and await conversations.resolve(event):
                return
            await self._registry.feed(event)
        except Exception:
            logger.exception("Error while feeding event")
        finally:
            if tracked:
                _metrics.observe(
                    "darkob.update.seconds", time.perf_counter() - started
                )

    # -- webhook ----------------------------------------------------------

    def _webhook_secret_ok(self: "darkob.Bot", request: web.Request) -> bool:
        """Validate the shared secret on an incoming webhook request.

        The secret may arrive as the ``X-Webhook-Secret`` header or as a
        ``secret`` query parameter. Without a configured secret everything
        is accepted, which is only safe on a private network.
        """
        expected = getattr(self, "webhook_secret", None)
        if not expected:
            return True

        provided = (
            request.headers.get("X-Webhook-Secret")
            or request.query.get("secret")
            or ""
        )
        return hmac.compare_digest(str(provided), str(expected))

    async def _handle_webhook(self: "darkob.Bot", request: web.Request) -> web.Response:
        if not self._webhook_secret_ok(request):
            logger.warning(
                "Rejected webhook request with a missing or wrong secret"
            )
            return web.json_response({"status": "UNAUTHORIZED"}, status=401)

        if not getattr(self, "webhook_secret", None):
            if not getattr(self, "_webhook_warned", False):
                self._webhook_warned = True
                logger.warning(WARNING_TEXT)

        try:
            data = await request.json()
        except (json.JSONDecodeError, ValueError):
            logger.error("Invalid JSON received in webhook")
            return web.json_response({"status": "ERROR"}, status=400)

        if not isinstance(data, dict):
            logger.error("Webhook payload was not an object")
            return web.json_response({"status": "ERROR"}, status=400)

        if "inline_message" in data:
            raw = data["inline_message"]
            raw["type"] = "InlineMessage"
            self._spawn_update(self._safe_feed(self._parse_raw_update(raw)))

        elif "update" in data:
            self._spawn_update(self._safe_feed(self._parse_raw_update(data["update"])))

        return web.json_response({"status": "OK"})

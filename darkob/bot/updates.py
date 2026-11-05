import asyncio
import json
import logging
from typing import Any, Dict
from aiohttp import web
import darkob
from ..types.incoming import Events

logger = logging.getLogger(__name__)

class Updates:
    def _parse_raw_update(self: "darkob.Bot", raw: Dict[str, Any]) -> "Events":

        return Events(data=raw, bot=self)

    async def _safe_feed(self: "darkob.Bot", event):
        try:
            await self._registry.feed(event)
        except Exception:
            logger.exception("Error while feeding event")

    async def _handle_webhook(self: "darkob.Bot", request: web.Request) -> web.Response:
        try:
            data = await request.json()
        except json.JSONDecodeError:
            logger.error("Invalid JSON received in webhook")
            return web.json_response({"status": "ERROR"}, status=400)

        if "inline_message" in data:
            raw = data["inline_message"]
            raw["type"] = "InlineMessage"
            event = self._parse_raw_update(raw)
            asyncio.create_task(self._safe_feed(event))

        elif "update" in data:
            event = self._parse_raw_update(data["update"])
            asyncio.create_task(self._safe_feed(event))

        return web.json_response({"status": "OK"})
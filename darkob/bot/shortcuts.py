"""Shortcuts that keep handler code short.

``bot.reply(event, text)`` instead of resolving the chat id and message id
by hand is the difference between one line and four in every handler.
"""

from __future__ import annotations

from typing import Any, AsyncIterator, Optional

import darkob

__all__ = ["Shortcuts"]


class Shortcuts:
    """Convenience methods mixed into :class:`darkob.Bot`."""

    # -- event field access -------------------------------------------------

    @staticmethod
    def _chat_id(event: Any) -> str:
        for attribute in ("chat_id", "object_guid"):
            value = getattr(event, attribute, None)
            if value:
                return value
        raise ValueError(
            "Event has no chat_id or object_guid; cannot address the chat."
        )

    @staticmethod
    def _message_id(event: Any) -> Any:
        for attribute in ("message_id", "id"):
            value = getattr(event, attribute, None)
            if value is not None:
                return value
        raise ValueError("Event has no message_id; it cannot be replied to.")

    # -- message shortcuts --------------------------------------------------

    async def reply(localself, event: Any, text: str, **kwargs: Any):
        """Reply to the message that produced *event*.

        Equivalent to ``send_message`` with ``chat_id`` and
        ``reply_to_message_id`` filled in from the event.
        """
        return await localself.send_message(
            localself._chat_id(event),
            text,
            reply_to_message_id=localself._message_id(event),
            **kwargs,
        )

    async def edit(localself, event: Any, text: str, **kwargs: Any):
        """Edit the message that produced *event* to say *text*."""
        return await localself.edit_message(
            localself._chat_id(event),
            localself._message_id(event),
            text,
            **kwargs,
        )

    async def delete(localself, event: Any):
        """Delete the message that produced *event*."""
        return await localself.delete_message(
            localself._chat_id(event),
            localself._message_id(event),
        )

    # -- updates as an async iterator --------------------------------------

    async def iter_updates(
        localself,
        limit: int = 100,
        max_pages: Optional[int] = None,
    ) -> AsyncIterator[Any]:
        """Yield updates one at a time, handling the offset cursor.

        Args:
            limit: Updates requested per round-trip.
            max_pages: Stop after this many round-trips (``None`` = forever).

        Yields:
            Individual update payloads, in server order.
        """
        offset: Optional[str] = None
        pages = 0

        while max_pages is None or pages < max_pages:
            response = await localself.get_updates(offset_id=offset, limit=limit)

            data: Any = {}
            try:
                data = response["data"] or {}
            except (KeyError, TypeError):
                data = {}

            if not isinstance(data, dict):
                return

            updates = data.get("updates") or []
            for update in updates:
                yield update

            next_offset = data.get("next_offset_id")
            if not next_offset or next_offset == offset:
                return

            offset = next_offset
            pages += 1

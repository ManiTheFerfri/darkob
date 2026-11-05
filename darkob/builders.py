"""Compose a message once, then send it.

Handlers often build the same message in several places: text, a keypad, a
reply target, notification flags. :class:`MessageBuilder` keeps that in
one object::

    from darkob import MessageBuilder, Keyboard

    message = (
        MessageBuilder("Order #42 confirmed")
        .append("Delivery tomorrow")
        .inline(Keyboard().row("Track", "Cancel"))
        .silent()
    )

    await message.send(bot, event.chat_id)

The builder only produces the keyword arguments that were actually set, so
nothing is overridden with a default by accident.
"""

from __future__ import annotations

from typing import Any, Dict

__all__ = ["MessageBuilder"]


class MessageBuilder:
    """Fluent builder for ``send_message`` arguments."""

    __slots__ = ("_text", "_kwargs")

    def __init__(self, text: str = "") -> None:
        if not isinstance(text, str):
            raise TypeError("MessageBuilder text must be a string.")
        self._text = text
        self._kwargs: Dict[str, Any] = {}

    # -- text -------------------------------------------------------------

    def append(self, text: str, separator: str = "\n") -> "MessageBuilder":
        """Add another line of text."""
        if not isinstance(text, str):
            raise TypeError("append() takes a string.")
        self._text = (
            f"{self._text}{separator}{text}" if self._text else text
        )
        return self

    def line(self, text: str = "") -> "MessageBuilder":
        """Add a line, or a blank line when called with no arguments."""
        return self.append(text)

    @property
    def text(self) -> str:
        """The text assembled so far."""
        return self._text

    def set_text(self, text: str) -> "MessageBuilder":
        """Replace the whole text."""
        if not isinstance(text, str):
            raise TypeError("set_text() takes a string.")
        self._text = text
        return self

    # -- options ----------------------------------------------------------

    def keypad(self, keyboard: Any) -> "MessageBuilder":
        """Attach a chat (persistent) keyboard."""
        self._kwargs["chat_keypad"] = keyboard
        return self

    def inline(self, keyboard: Any) -> "MessageBuilder":
        """Attach an inline keyboard."""
        self._kwargs["inline_keypad"] = keyboard
        return self

    def reply_to(self, message_id: Any) -> "MessageBuilder":
        """Send as a reply to *message_id*."""
        self._kwargs["reply_to_message_id"] = message_id
        return self

    def silent(self, enabled: bool = True) -> "MessageBuilder":
        """Disable (or re-enable) the notification sound."""
        self._kwargs["disable_notification"] = enabled
        return self

    def metadata(self, metadata: Dict[str, Any]) -> "MessageBuilder":
        """Attach Rubika text metadata."""
        self._kwargs["metadata"] = metadata
        return self

    def option(self, name: str, value: Any) -> "MessageBuilder":
        """Set any other ``send_message`` keyword."""
        self._kwargs[name] = value
        return self

    def clear_options(self) -> "MessageBuilder":
        """Drop every option, keeping the text."""
        self._kwargs.clear()
        return self

    # -- output -----------------------------------------------------------

    def build(self) -> Dict[str, Any]:
        """Return ``{"text": ..., **options}`` ready for ``send_message``."""
        return {"text": self._text, **self._kwargs}

    async def send(self, bot: Any, chat_id: str) -> Any:
        """Send through *bot* to *chat_id* and return the API result."""
        return await bot.send_message(chat_id, **self.build())

    def __len__(self) -> int:
        return len(self._text)

    def __repr__(self) -> str:
        return f"MessageBuilder(text={self._text[:20]!r}, options={sorted(self._kwargs)})"

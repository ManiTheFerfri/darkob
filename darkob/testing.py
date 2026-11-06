"""Helpers for testing bots without a token, network or sleeping.

    from darkob.testing import FakeBot, make_message

    async def test_echo():
        bot = FakeBot()
        event = make_message(text="hi")
        await echo(bot, event)
        assert event.replies == ["hi"]
        assert bot.calls[0][0] == "send_message"
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple

__all__ = ["FakeBot", "FakeEvent", "make_message"]


class FakeBot:
    """Records every method call instead of hitting the API.

    Access any attribute and get an awaitable recorder::

        bot = FakeBot()
        await bot.send_message("chat", "hi")
        bot.calls  # [("send_message", ("chat", "hi"), {})]
    """

    calls: List[Tuple[str, Tuple[Any, ...], Dict[str, Any]]]

    def __init__(self, **attributes: Any) -> None:
        object.__setattr__(self, "calls", [])
        for name, value in attributes.items():
            object.__setattr__(self, name, value)

    def __getattr__(self, name: str) -> Callable[..., Any]:
        if name.startswith("__"):
            raise AttributeError(name)

        async def recorder(*args: Any, **kwargs: Any) -> Dict[str, Any]:
            self.calls.append((name, args, kwargs))
            return {"status": "OK", "method": name}

        return recorder

    # -- assertions -------------------------------------------------------

    def called(self, method: str) -> bool:
        """True when *method* was called at least once.

        Examples:
            >>> from darkob.testing import FakeBot
            >>> bot = FakeBot()
            >>> bot.called("send_message")
            False
        """
        return any(call[0] == method for call in self.calls)

    def calls_to(self, method: str) -> List[Tuple[Any, ...]]:
        """Return ``(args, kwargs)`` pairs for *method*."""
        return [(args, kwargs) for name, args, kwargs in self.calls if name == method]

    def last_call(self) -> Optional[Tuple[str, Tuple[Any, ...], Dict[str, Any]]]:
        """Return the most recent call, or ``None``."""
        return self.calls[-1] if self.calls else None

    def reset(self) -> None:
        """Forget recorded calls."""
        self.calls.clear()

    def __repr__(self) -> str:
        return f"FakeBot(calls={len(self.calls)})"


class FakeEvent:
    """An event-shaped object with recording reply/edit/delete helpers."""

    def __init__(
        self,
        text: str = "",
        chat_id: str = "g0test",
        message_id: str = "1",
        author_id: str = "u0test",
        **attributes: Any,
    ) -> None:
        self.text = text
        self.chat_id = chat_id
        self.message_id = message_id
        self.author_id = author_id
        self.replies: List[Any] = []
        self.edits: List[Any] = []
        self.deleted = False
        self._memo: Dict[str, Any] = {}

        for name, value in attributes.items():
            setattr(self, name, value)

    async def reply(self, text: str, **kwargs: Any) -> Dict[str, Any]:
        self.replies.append(text)
        return {"status": "OK"}

    async def edit(self, text: str, **kwargs: Any) -> Dict[str, Any]:
        self.edits.append(text)
        return {"status": "OK"}

    async def delete(self) -> Dict[str, Any]:
        self.deleted = True
        return {"status": "OK"}

    def __repr__(self) -> str:
        return f"FakeEvent(chat_id={self.chat_id!r}, text={self.text!r})"


def make_message(
    text: str = "",
    chat_id: str = "g0test",
    message_id: str = "1",
    **attributes: Any,
) -> FakeEvent:
    """Build a :class:`FakeEvent` that looks like an incoming message."""
    return FakeEvent(
        text=text,
        chat_id=chat_id,
        message_id=message_id,
        **attributes,
    )

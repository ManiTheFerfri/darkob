"""Await the next matching message instead of writing a state machine.

Most bots need a one-off question:

    reply = await client.ask(chat_id, "What is your phone number?", timeout=60)

While an ``ask`` is pending, the next message in that chat that satisfies
the filters is handed to the caller *before* normal handlers see it. That
turns "prompt then wait" into a single await instead of a handler plus a
global ``waiting_for`` flag.
"""

from __future__ import annotations

import asyncio
import inspect
from typing import Any, Callable, Dict, List, Optional

__all__ = ["ConversationManager", "Waiter", "ask", "NoReply"]

Matcher = Callable[[Any], Any]


class NoReply(asyncio.TimeoutError):
    """Raised when a conversation prompt goes unanswered in time."""


class Waiter:
    """One pending ``ask`` call."""

    __slots__ = ("chat_id", "filters", "future", "cancelled")

    def __init__(self, chat_id: str, filters: List[Matcher]) -> None:
        self.chat_id = chat_id
        self.filters = filters
        self.future: "asyncio.Future[Any]" = asyncio.get_running_loop().create_future()
        self.cancelled = False

    async def matches(self, event: Any) -> bool:
        """True when *event* answers this waiter."""
        for matcher in self.filters:
            try:
                result = matcher(event)
                if inspect.isawaitable(result):
                    result = await result
                if not result:
                    return False
            except Exception:
                return False
        return True

    def resolve(self, event: Any) -> None:
        if not self.future.done():
            self.future.set_result(event)

    def cancel(self) -> None:
        self.cancelled = True
        if not self.future.done():
            self.future.cancel()

    def __repr__(self) -> str:
        return f"Waiter(chat_id={self.chat_id!r})"


class ConversationManager:
    """Registry of pending conversations, keyed by chat."""

    __slots__ = ("_waiters",)

    def __init__(self) -> None:
        self._waiters: Dict[str, List[Waiter]] = {}

    def register(self, chat_id: str, filters: Optional[List[Matcher]] = None) -> Waiter:
        """Create and track a waiter for *chat_id*."""
        waiter = Waiter(chat_id, list(filters or []))
        self._waiters.setdefault(chat_id, []).append(waiter)
        return waiter

    def unregister(self, waiter: Waiter) -> None:
        """Stop tracking *waiter*."""
        bucket = self._waiters.get(waiter.chat_id)
        if not bucket:
            return
        if waiter in bucket:
            bucket.remove(waiter)
        if not bucket:
            self._waiters.pop(waiter.chat_id, None)

    async def resolve(self, event: Any) -> bool:
        """Hand *event* to the first interested waiter.

        Returns ``True`` when a waiter consumed it, meaning normal dispatch
        should skip this event.
        """
        chat_id = _chat_id_of(event)
        if chat_id is None:
            return False

        bucket = self._waiters.get(chat_id)
        if not bucket:
            return False

        for waiter in list(bucket):
            if waiter.cancelled:
                continue
            if await waiter.matches(event):
                waiter.resolve(event)
                self.unregister(waiter)
                return True
        return False

    def pending(self, chat_id: Optional[str] = None) -> int:
        """Number of pending conversations, overall or for one chat."""
        if chat_id is None:
            return sum(len(bucket) for bucket in self._waiters.values())
        return len(self._waiters.get(chat_id, ()))

    def cancel_all(self) -> None:
        """Cancel every pending conversation."""
        for bucket in list(self._waiters.values()):
            for waiter in bucket:
                waiter.cancel()
        self._waiters.clear()

    def __repr__(self) -> str:
        return f"ConversationManager(pending={self.pending()})"


def _chat_id_of(event: Any) -> Optional[str]:
    """Best-effort chat identifier from an event of either surface."""
    for attribute in ("chat_id", "chat_guid", "object_guid"):
        value = getattr(event, attribute, None)
        if value:
            return str(value)
    return None


async def ask(
    owner: Any,
    chat_id: str,
    text: Optional[str] = None,
    *,
    filters: Optional[List[Matcher]] = None,
    timeout: float = 60.0,
    keypad: Any = None,
    inline_keypad: Any = None,
) -> Any:
    """Send *text* and return the next matching reply in the chat.

    The conversation registry is taken from ``owner._conversations``; the
    prompt is sent with whichever ``send_message`` signature the owner has.
    """
    manager = getattr(owner, "_conversations", None)
    if manager is None:
        raise RuntimeError(
            "This object has no conversation registry; use Bot or Client."
        )

    waiter = manager.register(chat_id, filters)
    try:
        if text:
            await _send_prompt(owner, chat_id, text, keypad, inline_keypad)
        try:
            return await asyncio.wait_for(waiter.future, timeout=timeout)
        except asyncio.TimeoutError:
            raise NoReply(
                f"No reply in chat {chat_id!r} within {timeout} seconds."
            ) from None
    finally:
        manager.unregister(waiter)


async def _send_prompt(
    owner: Any,
    chat_id: str,
    text: str,
    keypad: Any,
    inline_keypad: Any,
) -> Any:
    """Send a prompt using whichever keypad keywords the owner accepts."""
    signature = inspect.signature(owner.send_message)
    parameters = signature.parameters

    kwargs: Dict[str, Any] = {}
    if keypad is not None:
        # Bot calls it chat_keypad; the Messenger surface also uses it.
        if "chat_keypad" in parameters:
            kwargs["chat_keypad"] = keypad
    if inline_keypad is not None and "inline_keypad" in parameters:
        kwargs["inline_keypad"] = inline_keypad

    return await owner.send_message(chat_id, text, **kwargs)

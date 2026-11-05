"""Token-bucket rate limiting.

Rubika throttles bots, and a burst of sends is the fastest way to get a
``TOO_REQUESTS`` back. A limiter keeps the bot under the ceiling before the
server has to enforce it::

    from darkob import Bot, RateLimiter

    bot = Bot(
        token="...",
        rate_limiter=RateLimiter(rate=20, burst=5, per_chat_rate=3),
    )

Two levels are supported:

* a **global** bucket for the whole client, and
* optional **per-chat** buckets, so one busy group cannot starve the rest.

Both are token buckets: ``rate`` tokens per second, held in a bucket of at
most ``capacity``. A call takes one token, waiting if the bucket is empty.
"""

from __future__ import annotations

import asyncio
import time
from typing import Callable, Dict, Optional

__all__ = ["TokenBucket", "RateLimiter"]


class TokenBucket:
    """A classic token bucket with async acquisition."""

    __slots__ = ("rate", "capacity", "_tokens", "_updated", "_clock", "_lock")

    def __init__(
        self,
        rate: float,
        capacity: Optional[float] = None,
        *,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if rate <= 0:
            raise ValueError("rate must be greater than 0.")
        if capacity is not None and capacity <= 0:
            raise ValueError("capacity must be greater than 0.")

        self.rate = float(rate)
        self.capacity = float(capacity if capacity is not None else max(1.0, rate))
        self._tokens = self.capacity
        self._clock = clock
        self._updated = clock()
        self._lock = asyncio.Lock()

    # -- internals --------------------------------------------------------

    def _refill(self) -> None:
        now = self._clock()
        elapsed = now - self._updated
        if elapsed <= 0:
            return
        self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)
        self._updated = now

    # -- public api -------------------------------------------------------

    @property
    def tokens(self) -> float:
        """Tokens available right now (after refilling to the clock)."""
        self._refill()
        return self._tokens

    def try_acquire(self, tokens: float = 1.0) -> bool:
        """Take *tokens* if available, without waiting."""
        self._refill()
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    async def acquire(self, tokens: float = 1.0) -> None:
        """Take *tokens*, waiting until they are available."""
        if tokens > self.capacity:
            raise ValueError(
                f"Cannot acquire {tokens} tokens from a bucket of capacity "
                f"{self.capacity}."
            )

        while True:
            async with self._lock:
                self._refill()
                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return
                missing = tokens - self._tokens
                wait = missing / self.rate
            await asyncio.sleep(wait)

    def __repr__(self) -> str:
        return f"TokenBucket(rate={self.rate}, capacity={self.capacity})"


class RateLimiter:
    """A global bucket plus optional per-conversation buckets."""

    __slots__ = (
        "rate",
        "burst",
        "per_chat_rate",
        "per_chat_burst",
        "max_buckets",
        "_global",
        "_chats",
    )

    def __init__(
        self,
        rate: float = 20.0,
        burst: Optional[float] = None,
        *,
        per_chat_rate: Optional[float] = None,
        per_chat_burst: Optional[float] = None,
        max_buckets: int = 4096,
    ) -> None:
        self.rate = float(rate)
        self.burst = burst
        self.per_chat_rate = per_chat_rate
        self.per_chat_burst = per_chat_burst
        self.max_buckets = max_buckets
        self._global = TokenBucket(rate, burst)
        self._chats: Dict[str, TokenBucket] = {}

    def for_chat(self, chat_id: str) -> TokenBucket:
        """Return (creating if needed) the bucket for one conversation."""
        bucket = self._chats.get(chat_id)
        if bucket is None:
            if len(self._chats) >= self.max_buckets:
                # Drop the oldest entry rather than growing without bound.
                self._chats.pop(next(iter(self._chats)), None)
            bucket = TokenBucket(
                self.per_chat_rate or self.rate, self.per_chat_burst
            )
            self._chats[chat_id] = bucket
        return bucket

    async def acquire(self, chat_id: Optional[str] = None) -> None:
        """Wait for capacity, honouring the per-chat bucket when configured."""
        if chat_id is not None and self.per_chat_rate:
            await self.for_chat(chat_id).acquire()
        await self._global.acquire()

    def __repr__(self) -> str:
        return (
            f"RateLimiter(rate={self.rate}, burst={self.burst}, "
            f"per_chat_rate={self.per_chat_rate})"
        )

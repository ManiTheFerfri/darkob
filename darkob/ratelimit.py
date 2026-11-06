"""Token-bucket rate limiting, optionally self-tuning.

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

Adaptive limiting
-----------------

A fixed rate is a guess. If the server is being generous you are leaving
throughput on the table; if it is being strict you get throttled anyway. An
adaptive limiter closes the loop with additive-increase / multiplicative-
decrease (AIMD), the same control law TCP congestion control uses::

    from darkob import Bot, AdaptiveRateLimiter

    bot = Bot(
        token="...",
        # Start optimistically at 20/s, never drop below 2/s, halve on
        # every throttle, and climb back by 1/s per second of clean traffic.
        rate_limiter=AdaptiveRateLimiter(
            rate=20, min_rate=2, decrease_factor=0.5, increase_step=1.0,
        ),
    )

The client reports every throttle back into the limiter, so no wiring is
needed beyond passing the object to ``Bot(...)``. The effective rate is
available as :attr:`RateLimiter.current_rate` and :meth:`RateLimiter.stats`.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any, Callable, Dict, Optional

from .utils.concurrency import LazyLock

__all__ = ["TokenBucket", "RateLimiter", "AdaptiveRateLimiter"]


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
        # Lazily, not eagerly: a limiter built at import time has no running
        # loop to bind a 3.9 lock to.
        self._lock = LazyLock()

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
        """Take *tokens* if available, without waiting.

        Examples:
            >>> from darkob.ratelimit import TokenBucket
            >>> bucket = TokenBucket(rate=10, capacity=2)
            >>> [bucket.try_acquire() for _ in range(3)]
            [True, True, False]
        """
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
    """A global bucket plus optional per-conversation buckets.

    With ``adaptive=True`` the global rate starts at ``rate`` and is tuned by
    :meth:`on_throttle` / :meth:`on_success`, which the client calls
    automatically. Adaptive mode is off by default so that existing bots keep
    their exact previous behaviour.
    """

    __slots__ = (
        "rate",
        "burst",
        "per_chat_rate",
        "per_chat_burst",
        "max_buckets",
        "adaptive",
        "min_rate",
        "decrease_factor",
        "increase_step",
        "increase_interval",
        "max_block",
        "_global",
        "_chats",
        "_clock",
        "_current_rate",
        "_last_increase",
        "_blocked_until",
        "_throttles",
        "_recoveries",
        "_acquired",
    )

    def __init__(
        self,
        rate: float = 20.0,
        burst: Optional[float] = None,
        *,
        per_chat_rate: Optional[float] = None,
        per_chat_burst: Optional[float] = None,
        max_buckets: int = 4096,
        adaptive: bool = False,
        min_rate: float = 1.0,
        decrease_factor: float = 0.5,
        increase_step: float = 1.0,
        increase_interval: float = 1.0,
        max_block: float = 60.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if rate <= 0:
            raise ValueError("rate must be greater than 0.")
        if not 0 < decrease_factor < 1:
            raise ValueError("decrease_factor must be between 0 and 1 (exclusive).")
        if increase_step <= 0:
            raise ValueError("increase_step must be greater than 0.")
        if increase_interval <= 0:
            raise ValueError("increase_interval must be greater than 0.")
        if min_rate <= 0:
            raise ValueError("min_rate must be greater than 0.")
        if min_rate > rate:
            raise ValueError("min_rate cannot exceed the starting rate.")

        self.rate = float(rate)
        self.burst = burst
        self.per_chat_rate = per_chat_rate
        self.per_chat_burst = per_chat_burst
        self.max_buckets = max_buckets
        self.adaptive = adaptive
        self.min_rate = float(min_rate)
        self.decrease_factor = float(decrease_factor)
        self.increase_step = float(increase_step)
        self.increase_interval = float(increase_interval)
        self.max_block = float(max_block)
        self._global = TokenBucket(rate, burst)
        self._chats: Dict[str, TokenBucket] = {}

        self._clock = clock
        self._current_rate = float(rate)
        self._last_increase = clock()
        self._blocked_until = 0.0
        self._throttles = 0
        self._recoveries = 0
        self._acquired = 0

    def for_chat(self, chat_id: str) -> TokenBucket:
        """Return (creating if needed) the bucket for one conversation."""
        bucket = self._chats.get(chat_id)
        if bucket is None:
            if len(self._chats) >= self.max_buckets:
                # Drop the oldest entry rather than growing without bound.
                self._chats.pop(next(iter(self._chats)), None)
            bucket = TokenBucket(
                self._effective_per_chat_rate(), self.per_chat_burst
            )
            self._chats[chat_id] = bucket
        return bucket

    # -- adaptive control -------------------------------------------------

    @property
    def current_rate(self) -> float:
        """The effective global rate right now, in tokens per second."""
        return self._current_rate

    @property
    def blocked_for(self) -> float:
        """Seconds of forced quiet remaining from the last throttle."""
        remaining = self._blocked_until - self._clock()
        return remaining if remaining > 0 else 0.0

    def _effective_per_chat_rate(self) -> float:
        base = self.per_chat_rate or self.rate
        if not self.adaptive or self.rate <= 0:
            return base
        return max(base * (self._current_rate / self.rate), base * 0.01)

    def _apply_rate(self, new_rate: float) -> None:
        """Push a new effective rate into every live bucket."""
        new_rate = max(self.min_rate, min(self.rate, new_rate))
        if new_rate == self._current_rate:
            return
        self._current_rate = new_rate
        self._global.rate = new_rate

        want = base = self.per_chat_rate or self.rate
        if self.per_chat_rate:
            scaled = base * (new_rate / self.rate)
            want = max(scaled, base * 0.01)
        for bucket in self._chats.values():
            bucket.rate = want

    def on_throttle(self, retry_after: Optional[float] = None) -> float:
        """Report that the server pushed back. Halves the effective rate.

        Args:
            retry_after: Seconds the server asked us to wait, if it said so
                (for example via a ``Retry-After`` header). Acquisition is
                blocked for this long, capped at :attr:`max_block`.

        Returns:
            The new effective rate, in tokens per second. Non-adaptive
            limiters return their configured rate unchanged.

        Examples:
            >>> from darkob import AdaptiveRateLimiter
            >>> limiter = AdaptiveRateLimiter(rate=20)
            >>> limiter.on_throttle()
            10.0
            >>> limiter.current_rate
            10.0
        """
        if not self.adaptive:
            return self.rate

        self._throttles += 1
        self._apply_rate(self._current_rate * self.decrease_factor)
        now = self._clock()
        self._last_increase = now

        if retry_after is not None and retry_after > 0:
            pause = min(float(retry_after), self.max_block)
            self._blocked_until = max(self._blocked_until, now + pause)

        return self._current_rate

    def on_success(self) -> None:
        """Report that a request succeeded; climb back towards ``rate``."""
        if not self.adaptive:
            return

        self._acquired += 1
        if self._current_rate >= self.rate:
            return

        now = self._clock()
        if now - self._last_increase >= self.increase_interval:
            self._apply_rate(self._current_rate + self.increase_step)
            self._last_increase = now
            self._recoveries += 1

    def reset(self) -> None:
        """Return to the configured rate and forget throttle history."""
        self._current_rate = self.rate
        self._global.rate = self.rate
        self._blocked_until = 0.0
        self._last_increase = self._clock()
        self._throttles = 0
        self._recoveries = 0
        self._acquired = 0
        for bucket in self._chats.values():
            bucket.rate = self.per_chat_rate or self.rate

    def stats(self) -> Dict[str, Any]:
        """A snapshot of the limiter's state, suitable for logging or metrics."""
        return {
            "rate": self.rate,
            "current_rate": self._current_rate,
            "min_rate": self.min_rate,
            "adaptive": self.adaptive,
            "throttles": self._throttles,
            "recoveries": self._recoveries,
            "acquired": self._acquired,
            "blocked_for": self.blocked_for,
            "chats_tracked": len(self._chats),
            "tokens": self._global.tokens,
        }

    # -- acquisition ------------------------------------------------------

    async def acquire(self, chat_id: Optional[str] = None) -> None:
        """Wait for capacity, honouring the per-chat bucket when configured."""
        wait = self._blocked_until - self._clock()
        if wait > 0:
            # The server told us to stop; sleeping inside acquire() means
            # every caller is held back, not just the one that was throttled.
            await asyncio.sleep(wait)

        if chat_id is not None and self.per_chat_rate:
            await self.for_chat(chat_id).acquire()
        await self._global.acquire()

    def __repr__(self) -> str:
        if self.adaptive:
            return (
                f"RateLimiter(rate={self.rate}, current={self._current_rate:.2f}, "
                f"per_chat_rate={self.per_chat_rate}, adaptive=True)"
            )
        return (
            f"RateLimiter(rate={self.rate}, burst={self.burst}, "
            f"per_chat_rate={self.per_chat_rate})"
        )


class AdaptiveRateLimiter(RateLimiter):
    """A :class:`RateLimiter` with AIMD tuning switched on.

    Equivalent to ``RateLimiter(..., adaptive=True)``; provided as its own
    name so the behaviour is visible at the call site.
    """

    __slots__ = ()

    def __init__(
        self,
        rate: float = 20.0,
        burst: Optional[float] = None,
        *,
        per_chat_rate: Optional[float] = None,
        per_chat_burst: Optional[float] = None,
        max_buckets: int = 4096,
        min_rate: float = 1.0,
        decrease_factor: float = 0.5,
        increase_step: float = 1.0,
        increase_interval: float = 1.0,
        max_block: float = 60.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        super().__init__(
            rate,
            burst,
            per_chat_rate=per_chat_rate,
            per_chat_burst=per_chat_burst,
            max_buckets=max_buckets,
            adaptive=True,
            min_rate=min_rate,
            decrease_factor=decrease_factor,
            increase_step=increase_step,
            increase_interval=increase_interval,
            max_block=max_block,
            clock=clock,
        )

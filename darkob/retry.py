"""A retry policy you can reason about and pass around.

The client already retries, but its knobs live on the constructor. A
:class:`Retry` value object makes the policy explicit, unit-testable, and
overridable per request::

    from darkob import Retry

    client = Messenger(..., retry=Retry(attempts=5, backoff=0.5))
    client.retry = Retry.none()          # fail fast
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional

__all__ = ["Retry"]


@dataclass(frozen=True)
class Retry:
    """How many times to retry, and how long to wait between attempts.

    Attributes:
        attempts: Total attempts, including the first. Must be >= 1.
        backoff: Base delay in seconds.
        jitter: Fraction of the delay randomised, 0.0–1.0. Keeps many bots
            from retrying in lockstep.
        max_delay: Upper bound for any single delay, in seconds.
        rate_limit_backoff: Base delay used when the server reports rate
            limiting, instead of ``backoff``.
    """

    attempts: int = 3
    backoff: float = 1.0
    jitter: float = 0.5
    max_delay: float = 30.0
    rate_limit_backoff: float = 5.0

    def __post_init__(self) -> None:
        if self.attempts < 1:
            raise ValueError("Retry.attempts must be >= 1.")
        if self.backoff < 0:
            raise ValueError("Retry.backoff must be >= 0.")
        if not 0.0 <= self.jitter <= 1.0:
            raise ValueError("Retry.jitter must be between 0.0 and 1.0.")
        if self.max_delay <= 0:
            raise ValueError("Retry.max_delay must be > 0.")

    # -- timing -----------------------------------------------------------

    def base_delay(self, attempt: int, *, rate_limited: bool = False) -> float:
        """Delay before attempt number *attempt* (1-based), before jitter."""
        if rate_limited:
            return min(
                self.rate_limit_backoff * (2 ** max(0, attempt - 1)),
                self.max_delay,
            )
        return min(self.backoff * attempt, self.max_delay)

    def delay(
        self,
        attempt: int,
        *,
        rate_limited: bool = False,
        rng: Optional[random.Random] = None,
    ) -> float:
        """Delay before attempt *attempt*, with jitter applied."""
        base = self.base_delay(attempt, rate_limited=rate_limited)
        if self.jitter <= 0 or base <= 0:
            return base

        generator = rng or random
        spread = base * self.jitter
        return max(0.0, base - spread + spread * 2 * generator.random())

    def should_retry(self, attempt: int) -> bool:
        """True when another attempt is allowed after failed *attempt*."""
        return attempt < self.attempts

    # -- presets ----------------------------------------------------------

    @classmethod
    def none(cls) -> "Retry":
        """A single attempt, no waiting — useful in tests and CLIs."""
        return cls(attempts=1, backoff=0.0, jitter=0.0)

    @classmethod
    def aggressive(cls) -> "Retry":
        """Many quick attempts — for interactive, latency-sensitive bots."""
        return cls(attempts=5, backoff=0.25, jitter=0.5, max_delay=5.0)

    @classmethod
    def patient(cls) -> "Retry":
        """Few slow attempts — for batch jobs that must not hammer an API."""
        return cls(attempts=4, backoff=3.0, jitter=0.3, max_delay=60.0)

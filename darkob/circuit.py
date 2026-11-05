"""Per-endpoint circuit breaker.

A failing data centre should stop being tried, instead of burning the
whole retry budget on every request::

    breaker = CircuitBreaker(threshold=5, reset_timeout=30.0)

State machine:

    closed --(threshold consecutive failures)--> open
    open   --(reset_timeout elapsed)----------> half_open
    half_open --(success)--> closed
    half_open --(failure)--> open
"""

from __future__ import annotations

import time
from typing import Optional

__all__ = ["CircuitBreaker", "CLOSED", "OPEN", "HALF_OPEN"]

CLOSED = "closed"
OPEN = "open"
HALF_OPEN = "half_open"


class CircuitBreaker:
    """Track failures for one endpoint and trip when they pile up."""

    __slots__ = ("threshold", "reset_timeout", "_failures", "_state", "_opened_at")

    def __init__(self, threshold: int = 5, reset_timeout: float = 30.0) -> None:
        if threshold < 1:
            raise ValueError("threshold must be >= 1.")
        if reset_timeout <= 0:
            raise ValueError("reset_timeout must be > 0.")

        self.threshold = threshold
        self.reset_timeout = reset_timeout
        self._failures = 0
        self._state = CLOSED
        self._opened_at = 0.0

    # -- introspection ----------------------------------------------------

    @property
    def failures(self) -> int:
        """Consecutive failures since the last success."""
        return self._failures

    @property
    def state(self) -> str:
        """Current state, accounting for an elapsed reset timeout."""
        return self._current_state(time.time())

    def _current_state(self, now: float) -> str:
        if self._state == OPEN and (now - self._opened_at) >= self.reset_timeout:
            self._state = HALF_OPEN
        return self._state

    def is_open(self, now: Optional[float] = None) -> bool:
        """True when this endpoint should be skipped."""
        return self._current_state(now if now is not None else time.time()) == OPEN

    def allows_request(self, now: Optional[float] = None) -> bool:
        """True when a request may be attempted (closed or half-open)."""
        return not self.is_open(now)

    # -- transitions ------------------------------------------------------

    def record_success(self) -> None:
        """A request succeeded: close the circuit and reset the count."""
        self._failures = 0
        self._state = CLOSED
        self._opened_at = 0.0

    def record_failure(self, now: Optional[float] = None) -> None:
        """A request failed: count it and trip when the threshold is reached."""
        moment = now if now is not None else time.time()
        self._failures += 1

        if self._state == HALF_OPEN:
            # The probe failed; go straight back to open.
            self._state = OPEN
            self._opened_at = moment
            return

        if self._failures >= self.threshold:
            self._state = OPEN
            self._opened_at = moment

    def reset(self) -> None:
        """Forget everything (used by tests and manual recovery)."""
        self._failures = 0
        self._state = CLOSED
        self._opened_at = 0.0

    def __repr__(self) -> str:
        return (
            f"CircuitBreaker(state={self.state!r}, failures={self._failures}"
            f"/{self.threshold})"
        )

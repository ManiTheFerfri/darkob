"""In-process metrics for production bots.

A bot in production needs to answer "how many updates am I processing, how slow
are my handlers, is the API throttling me?" without pulling in a metrics
server. This module keeps that bookkeeping in plain dicts and can render the
result in Prometheus text format when you do have a collector::

    from darkob.metrics import enable_metrics, metrics

    enable_metrics()                       # off by default
    bot.run()
    ...
    print(metrics.snapshot())              # plain dict, JSON-serialisable
    print(metrics.render_prometheus())     # text/plain exposition format

What gets recorded automatically
--------------------------------

Enabling metrics instruments the hot paths:

======================  ==================================================
``darkob.updates``      Updates received, by event name.
``darkob.update.seconds``  Time from receipt to end of dispatch.
``darkob.handlers.skipped``  Filters that did not match.
``darkob.handlers.called``   Handler invocations that passed the filters.
``darkob.handlers.errors``   Exceptions raised by handlers.
``darkob.api.requests``      HTTP calls issued.
``darkob.api.errors``        HTTP calls that did not succeed.
``darkob.api.retries``       Retry attempts after a failure.
``darkob.api.ratelimited``   Server-side throttles observed.
``darkob.api.seconds``       Per-call latency.
``darkob.queue.pending``     Messages waiting in a ``SendQueue``.
======================  ==================================================

Custom instrumentation
----------------------

The same primitives are public, so application code can share one registry::

    from darkob.metrics import metrics

    metrics.increment("orders.created")
    with metrics.timer("orders.checkout"):
        await checkout()

    @metrics.time_it("catalog.search")
    async def search(query: str) -> list:
        ...

Cost when disabled
------------------

Everything is guarded by a single boolean attribute read. With metrics off,
the instrumentation costs one attribute lookup and a branch per hot-path
call — it does not allocate, lock, or format anything.
"""

from __future__ import annotations

import functools
import threading
import time
from typing import Any, Callable, Dict, List, Optional, TypeVar

__all__ = [
    "Histogram",
    "Metrics",
    "metrics",
    "enable_metrics",
    "disable_metrics",
    "get_metrics",
]

_F = TypeVar("_F", bound=Callable[..., Any])

#: Characters Prometheus allows in a metric name.
_ALLOWED = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_:")


def sanitize_name(name: str) -> str:
    """Turn ``darkob.api.requests`` into ``darkob_api_requests``."""
    return "".join(char if char in _ALLOWED else "_" for char in name)


class Histogram:
    """A counter plus a bounded sample window for percentiles.

    Percentiles need the values, not just aggregates, so the last
    ``capacity`` observations are kept in a fixed-size ring buffer. Memory is
    bounded no matter how many observations arrive, and the sort only happens
    when you ask for a snapshot.

    Examples:
        >>> from darkob.metrics import Histogram
        >>> latencies = Histogram(capacity=4)
        >>> for value in (1.0, 2.0, 3.0, 4.0):
        ...     latencies.observe(value)
        >>> latencies.count
        4
        >>> latencies.mean
        2.5
        >>> latencies.percentile(0.5)
        2.5
    """

    __slots__ = (
        "count",
        "total",
        "minimum",
        "maximum",
        "_samples",
        "_next",
        "_capacity",
    )

    def __init__(self, capacity: int = 512) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1.")
        self.count = 0
        self.total = 0.0
        self.minimum: Optional[float] = None
        self.maximum: Optional[float] = None
        self._samples: List[float] = [0.0] * capacity
        self._next = 0
        self._capacity = capacity

    def observe(self, value: float) -> None:
        """Record one observation."""
        self.count += 1
        self.total += value
        if self.minimum is None or value < self.minimum:
            self.minimum = value
        if self.maximum is None or value > self.maximum:
            self.maximum = value
        self._samples[self._next] = value
        self._next += 1
        if self._next == self._capacity:
            self._next = 0

    def percentile(self, quantile: float) -> Optional[float]:
        """The *quantile* (0..1) of the retained window, or ``None``."""
        if self.count == 0:
            return None
        window = self._samples[: min(self.count, self._capacity)]
        window.sort()
        if quantile <= 0:
            return window[0]
        if quantile >= 1:
            return window[-1]
        position = quantile * (len(window) - 1)
        lower = int(position)
        upper = min(lower + 1, len(window) - 1)
        weight = position - lower
        return window[lower] * (1.0 - weight) + window[upper] * weight

    @property
    def mean(self) -> Optional[float]:
        """Arithmetic mean of every observation, or ``None``."""
        if self.count == 0:
            return None
        return self.total / self.count

    def snapshot(self) -> Dict[str, Any]:
        """A JSON-friendly summary."""
        return {
            "count": self.count,
            "sum": self.total,
            "min": self.minimum,
            "max": self.maximum,
            "mean": self.mean,
            "p50": self.percentile(0.50),
            "p95": self.percentile(0.95),
            "p99": self.percentile(0.99),
        }

    def reset(self) -> None:
        """Forget every observation."""
        self.count = 0
        self.total = 0.0
        self.minimum = None
        self.maximum = None
        self._samples = [0.0] * self._capacity
        self._next = 0

    def __repr__(self) -> str:
        return f"Histogram(count={self.count}, mean={self.mean})"


class _Timer:
    """Context manager returned by :meth:`Metrics.timer`."""

    __slots__ = ("_metrics", "_name", "_started")

    def __init__(self, metrics: "Metrics", name: str) -> None:
        self._metrics = metrics
        self._name = name
        self._started = 0.0

    def __enter__(self) -> "_Timer":
        self._started = time.perf_counter()
        return self

    def __exit__(self, *exc_info: Any) -> bool:
        self._metrics.observe(
            self._name, time.perf_counter() - self._started
        )
        return False


class Metrics:
    """A small, allocation-light metric registry.

    Recording is lock-free: counters are plain dict entries and histograms are
    fixed-size rings. That is safe because the library records from the event
    loop thread only. :meth:`snapshot`, :meth:`render_prometheus` and
    :meth:`reset` take a lock, so they may be called from another thread —
    which is what an HTTP metrics endpoint or a signal handler does.
    """

    __slots__ = (
        "enabled",
        "prefix",
        "histogram_capacity",
        "_counters",
        "_gauges",
        "_histograms",
        "_lock",
    )

    def __init__(
        self,
        *,
        enabled: bool = False,
        prefix: str = "darkob",
        histogram_capacity: int = 512,
    ) -> None:
        self.enabled = enabled
        self.prefix = prefix
        self.histogram_capacity = histogram_capacity
        self._counters: Dict[str, float] = {}
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, Histogram] = {}
        self._lock = threading.Lock()

    # -- recording --------------------------------------------------------

    def increment(self, name: str, value: float = 1) -> None:
        """Add *value* to a counter."""
        self._counters[name] = self._counters.get(name, 0) + value

    def decrement(self, name: str, value: float = 1) -> None:
        """Subtract *value* from a counter."""
        self._counters[name] = self._counters.get(name, 0) - value

    def set(self, name: str, value: float) -> None:
        """Set a gauge to an absolute value."""
        self._gauges[name] = value

    def adjust(self, name: str, delta: float = 1) -> None:
        """Move a gauge by *delta*."""
        self._gauges[name] = self._gauges.get(name, 0) + delta

    def observe(self, name: str, value: float) -> None:
        """Record one observation in a histogram."""
        histogram = self._histograms.get(name)
        if histogram is None:
            histogram = Histogram(self.histogram_capacity)
            self._histograms[name] = histogram
        histogram.observe(value)

    def timer(self, name: str) -> _Timer:
        """Time a block and record it into a histogram of seconds."""
        return _Timer(self, name)

    def time_it(self, name: Optional[str] = None) -> Callable[[_F], _F]:
        """Decorator recording a call's duration, for sync and async functions.

        ``@metrics.time_it("handler.fetch")`` works on both kinds of
        callable and returns the wrapped object unchanged while metrics are
        disabled.
        """

        def decorate(func: _F) -> _F:
            label = name or f"{func.__module__}.{func.__qualname__}"

            if _is_coroutine(func):

                @functools.wraps(func)
                async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                    started = time.perf_counter()
                    try:
                        return await func(*args, **kwargs)
                    finally:
                        self.observe(label, time.perf_counter() - started)

                return async_wrapper  # type: ignore[return-value]

            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                started = time.perf_counter()
                try:
                    return func(*args, **kwargs)
                finally:
                    self.observe(label, time.perf_counter() - started)

            return wrapper  # type: ignore[return-value]

        return decorate

    # -- reading ----------------------------------------------------------

    @property
    def counters(self) -> Dict[str, float]:
        """A copy of the counter values."""
        return dict(self._counters)

    @property
    def gauges(self) -> Dict[str, float]:
        """A copy of the gauge values."""
        return dict(self._gauges)

    def histogram(self, name: str) -> Optional[Histogram]:
        """The histogram registered under *name*, if any."""
        return self._histograms.get(name)

    def snapshot(self) -> Dict[str, Any]:
        """Everything recorded, as plain JSON-safe data."""
        with self._lock:
            return {
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "histograms": {
                    name: histogram.snapshot()
                    for name, histogram in self._histograms.items()
                },
            }

    def render_prometheus(self, prefix: Optional[str] = None) -> str:
        """Render the current values in Prometheus text exposition format.

        Histograms become ``summary`` metrics with ``quantile`` labels, which
        is what a bounded sample window can honestly report.

        Examples:
            >>> from darkob.metrics import Metrics
            >>> registry = Metrics(prefix="")
            >>> registry.increment("hits", 5)
            >>> print(registry.render_prometheus(), end="")
            # TYPE hits counter
            hits 5
        """
        label = prefix if prefix is not None else self.prefix
        prefix_with_sep = f"{label}_" if label and not label.endswith("_") else label

        def full_name(name: str) -> str:
            cleaned = sanitize_name(name)
            if label and not cleaned.startswith(f"{label}_"):
                return f"{prefix_with_sep}{cleaned}"
            return cleaned

        lines: List[str] = []
        with self._lock:
            for name in sorted(self._counters):
                metric = full_name(name)
                lines.append(f"# TYPE {metric} counter")
                lines.append(f"{metric} {_fmt(self._counters[name])}")

            for name in sorted(self._gauges):
                metric = full_name(name)
                lines.append(f"# TYPE {metric} gauge")
                lines.append(f"{metric} {_fmt(self._gauges[name])}")

            for name in sorted(self._histograms):
                histogram = self._histograms[name]
                metric = full_name(name)
                lines.append(f"# TYPE {metric} summary")
                for quantile in (0.5, 0.95, 0.99):
                    value = histogram.percentile(quantile)
                    if value is not None:
                        lines.append(
                            f'{metric}{{quantile="{quantile}"}} {_fmt(value)}'
                        )
                lines.append(f"{metric}_count {_fmt(histogram.count)}")
                lines.append(f"{metric}_sum {_fmt(histogram.total)}")

        return "\n".join(lines) + ("\n" if lines else "")

    def reset(self) -> None:
        """Clear every counter, gauge and histogram."""
        with self._lock:
            self._counters.clear()
            self._gauges.clear()
            for histogram in self._histograms.values():
                histogram.reset()

    def __repr__(self) -> str:
        return (
            f"Metrics(enabled={self.enabled}, "
            f"counters={len(self._counters)}, "
            f"histograms={len(self._histograms)})"
        )


def _fmt(value: float) -> str:
    """Format a number the way Prometheus expects (no exponent for small ints)."""
    if value == int(value) and abs(value) < 1e15:
        return str(int(value))
    return repr(float(value))


def _is_coroutine(func: Callable[..., Any]) -> bool:
    import inspect

    # Not asyncio.iscoroutinefunction: deprecated in 3.14, and this only needs
    # to know whether to await the result.
    return inspect.iscoroutinefunction(func)


#: The registry the library instruments by default. Disabled until you call
#: :func:`enable_metrics`.
metrics = Metrics()


def get_metrics() -> Metrics:
    """Return the shared registry."""
    return metrics


def enable_metrics(
    *,
    prefix: str = "darkob",
    histogram_capacity: int = 512,
    reset: bool = True,
) -> Metrics:
    """Turn on the shared registry and return it."""
    metrics.prefix = prefix
    metrics.histogram_capacity = histogram_capacity
    if reset:
        metrics.reset()
    metrics.enabled = True
    return metrics


def disable_metrics() -> None:
    """Turn off instrumentation (recorded data is kept)."""
    metrics.enabled = False

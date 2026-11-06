"""Tests for ``darkob.metrics``."""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from darkob.client.core.api import Api
from darkob.metrics import (
    Histogram,
    Metrics,
    disable_metrics,
    enable_metrics,
    get_metrics,
    metrics,
    sanitize_name,
)


@pytest.fixture
def registry():
    """Enable the shared registry for one test, then switch it back off."""
    enable_metrics()
    try:
        yield metrics
    finally:
        disable_metrics()
        metrics.reset()


# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------


def test_metrics_are_off_by_default():
    assert Metrics().enabled is False
    assert get_metrics() is metrics


def test_sanitize_name():
    assert sanitize_name("darkob.api.requests") == "darkob_api_requests"
    assert sanitize_name("orders-created") == "orders_created"
    assert sanitize_name("weird name!") == "weird_name_"


def test_counter_and_gauge():
    registry = Metrics()
    registry.increment("calls")
    registry.increment("calls", 4)
    registry.decrement("calls")
    registry.set("depth", 7)
    registry.adjust("depth", 3)

    assert registry.counters["calls"] == 4
    assert registry.gauges["depth"] == 10


def test_histogram_percentiles():
    histogram = Histogram(capacity=8)
    for value in (1, 2, 3, 4):
        histogram.observe(value)

    assert histogram.count == 4
    assert histogram.total == 10
    assert histogram.mean == pytest.approx(2.5)
    assert histogram.minimum == 1
    assert histogram.maximum == 4
    assert histogram.percentile(0.0) == 1
    assert histogram.percentile(0.5) == pytest.approx(2.5)
    assert histogram.percentile(1.0) == 4


def test_histogram_percentile_of_empty_is_none():
    assert Histogram().percentile(0.5) is None
    assert Histogram().mean is None


def test_histogram_memory_is_bounded():
    histogram = Histogram(capacity=2)
    for value in (1, 2, 3):
        histogram.observe(value)

    assert histogram.count == 3  # the total keeps counting
    assert histogram.percentile(0.5) == pytest.approx(2.5)  # window is 2, 3


def test_histogram_capacity_must_be_positive():
    with pytest.raises(ValueError):
        Histogram(capacity=0)


def test_timer_records_seconds():
    registry = Metrics()
    with registry.timer("work") as timer:
        assert timer is not None

    histogram = registry.histogram("work")
    assert histogram is not None
    assert histogram.count == 1
    assert histogram.total >= 0


def test_time_it_wraps_sync_and_async():
    registry = Metrics()

    @registry.time_it("sync")
    def sync_fn(value):
        return value * 2

    @registry.time_it("async")
    async def async_fn(value):
        return value + 1

    assert sync_fn(2) == 4
    assert registry.histogram("sync").count == 1

    import asyncio

    assert asyncio.run(async_fn(2)) == 3
    assert registry.histogram("async").count == 1


def test_snapshot_is_json_serialisable():
    registry = Metrics()
    registry.increment("a")
    registry.set("b", 2)
    registry.observe("c", 0.5)

    snapshot = registry.snapshot()

    assert snapshot["counters"]["a"] == 1
    assert snapshot["gauges"]["b"] == 2
    assert snapshot["histograms"]["c"]["count"] == 1
    json.dumps(snapshot)


def test_prometheus_exposition():
    registry = Metrics()
    registry.increment("darkob.api.requests", 3)
    registry.set("darkob.queue.pending", 0)
    registry.observe("darkob.api.seconds", 0.25)

    text = registry.render_prometheus()

    assert "# TYPE darkob_api_requests counter" in text
    assert "darkob_api_requests 3" in text
    assert "# TYPE darkob_queue_pending gauge" in text
    assert "# TYPE darkob_api_seconds summary" in text
    assert 'darkob_api_seconds{quantile="0.5"}' in text
    assert "darkob_api_seconds_count 1" in text
    assert "darkob_api_seconds_sum 0.25" in text


def test_prometheus_prefix_is_not_applied_twice():
    registry = Metrics()
    registry.increment("darkob.api.requests")
    registry.increment("orders.created")

    text = registry.render_prometheus()

    assert "darkob_api_requests 1" in text
    assert "darkob_orders_created 1" in text
    assert "darkob_darkob" not in text


def test_prometheus_prefix_can_be_changed():
    registry = Metrics(prefix="myapp")
    registry.increment("orders.created")

    assert "myapp_orders_created 1" in registry.render_prometheus()


def test_reset_clears_everything():
    registry = Metrics()
    registry.increment("a")
    registry.set("b", 1)
    registry.observe("c", 1.0)

    registry.reset()

    assert registry.counters == {}
    assert registry.gauges == {}
    assert registry.histogram("c").count == 0


def test_enable_and_disable_toggle_the_shared_registry():
    enable_metrics()
    assert metrics.enabled is True
    disable_metrics()
    assert metrics.enabled is False


# ---------------------------------------------------------------------------
# Client instrumentation
# ---------------------------------------------------------------------------


def make_client(**overrides):
    base = dict(
        DEFAULT_PLATFORM={"platform": "PWA"},
        _original_platform="pwa",
        user_agent="test",
        max_retries=1,
        timeout=5,
        verify_ssl=False,
        proxy=None,
        stop_on_first_match=False,
        handlers={},
        flood_sleep_threshold=0,
    )
    base.update(overrides)
    return SimpleNamespace(**base)


def wire(api: Api, count: int = 1) -> None:
    api.api_map = {str(i): f"https://dc{i}.test/" for i in range(count)}
    api.api_priority = [str(i) for i in range(count)]
    api.api_url = "https://dc0.test/"
    api._api_code_by_url = {f"https://dc{i}.test": str(i) for i in range(count)}


class FakeResponse:
    def __init__(self, status=200, payload=None, headers=None):
        self.status = status
        self._payload = payload
        self.headers = headers or {}

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        return False

    def raise_for_status(self):
        if self.status >= 400:
            raise RuntimeError(f"HTTP {self.status}")

    async def json(self):
        return self._payload


class FakeSession:
    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = []

    def post(self, url, json=None, proxy=None):
        self.calls.append((url, json))
        return FakeResponse(*self._responses.pop(0))


async def _request(api: Api, responses, retries: int = 1):
    real = api.session
    api.session = FakeSession(responses)
    try:
        return await api._http_request({"method": "getMe"}, max_retries=retries)
    finally:
        await real.close()


async def test_requests_and_latency_are_recorded(registry):
    api = Api(make_client())
    wire(api)

    await _request(api, [(200, {"status": "OK"})])

    assert registry.counters["darkob.api.requests"] == 1
    assert registry.histogram("darkob.api.seconds").count == 1


async def test_errors_and_retries_are_recorded(registry):
    api = Api(make_client())
    wire(api)

    await _request(api, [(500, None), (200, {"status": "OK"})], retries=2)

    assert registry.counters["darkob.api.requests"] == 1
    assert registry.counters["darkob.api.errors"] == 1
    assert registry.counters["darkob.api.retries"] == 1


async def test_throttles_are_recorded(registry):
    api = Api(make_client())
    wire(api)

    await _request(api, [(429, None), (200, {"status": "OK"})], retries=2)

    assert registry.counters["darkob.api.ratelimited"] == 1


async def test_metrics_off_means_nothing_is_recorded():
    disable_metrics()
    api = Api(make_client())
    wire(api)

    await _request(api, [(200, {"status": "OK"})])

    assert metrics.counters.get("darkob.api.requests") is None


# ---------------------------------------------------------------------------
# Dispatch instrumentation
# ---------------------------------------------------------------------------


class CountingHandler:
    __name__ = "NewMessage"

    def __init__(self, matched: bool = True) -> None:
        self.matched = matched
        self.calls = 0

    async def __call__(self, *, event):
        self.calls += 1
        return self.matched


def dispatch_client(handler):
    async def on_message(event):
        return None

    return SimpleNamespace(
        DEFAULT_PLATFORM={"platform": "PWA"},
        _original_platform="pwa",
        user_agent="test",
        max_retries=1,
        timeout=5,
        verify_ssl=False,
        proxy=None,
        stop_on_first_match=True,
        handlers={on_message: handler},
        _conversations=None,
        plugin_manager=None,
    )


async def test_updates_and_handler_calls_are_recorded(registry):
    client = dispatch_client(CountingHandler())
    api = Api(client)
    real = api.session
    try:
        await api.handle_update("new_message", {"text": "hi"})
    finally:
        await real.close()

    assert registry.counters["darkob.updates"] == 1
    assert registry.counters["darkob.handlers.called"] == 1
    assert registry.histogram("darkob.update.seconds").count == 1


async def test_skipped_handlers_are_recorded(registry):
    client = dispatch_client(CountingHandler(matched=False))
    api = Api(client)
    real = api.session
    try:
        await api.handle_update("new_message", {"text": "hi"})
    finally:
        await real.close()

    assert registry.counters["darkob.handlers.skipped"] == 1
    assert "darkob.handlers.called" not in registry.counters


async def test_handler_errors_are_recorded(registry):
    class Exploding(CountingHandler):
        async def __call__(self, *, event):
            raise ValueError("boom")

    client = dispatch_client(Exploding())
    api = Api(client)
    real = api.session
    try:
        await api.handle_update("new_message", {"text": "hi"})
    finally:
        await real.close()

    assert registry.counters["darkob.handlers.errors"] == 1


# ---------------------------------------------------------------------------
# SendQueue depth
# ---------------------------------------------------------------------------


class _OfflineBot:
    """A bot whose sends always fail with a transient error."""

    async def send_message(self, *args, **kwargs):
        raise OSError("network is down")


async def test_sendqueue_publishes_its_depth(registry):
    from darkob.queue import SendQueue

    queue = SendQueue(_OfflineBot())

    await queue.put("chat", "hello")

    assert registry.gauges["darkob.queue.pending"] == 1

    queue.drain()

    assert registry.gauges["darkob.queue.pending"] == 0


async def test_sendqueue_does_not_touch_metrics_when_disabled():
    from darkob.queue import SendQueue

    disable_metrics()
    queue = SendQueue(_OfflineBot())

    await queue.put("chat", "hello")

    assert "darkob.queue.pending" not in metrics.gauges

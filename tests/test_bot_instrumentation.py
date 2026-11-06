"""The Bot API surface is the front door, so prove it is actually wired.

Everything added in 0.18 was first attached to the *userbot* request path
(`darkob.client.core.api`). `Bot` turned out to have a completely separate
request path and dispatch loop, so metrics, plugin hooks and the adaptive rate
limiter silently did nothing on the surface most people use. These tests exist
to stop that happening again: they assert behaviour on `Bot`, not on the
internal helper that happens to be easy to test.
"""

from __future__ import annotations

import json

import pytest

from darkob import AdaptiveRateLimiter, Bot
from darkob.bot.filters import Text
from darkob.metrics import disable_metrics, enable_metrics, metrics
from darkob.plugin import Plugin, PluginManager, PluginMeta
from darkob.testing import make_message

from conftest import VALID_TOKEN


@pytest.fixture
def registry():
    """Enable the shared metrics registry for one test."""
    enable_metrics()
    try:
        yield metrics
    finally:
        disable_metrics()
        metrics.reset()


# ---------------------------------------------------------------------------
# Transport doubles
# ---------------------------------------------------------------------------


class FakeResp:
    def __init__(self, status: int = 200, payload=None, headers=None) -> None:
        self.status = status
        self._payload = payload
        self.headers = headers or {}

    async def __aenter__(self) -> "FakeResp":
        return self

    async def __aexit__(self, *exc_info) -> bool:
        return False

    async def text(self) -> str:
        return json.dumps({} if self._payload is None else self._payload)


class FakeSess:
    def __init__(self, responses) -> None:
        self._responses = list(responses)
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        item = self._responses.pop(0)
        if isinstance(item, BaseException):
            raise item
        return item


def attach(bot: Bot, *responses) -> FakeSess:
    session = FakeSess(list(responses))

    async def _get_session():
        return session

    bot._get_session = _get_session  # type: ignore[method-assign]
    return session


def make_bot(**kwargs) -> Bot:
    return Bot(token=VALID_TOKEN, show_welcome=False, **kwargs)


# ---------------------------------------------------------------------------
# Adaptive rate limiting on the Bot surface
# ---------------------------------------------------------------------------


async def test_bot_429_halves_an_adaptive_limiter():
    limiter = AdaptiveRateLimiter(rate=20)
    bot = make_bot(rate_limiter=limiter, max_retries=1)
    attach(bot, FakeResp(429))

    with pytest.raises(Exception):
        await bot.request("POST", "getMe", json={})

    assert limiter.current_rate == 10.0


async def test_bot_too_requests_halves_an_adaptive_limiter():
    limiter = AdaptiveRateLimiter(rate=20)
    bot = make_bot(rate_limiter=limiter, max_retries=1)
    attach(bot, FakeResp(200, {"status": "TOO_REQUESTS"}))

    with pytest.raises(Exception):
        await bot.request("POST", "getMe", json={})

    assert limiter.current_rate == 10.0


async def test_bot_honours_retry_after():
    limiter = AdaptiveRateLimiter(rate=20)
    bot = make_bot(rate_limiter=limiter, max_retries=1)
    attach(bot, FakeResp(429, headers={"Retry-After": "9"}))

    with pytest.raises(Exception):
        await bot.request("POST", "getMe", json={})

    assert limiter.blocked_for == pytest.approx(9.0, abs=0.5)


async def test_bot_success_raises_the_rate_again():
    state = {"now": 0.0}
    limiter = AdaptiveRateLimiter(
        rate=20, increase_interval=1.0, clock=lambda: state["now"]
    )
    limiter.on_throttle()
    assert limiter.current_rate == 10.0
    state["now"] += 5.0

    bot = make_bot(rate_limiter=limiter, max_retries=1)
    attach(bot, FakeResp(200, {"status": "OK"}))

    await bot.request("POST", "getMe", json={})

    assert limiter.current_rate > 10.0


async def test_a_plain_limiter_is_unaffected():
    from darkob import RateLimiter

    limiter = RateLimiter(rate=20)
    bot = make_bot(rate_limiter=limiter, max_retries=1)
    attach(bot, FakeResp(429))

    with pytest.raises(Exception):
        await bot.request("POST", "getMe", json={})

    assert limiter.current_rate == 20.0


# ---------------------------------------------------------------------------
# Metrics on the Bot surface
# ---------------------------------------------------------------------------


async def test_bot_requests_are_counted(registry):
    bot = make_bot(max_retries=1)
    attach(bot, FakeResp(200, {"status": "OK"}))

    await bot.request("POST", "getMe", json={})

    assert registry.counters["darkob.api.requests"] == 1
    assert registry.histogram("darkob.api.seconds").count == 1


async def test_bot_throttles_are_counted(registry):
    bot = make_bot(max_retries=1)
    attach(bot, FakeResp(429))

    with pytest.raises(Exception):
        await bot.request("POST", "getMe", json={})

    assert registry.counters["darkob.api.ratelimited"] == 1


async def test_bot_updates_are_counted(registry):
    bot = make_bot()

    await bot._safe_feed(make_message("hi"))

    assert registry.counters["darkob.updates"] == 1
    assert registry.histogram("darkob.update.seconds").count == 1


async def test_metrics_off_records_nothing():
    disable_metrics()
    bot = make_bot(max_retries=1)
    attach(bot, FakeResp(200, {"status": "OK"}))

    await bot.request("POST", "getMe", json={})

    assert "darkob.api.requests" not in metrics.counters


# ---------------------------------------------------------------------------
# Handler counters
# ---------------------------------------------------------------------------


async def test_handler_counters_are_recorded(registry):
    bot = make_bot()
    seen = []

    async def handler(_bot, event):
        seen.append(event)

    bot._registry.store(handler, Text("does-not-match"))
    bot._registry.store(handler)

    await bot._safe_feed(make_message("hi"))

    assert registry.counters["darkob.handlers.skipped"] == 1
    assert registry.counters["darkob.handlers.called"] == 1
    assert len(seen) == 1


# ---------------------------------------------------------------------------
# Plugin hooks on the Bot surface
# ---------------------------------------------------------------------------


class Recorder(Plugin):
    meta = PluginMeta(name="recorder")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates = []
        self.before = []
        self.after = []
        self.consume = False

    async def on_update(self, event):
        self.updates.append(event)
        return True if self.consume else None

    async def before_request(self, action, data):
        self.before.append(action)
        return {"method": action, "rewritten": True}

    async def after_response(self, action, data):
        self.after.append(action)
        return {"status": "OK", "rewritten": True}


async def enable(bot: Bot, plugin_class=Recorder) -> PluginManager:
    manager = PluginManager(bot, auto_discover=False, plugins_dir=None)
    identifier = manager.register_plugin(plugin_class)
    await manager.enable(identifier)
    bot.plugin_manager = manager
    return manager


async def test_bot_before_request_rewrites_the_body():
    bot = make_bot(max_retries=1)
    await enable(bot)
    session = attach(bot, FakeResp(200, {"status": "OK"}))

    await bot.request("POST", "sendMessage", json={"method": "sendMessage"})

    assert session.calls[0][2]["json"] == {"method": "sendMessage", "rewritten": True}


async def test_bot_after_response_rewrites_the_payload():
    bot = make_bot(max_retries=1)
    await enable(bot)
    attach(bot, FakeResp(200, {"status": "OK"}))

    result = await bot.request("POST", "getMe", json={})

    assert result["rewritten"] is True


async def test_a_consuming_plugin_stops_bot_dispatch():
    bot = make_bot()
    manager = await enable(bot)
    manager.get_plugin("recorder").consume = True
    fired = []

    async def handler(_bot, event):
        fired.append(event)

    bot._registry.store(handler)

    await bot._safe_feed(make_message("hi"))

    assert fired == []


async def test_a_non_consuming_plugin_lets_bot_dispatch_continue():
    bot = make_bot()
    manager = await enable(bot)
    fired = []

    async def handler(_bot, event):
        fired.append(event)

    bot._registry.store(handler)

    await bot._safe_feed(make_message("hi"))

    assert len(fired) == 1
    assert len(manager.get_plugin("recorder").updates) == 1


async def test_a_bot_without_plugins_still_dispatches():
    bot = make_bot()
    fired = []

    async def handler(_bot, event):
        fired.append(event)

    bot._registry.store(handler)

    await bot._safe_feed(make_message("hi"))

    assert len(fired) == 1

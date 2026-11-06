"""Tests for AIMD adaptive rate limiting (``AdaptiveRateLimiter``)."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from darkob import AdaptiveRateLimiter, Bot, RateLimiter
from darkob.client.core.api import Api

from conftest import VALID_TOKEN


def make_clock(start: float = 0.0):
    state = {"now": start}
    return state, lambda: state["now"]


# ---------------------------------------------------------------------------
# Off by default
# ---------------------------------------------------------------------------


def test_plain_limiter_is_not_adaptive():
    limiter = RateLimiter(rate=20)

    assert limiter.adaptive is False
    assert limiter.current_rate == 20.0


def test_plain_limiter_ignores_throttle_reports():
    limiter = RateLimiter(rate=20)

    assert limiter.on_throttle() == 20.0
    limiter.on_success()
    assert limiter.current_rate == 20.0


def test_adaptive_limiter_is_a_rate_limiter():
    assert isinstance(AdaptiveRateLimiter(rate=20), RateLimiter)


def test_adaptive_limiter_switches_the_flag_on():
    limiter = RateLimiter(rate=20, adaptive=True)

    assert limiter.adaptive is True
    assert limiter.on_throttle() == 10.0


# ---------------------------------------------------------------------------
# Multiplicative decrease
# ---------------------------------------------------------------------------


def test_throttle_halves_the_rate_and_the_bucket():
    _, clock = make_clock()
    limiter = AdaptiveRateLimiter(rate=20, clock=clock)

    assert limiter.on_throttle() == 10.0
    assert limiter.current_rate == 10.0
    assert limiter._global.rate == 10.0


def test_repeated_throttles_floor_at_min_rate():
    _, clock = make_clock()
    limiter = AdaptiveRateLimiter(rate=20, min_rate=5, clock=clock)

    for _ in range(10):
        limiter.on_throttle()

    assert limiter.current_rate == 5.0
    assert limiter._global.rate == 5.0


def test_decrease_factor_is_configurable():
    _, clock = make_clock()
    limiter = AdaptiveRateLimiter(rate=20, decrease_factor=0.25, clock=clock)

    assert limiter.on_throttle() == 5.0


# ---------------------------------------------------------------------------
# Additive increase
# ---------------------------------------------------------------------------


def test_success_grows_the_rate_only_after_the_interval():
    state, clock = make_clock()
    limiter = AdaptiveRateLimiter(
        rate=20,
        min_rate=1,
        increase_step=2,
        increase_interval=1.0,
        clock=clock,
    )
    limiter.on_throttle()  # 20 -> 10
    assert limiter.current_rate == 10.0

    limiter.on_success()  # no time has passed yet
    assert limiter.current_rate == 10.0

    state["now"] += 1.0
    limiter.on_success()
    assert limiter.current_rate == 12.0

    limiter.on_success()  # same interval again: no growth
    assert limiter.current_rate == 12.0

    state["now"] += 1.0
    limiter.on_success()
    assert limiter.current_rate == 14.0


def test_recovery_never_exceeds_the_configured_rate():
    state, clock = make_clock()
    limiter = AdaptiveRateLimiter(
        rate=20, min_rate=1, increase_step=5, increase_interval=0.5, clock=clock
    )
    limiter.on_throttle()

    for _ in range(50):
        state["now"] += 1.0
        limiter.on_success()

    assert limiter.current_rate == 20.0
    assert limiter._global.rate == 20.0


def test_a_throttle_resets_the_recovery_timer():
    state, clock = make_clock()
    limiter = AdaptiveRateLimiter(
        rate=20, increase_step=1, increase_interval=1.0, clock=clock
    )
    state["now"] += 5.0
    limiter.on_throttle()  # -> 10, timer restarts here

    limiter.on_success()
    assert limiter.current_rate == 10.0


# ---------------------------------------------------------------------------
# Retry-After
# ---------------------------------------------------------------------------


def test_retry_after_blocks_acquisition():
    state, clock = make_clock()
    limiter = AdaptiveRateLimiter(rate=20, clock=clock)

    limiter.on_throttle(retry_after=5)

    assert limiter.blocked_for == 5.0
    state["now"] += 5.0
    assert limiter.blocked_for == 0.0


def test_retry_after_is_capped_by_max_block():
    _, clock = make_clock()
    limiter = AdaptiveRateLimiter(rate=20, max_block=10, clock=clock)

    limiter.on_throttle(retry_after=9999)

    assert limiter.blocked_for == 10.0


def test_zero_or_negative_retry_after_is_ignored():
    _, clock = make_clock()
    limiter = AdaptiveRateLimiter(rate=20, clock=clock)

    limiter.on_throttle(retry_after=0)
    limiter.on_throttle(retry_after=-5)

    assert limiter.blocked_for == 0.0


# ---------------------------------------------------------------------------
# Per-chat buckets follow the global rate
# ---------------------------------------------------------------------------


def test_per_chat_bucket_scales_with_the_global_rate():
    _, clock = make_clock()
    limiter = AdaptiveRateLimiter(rate=20, per_chat_rate=4, clock=clock)

    assert limiter.for_chat("g1").rate == pytest.approx(4.0)

    limiter.on_throttle()  # global 20 -> 10, so the per-chat share halves

    assert limiter.for_chat("g1").rate == pytest.approx(2.0)


# ---------------------------------------------------------------------------
# Introspection
# ---------------------------------------------------------------------------


def test_stats_reports_the_control_loop():
    state, clock = make_clock()
    limiter = AdaptiveRateLimiter(rate=20, clock=clock)
    limiter.on_throttle(retry_after=2)
    state["now"] += 3.0
    limiter.on_success()

    stats = limiter.stats()

    assert stats["adaptive"] is True
    assert stats["rate"] == 20.0
    assert stats["current_rate"] >= 10.0
    assert stats["throttles"] == 1
    assert stats["acquired"] == 1
    assert stats["blocked_for"] == 0.0


def test_reset_restores_the_configured_rate():
    _, clock = make_clock()
    limiter = AdaptiveRateLimiter(rate=20, clock=clock)
    limiter.on_throttle(retry_after=5)

    limiter.reset()

    assert limiter.current_rate == 20.0
    assert limiter.blocked_for == 0.0
    assert limiter.stats()["throttles"] == 0


def test_repr_shows_the_live_rate():
    _, clock = make_clock()
    limiter = AdaptiveRateLimiter(rate=20, clock=clock)
    limiter.on_throttle()

    assert "adaptive=True" in repr(limiter)
    assert "current=10.00" in repr(limiter)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "kwargs",
    [
        {"rate": 0},
        {"rate": -1},
        {"rate": 20, "min_rate": 0},
        {"rate": 20, "min_rate": 30},
        {"rate": 20, "decrease_factor": 1.0},
        {"rate": 20, "decrease_factor": 0.0},
        {"rate": 20, "increase_step": 0},
        {"rate": 20, "increase_interval": 0},
    ],
)
def test_invalid_configuration_is_rejected(kwargs):
    with pytest.raises(ValueError):
        AdaptiveRateLimiter(**kwargs)


# ---------------------------------------------------------------------------
# Client integration
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


async def test_client_lowers_the_rate_on_a_429():
    limiter = AdaptiveRateLimiter(rate=20)
    api = Api(make_client(rate_limiter=limiter))
    wire(api)
    real = api.session
    api.session = FakeSession([(429, None, {"Retry-After": "7"}), (200, {"status": "OK"})])

    try:
        await api._http_request({"method": "getMe"}, max_retries=2)
    finally:
        await real.close()

    assert limiter.current_rate == 10.0
    assert limiter.stats()["throttles"] == 1


async def test_client_reads_retry_after_from_the_header():
    limiter = AdaptiveRateLimiter(rate=20)
    api = Api(make_client(rate_limiter=limiter))
    wire(api)
    real = api.session
    api.session = FakeSession([(429, None, {"Retry-After": "12"}), (200, {"status": "OK"})])

    try:
        await api._http_request({"method": "getMe"}, max_retries=2)
    finally:
        await real.close()

    assert limiter.blocked_for == pytest.approx(12.0, abs=0.5)


async def test_client_raises_the_rate_again_after_success():
    state, clock = make_clock()
    limiter = AdaptiveRateLimiter(rate=20, increase_interval=1.0, clock=clock)
    limiter.on_throttle()
    assert limiter.current_rate == 10.0
    state["now"] += 5.0  # a clean stretch of traffic

    api = Api(make_client(rate_limiter=limiter))
    wire(api)
    real = api.session
    api.session = FakeSession([(200, {"status": "OK"})])

    try:
        await api._http_request({"method": "getMe"}, max_retries=1)
    finally:
        await real.close()

    assert limiter.current_rate > 10.0


async def test_a_plain_limiter_is_untouched_by_a_429():
    limiter = RateLimiter(rate=20)
    api = Api(make_client(rate_limiter=limiter))
    wire(api)
    real = api.session
    api.session = FakeSession([(429, None, {}), (200, {"status": "OK"})])

    try:
        await api._http_request({"method": "getMe"}, max_retries=2)
    finally:
        await real.close()

    assert limiter.current_rate == 20.0


# ---------------------------------------------------------------------------
# The public Bot surface still accepts either limiter
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "limiter",
    [RateLimiter(rate=20), AdaptiveRateLimiter(rate=20)],
)
def test_bot_accepts_both_limiters(limiter):
    bot = Bot(token=VALID_TOKEN, show_welcome=False, rate_limiter=limiter)

    assert bot.rate_limiter is limiter

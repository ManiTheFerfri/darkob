"""Tests for the token bucket and the rate limiter."""

from __future__ import annotations

import asyncio

import pytest

from darkob import Bot, RateLimiter, TokenBucket

from conftest import VALID_TOKEN, FakeResponse, attach


def make_clock(start: float = 0.0):
    state = {"now": start}
    return state, lambda: state["now"]


# ---------------------------------------------------------------------------
# TokenBucket
# ---------------------------------------------------------------------------


def test_bucket_starts_full():
    bucket = TokenBucket(rate=10, capacity=5)

    assert bucket.tokens == 5


def test_try_acquire_consumes_a_token():
    bucket = TokenBucket(rate=10, capacity=5)

    assert bucket.try_acquire() is True
    assert bucket.tokens == pytest.approx(4, abs=0.05)


def test_try_acquire_fails_when_empty():
    bucket = TokenBucket(rate=1, capacity=1)

    assert bucket.try_acquire() is True
    assert bucket.try_acquire() is False


def test_tokens_refill_over_time():
    state, clock = make_clock()
    bucket = TokenBucket(rate=2.0, capacity=10, clock=clock)

    bucket.try_acquire(10)
    assert bucket.tokens == 0

    state["now"] = 3.0
    assert bucket.tokens == 6


def test_refill_is_capped_at_capacity():
    state, clock = make_clock()
    bucket = TokenBucket(rate=100.0, capacity=5, clock=clock)

    state["now"] = 1000.0

    assert bucket.tokens == 5


async def test_acquire_waits_until_a_token_is_available(monkeypatch):
    state, clock = make_clock()
    bucket = TokenBucket(rate=1.0, capacity=1, clock=clock)
    bucket.try_acquire()

    async def fake_sleep(delay):
        state["now"] += delay

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)

    await bucket.acquire()

    assert state["now"] >= 1.0
    assert bucket.tokens < 1


async def test_acquire_returns_immediately_when_a_token_exists():
    bucket = TokenBucket(rate=1.0, capacity=2)

    await asyncio.wait_for(bucket.acquire(), timeout=0.5)

    assert bucket.tokens == pytest.approx(1, abs=0.05)


async def test_acquire_rejects_more_than_capacity():
    bucket = TokenBucket(rate=1.0, capacity=2)

    with pytest.raises(ValueError):
        await bucket.acquire(5)


@pytest.mark.parametrize("kwargs", [{"rate": 0}, {"rate": -1}, {"rate": 1, "capacity": 0}])
def test_invalid_configuration_is_rejected(kwargs):
    with pytest.raises(ValueError):
        TokenBucket(**kwargs)


# ---------------------------------------------------------------------------
# RateLimiter
# ---------------------------------------------------------------------------


def test_per_chat_buckets_are_isolated():
    limiter = RateLimiter(rate=10, per_chat_rate=1)

    first = limiter.for_chat("a")
    second = limiter.for_chat("b")

    assert first is not second
    assert limiter.for_chat("a") is first


def test_per_chat_buckets_are_bounded():
    limiter = RateLimiter(rate=10, per_chat_rate=1, max_buckets=2)

    limiter.for_chat("a")
    limiter.for_chat("b")
    limiter.for_chat("c")

    assert len(limiter._chats) == 2
    assert "a" not in limiter._chats


async def test_without_per_chat_rate_only_the_global_bucket_is_used():
    limiter = RateLimiter(rate=100, burst=100)

    await limiter.acquire("a")

    assert limiter._chats == {}


async def test_acquire_uses_a_chat_bucket_when_configured(monkeypatch):
    limiter = RateLimiter(rate=100, burst=100, per_chat_rate=1, per_chat_burst=1)
    calls = []

    original = TokenBucket.acquire

    async def spy(self, tokens=1.0):
        calls.append(self)
        await original(self, tokens)

    monkeypatch.setattr(TokenBucket, "acquire", spy)

    await limiter.acquire("chat-1")
    await limiter.acquire("chat-2")

    assert len(calls) == 4, "each call takes the chat bucket and the global one"
    assert calls[0] is limiter.for_chat("chat-1")
    assert calls[2] is limiter.for_chat("chat-2")
    assert calls[1] is calls[3], "the global bucket is shared"


# ---------------------------------------------------------------------------
# Bot integration
# ---------------------------------------------------------------------------


class RecordingLimiter:
    def __init__(self):
        self.keys = []

    async def acquire(self, chat_id=None):
        self.keys.append(chat_id)


async def test_bot_request_acquires_from_the_limiter():
    limiter = RecordingLimiter()
    bot = Bot(token=VALID_TOKEN, show_welcome=False, rate_limiter=limiter)
    attach(bot, FakeResponse(200, {"status": "OK"}))

    await bot.request("POST", "sendMessage", json={"chat_id": "g0abc", "text": "hi"})

    assert limiter.keys == ["g0abc"]


async def test_bot_without_a_limiter_works_normally():
    bot = Bot(token=VALID_TOKEN, show_welcome=False)
    attach(bot, FakeResponse(200, {"status": "OK"}))

    result = await bot.request("POST", "getMe", json={})

    assert result["status"] == "OK"


async def test_limiter_is_applied_to_every_retry_attempt():
    limiter = RecordingLimiter()
    bot = Bot(
        token=VALID_TOKEN, show_welcome=False, max_retries=3, rate_limiter=limiter
    )
    attach(
        bot,
        FakeResponse(502, text="down"),
        FakeResponse(200, {"status": "OK"}),
    )

    await bot.request("POST", "getMe", json={})

    assert len(limiter.keys) == 2

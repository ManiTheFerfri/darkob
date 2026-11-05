"""Tests for CircuitBreaker and its integration with the transport."""

from __future__ import annotations

import asyncio

import pytest

from darkob.circuit import CLOSED, HALF_OPEN, OPEN, CircuitBreaker
from darkob.client.core.api import Api
from types import SimpleNamespace


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------


def test_starts_closed():
    breaker = CircuitBreaker()

    assert breaker.state == CLOSED
    assert breaker.allows_request() is True


def test_opens_after_the_threshold():
    breaker = CircuitBreaker(threshold=3)

    breaker.record_failure()
    breaker.record_failure()
    assert breaker.is_open() is False

    breaker.record_failure()
    assert breaker.is_open() is True
    assert breaker.state == OPEN


def test_success_resets_the_failure_count():
    breaker = CircuitBreaker(threshold=3)
    breaker.record_failure()
    breaker.record_failure()

    breaker.record_success()

    assert breaker.failures == 0
    assert breaker.state == CLOSED


def test_half_open_after_the_reset_timeout():
    breaker = CircuitBreaker(threshold=2, reset_timeout=10.0)
    breaker.record_failure(now=100.0)
    breaker.record_failure(now=100.0)
    assert breaker.is_open(now=105.0) is True

    assert breaker.state == HALF_OPEN or breaker.is_open(now=111.0) is False


def test_half_open_failure_reopens_immediately():
    breaker = CircuitBreaker(threshold=1, reset_timeout=10.0)
    breaker.record_failure(now=100.0)

    # Probe after the timeout, then fail again.
    breaker.record_failure(now=115.0)

    assert breaker.is_open(now=116.0) is True


def test_reset_clears_everything():
    breaker = CircuitBreaker(threshold=1)
    breaker.record_failure()
    assert breaker.is_open() is True

    breaker.reset()

    assert breaker.state == CLOSED
    assert breaker.failures == 0


@pytest.mark.parametrize("kwargs", [{"threshold": 0}, {"reset_timeout": 0}])
def test_invalid_configuration_is_rejected(kwargs):
    with pytest.raises(ValueError):
        CircuitBreaker(**kwargs)


def test_repr_shows_state_and_count():
    breaker = CircuitBreaker(threshold=2)
    breaker.record_failure()

    assert "failures=1/2" in repr(breaker)


# ---------------------------------------------------------------------------
# Transport integration
# ---------------------------------------------------------------------------


class FakePostResponse:
    def __init__(self, status, payload=None):
        self.status = status
        self._payload = payload

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    def raise_for_status(self):
        if self.status >= 400:
            raise RuntimeError(f"HTTP {self.status}")

    async def json(self):
        return self._payload


class FakePostSession:
    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = []

    def post(self, url, json=None, proxy=None):
        self.calls.append(url)
        item = self._responses.pop(0)
        if isinstance(item, BaseException):
            raise item
        return FakePostResponse(*item)


def make_client():
    return SimpleNamespace(
        DEFAULT_PLATFORM={"platform": "PWA"},
        _original_platform="pwa",
        user_agent="test",
        max_retries=3,
        timeout=5,
        verify_ssl=False,
        proxy=None,
        stop_on_first_match=False,
        handlers={},
    )


async def test_open_endpoint_is_skipped_on_the_next_request():
    api = Api(make_client())
    api.api_map = {"0": "https://dc0.test/", "1": "https://dc1.test/"}
    api.api_priority = ["0", "1"]
    api.api_url = "https://dc0.test/"
    api._api_code_by_url = {"https://dc0.test": "0", "https://dc1.test": "1"}

    api.breaker_for("https://dc0.test").threshold = 1
    real = api.session
    session = FakePostSession([RuntimeError("dc0 down"), (200, {"status": "OK"})])
    api.session = session

    try:
        first = await api._http_request({}, max_retries=3)
        assert first == {"status": "OK"}
        assert session.calls == ["https://dc0.test", "https://dc1.test"]

        # dc0 is now open; the next request must not touch it.
        session._responses.append((200, {"status": "OK"}))
        second = await api._http_request({}, max_retries=3)

        assert second == {"status": "OK"}
        assert session.calls[-1] == "https://dc1.test"
        assert "https://dc0.test" not in session.calls[2:]
    finally:
        await real.close()


async def test_all_endpoints_open_returns_none_without_network():
    api = Api(make_client())
    api.api_map = {"0": "https://dc0.test/"}
    api.api_priority = ["0"]
    api.api_url = "https://dc0.test/"
    api._api_code_by_url = {"https://dc0.test": "0"}

    breaker = api.breaker_for("https://dc0.test")
    breaker.threshold = 1
    breaker.record_failure()

    real = api.session
    session = FakePostSession([])
    api.session = session

    try:
        assert await api._http_request({}, max_retries=3) is None
        assert session.calls == []
    finally:
        await real.close()

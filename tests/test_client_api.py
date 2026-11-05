"""Tests for the client-side dispatch index and bounded retry policy."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import aiohttp
import pytest

from darkob.client.core.api import Api


def make_client(**overrides) -> SimpleNamespace:
    """Minimal stand-in for darkob.Client, sufficient to build an Api."""
    base = dict(
        DEFAULT_PLATFORM={"platform": "PWA"},
        _original_platform="pwa",
        user_agent="darkob-tests",
        max_retries=3,
        timeout=5,
        verify_ssl=False,
        proxy=None,
        stop_on_first_match=True,
        handlers={},
    )
    base.update(overrides)
    return SimpleNamespace(**base)


async def make_api(**overrides) -> Api:
    return Api(make_client(**overrides))


class FakePostResponse:
    def __init__(self, status: int, payload=None):
        self.status = status
        self._payload = payload

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        return False

    def raise_for_status(self):
        if self.status >= 400:
            raise aiohttp.ClientResponseError(
                request_info=None,
                history=(),
                status=self.status,
                message="error",
            )

    async def json(self):
        return self._payload


class FakePostSession:
    """Queues (status, payload) tuples or exceptions; records requested URLs."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = []
        self.closed = False

    def post(self, url, json=None, proxy=None):
        self.calls.append(url)
        if not self._responses:
            raise AssertionError("FakePostSession ran out of queued responses")
        item = self._responses.pop(0)
        if isinstance(item, BaseException):
            raise item
        return FakePostResponse(*item)

    async def close(self):
        self.closed = True


# ---------------------------------------------------------------------------
# Dispatch index
# ---------------------------------------------------------------------------


class MessageUpdates:
    __name__ = "MessageUpdates"

    def __init__(self, allow: bool = True):
        self.allow = allow

    async def __call__(self, event=None):
        return self.allow


class ChatUpdates:
    __name__ = "ChatUpdates"

    async def __call__(self, event=None):
        return True


async def test_only_handlers_for_the_update_name_run():
    api = await make_api()
    called = []

    async def on_message(event):
        called.append("message")

    async def on_chat(event):
        called.append("chat")

    api.client.handlers = {on_message: MessageUpdates(), on_chat: ChatUpdates()}

    try:
        await api.handle_update("message_updates", {"x": 1})
    finally:
        await api.close()

    assert called == ["message"]


async def test_index_is_built_once_and_reused():
    api = await make_api()

    async def handler(event):
        return None

    api.client.handlers = {handler: MessageUpdates()}

    try:
        await api.handle_update("message_updates", {"x": 1})
        first_index = api._dispatch_index
        assert first_index is not None

        await api.handle_update("message_updates", {"x": 2})
        assert api._dispatch_index is first_index, "index should be reused"
    finally:
        await api.close()


async def test_index_rebuilds_when_handlers_change():
    api = await make_api()

    async def handler(event):
        return None

    api.client.handlers = {handler: MessageUpdates()}

    try:
        await api.handle_update("message_updates", {"x": 1})
        first_index = api._dispatch_index

        async def second(event):
            return None

        api.client.handlers[second] = MessageUpdates()
        await api.handle_update("message_updates", {"x": 2})

        assert api._dispatch_index is not first_index
    finally:
        await api.close()


async def test_filtering_handler_blocks_execution():
    api = await make_api()
    called = []

    async def handler(event):
        called.append("ran")

    api.client.handlers = {handler: MessageUpdates(allow=False)}

    try:
        await api.handle_update("message_updates", {"x": 1})
    finally:
        await api.close()

    assert called == []


async def test_unknown_update_name_is_a_no_op():
    api = await make_api()
    called = []

    async def handler(event):
        called.append("ran")

    api.client.handlers = {handler: MessageUpdates()}

    try:
        await api.handle_update("something_else", {"x": 1})
    finally:
        await api.close()

    assert called == []


async def test_sync_handler_runs_to_completion():
    api = await make_api(stop_on_first_match=False)
    called = []

    def sync_handler(event):
        called.append("sync")

    api.client.handlers = {sync_handler: MessageUpdates()}

    try:
        await api.handle_update("message_updates", {"x": 1})
        # Backgrounded sync handler completes in the loop's executor.
        await asyncio.gather(*list(api._background_tasks))
    finally:
        await api.close()

    assert called == ["sync"]


# ---------------------------------------------------------------------------
# Bounded retry policy
# ---------------------------------------------------------------------------


def wire_endpoints(api: Api, count: int = 3) -> None:
    api.api_map = {str(i): f"https://dc{i}.test/" for i in range(count)}
    api.api_priority = [str(i) for i in range(count)]
    api.api_url = f"https://dc0.test/"
    api._api_code_by_url = {
        f"https://dc{i}.test": str(i) for i in range(count)
    }


async def test_attempts_are_bounded_not_multiplied_by_endpoints():
    """Three endpoints with max_retries=3 means 3 attempts, not 9."""
    api = await make_api()
    wire_endpoints(api, 3)
    real_session = api.session
    fake = FakePostSession([RuntimeError("boom")] * 3)
    api.session = fake

    try:
        result = await api._http_request({}, max_retries=3)
    finally:
        await real_session.close()

    assert result is None
    assert len(fake.calls) == 3, f"expected 3 attempts, got {len(fake.calls)}"


async def test_rotates_across_endpoints_before_repeating():
    api = await make_api()
    wire_endpoints(api, 3)
    real_session = api.session
    fake = FakePostSession([RuntimeError("boom")] * 3)
    api.session = fake

    try:
        await api._http_request({}, max_retries=3)
    finally:
        await real_session.close()

    assert len(set(fake.calls)) == 3, "each attempt should target a new endpoint"


async def test_too_requests_status_is_retried():
    api = await make_api()
    wire_endpoints(api, 1)
    real_session = api.session
    fake = FakePostSession(
        [(200, {"status": "TOO_REQUESTS"}), (200, {"status": "OK", "data": {}})]
    )
    api.session = fake

    try:
        result = await api._http_request({}, max_retries=3)
    finally:
        await real_session.close()

    assert result == {"status": "OK", "data": {}}
    assert len(fake.calls) == 2


async def test_http_429_is_retried():
    api = await make_api()
    wire_endpoints(api, 1)
    real_session = api.session
    fake = FakePostSession([(429, None), (200, {"status": "OK"})])
    api.session = fake

    try:
        result = await api._http_request({}, max_retries=3)
    finally:
        await real_session.close()

    assert result == {"status": "OK"}
    assert len(fake.calls) == 2


async def test_successful_endpoint_is_promoted():
    api = await make_api()
    wire_endpoints(api, 2)
    api.api_priority = ["0", "1"]
    real_session = api.session
    fake = FakePostSession([RuntimeError("boom"), (200, {"status": "OK"})])
    api.session = fake

    try:
        await api._http_request({}, max_retries=2)
    finally:
        await real_session.close()

    # Second attempt hit dc1; it should now be first in priority.
    assert api.api_priority[0] == "1"


async def test_no_endpoints_returns_none_without_raising():
    api = await make_api()
    try:
        assert await api._http_request({}, max_retries=2) is None
    finally:
        await api.close()


# ---------------------------------------------------------------------------
# Pooled auxiliary sessions (file servers)
# ---------------------------------------------------------------------------


async def test_aux_session_is_reused_for_the_same_host():
    api = await make_api()
    try:
        async with api.aux_session("https://file.test") as first:
            pass
        async with api.aux_session("https://file.test") as second:
            pass

        assert first is second, "same host should reuse the pooled session"
    finally:
        await api.close()


async def test_aux_sessions_are_separate_per_host():
    api = await make_api()
    try:
        async with api.aux_session("https://a.test") as first:
            pass
        async with api.aux_session("https://b.test") as second:
            pass

        assert first is not second
    finally:
        await api.close()


async def test_aux_sessions_are_closed_with_the_client():
    api = await make_api()
    async with api.aux_session("https://file.test") as pooled:
        pass

    await api.close()

    assert pooled.closed
    assert api._aux_sessions == {}


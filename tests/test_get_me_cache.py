"""Tests for the get_me caches."""

from __future__ import annotations

import time

from darkob import Bot
from darkob.client.users.get_me import GetMe as ClientGetMe

from conftest import VALID_TOKEN


def make_bot() -> Bot:
    return Bot(token=VALID_TOKEN, show_welcome=False)


# ---------------------------------------------------------------------------
# Bot
# ---------------------------------------------------------------------------


async def test_bot_get_me_is_cached():
    bot = make_bot()
    calls = []

    async def fake_request(method, endpoint, **kwargs):
        calls.append(endpoint)
        return {"data": {"bot": {"bot_id": "b0"}}}

    bot.request = fake_request

    first = await bot.get_me()
    second = await bot.get_me()

    assert first is second
    assert len(calls) == 1


async def test_bot_get_me_refresh_bypasses_the_cache():
    bot = make_bot()
    calls = []

    async def fake_request(method, endpoint, **kwargs):
        calls.append(endpoint)
        return {"data": {"bot": {"bot_id": "b0"}}}

    bot.request = fake_request

    await bot.get_me()
    await bot.get_me(refresh=True)

    assert len(calls) == 2


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------


class FakeClient(ClientGetMe):
    auth = "a" * 32
    private_key = "key"

    def __init__(self):
        self.calls = 0

    async def get_user_info(self):
        self.calls += 1
        return {"user": {"user_guid": "u0"}}


async def test_client_get_me_is_cached():
    client = FakeClient()

    first = await client.get_me()
    second = await client.get_me()

    assert first is second
    assert client.calls == 1


async def test_client_get_me_refresh_bypasses_the_cache():
    client = FakeClient()

    await client.get_me()
    await client.get_me(refresh=True)

    assert client.calls == 2


async def test_client_get_me_cache_expires_after_ttl():
    client = FakeClient()

    await client.get_me(ttl=300)
    client._me_cached_at = time.time() - 10_000
    await client.get_me(ttl=300)

    assert client.calls == 2


async def test_client_get_me_exposes_auth_and_private_key():
    client = FakeClient()

    payload = await client.get_me()

    assert payload["auth"] == "a" * 32
    assert payload["private_key"] == "key"

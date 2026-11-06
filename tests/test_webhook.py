"""Tests for webhook authentication and bounded update spawning."""

from __future__ import annotations

import asyncio


from darkob import Bot

from conftest import VALID_TOKEN


class FakeRequest:
    def __init__(self, payload=None, headers=None, query=None, invalid=False):
        self._payload = payload
        self._invalid = invalid
        self.headers = headers or {}
        self.query = query or {}

    async def json(self):
        if self._invalid:
            raise ValueError("not json")
        return self._payload


def make_bot(**kwargs) -> Bot:
    return Bot(token=VALID_TOKEN, show_welcome=False, **kwargs)


UPDATE_PAYLOAD = {"update": {"type": "NewMessage", "chat_id": "g0x"}}


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------


async def test_webhook_without_a_secret_accepts_requests():
    bot = make_bot()

    response = await bot._handle_webhook(FakeRequest(payload=UPDATE_PAYLOAD))

    assert response.status == 200


async def test_webhook_rejects_a_missing_secret():
    bot = make_bot(webhook_secret="s3cret")

    response = await bot._handle_webhook(FakeRequest(payload=UPDATE_PAYLOAD))

    assert response.status == 401


async def test_webhook_rejects_a_wrong_secret():
    bot = make_bot(webhook_secret="s3cret")

    response = await bot._handle_webhook(
        FakeRequest(payload=UPDATE_PAYLOAD, headers={"X-Webhook-Secret": "nope"})
    )

    assert response.status == 401


async def test_webhook_accepts_the_secret_header():
    bot = make_bot(webhook_secret="s3cret")

    response = await bot._handle_webhook(
        FakeRequest(payload=UPDATE_PAYLOAD, headers={"X-Webhook-Secret": "s3cret"})
    )

    assert response.status == 200


async def test_webhook_accepts_the_secret_query_parameter():
    bot = make_bot(webhook_secret="s3cret")

    response = await bot._handle_webhook(
        FakeRequest(payload=UPDATE_PAYLOAD, query={"secret": "s3cret"})
    )

    assert response.status == 200


async def test_webhook_rejects_an_inline_message_without_the_secret():
    bot = make_bot(webhook_secret="s3cret")

    response = await bot._handle_webhook(
        FakeRequest(payload={"inline_message": {"type": "InlineMessage"}})
    )

    assert response.status == 401


async def test_webhook_accepts_an_inline_message_with_the_secret():
    bot = make_bot(webhook_secret="s3cret")

    response = await bot._handle_webhook(
        FakeRequest(
            payload={"inline_message": {"type": "InlineMessage"}},
            headers={"X-Webhook-Secret": "s3cret"},
        )
    )

    assert response.status == 200


# ---------------------------------------------------------------------------
# Payload validation
# ---------------------------------------------------------------------------


async def test_webhook_rejects_invalid_json():
    bot = make_bot()

    response = await bot._handle_webhook(FakeRequest(invalid=True))

    assert response.status == 400


async def test_webhook_rejects_a_non_object_payload():
    bot = make_bot()

    response = await bot._handle_webhook(FakeRequest(payload=["not", "an", "object"]))

    assert response.status == 400


async def test_webhook_ignores_unknown_payloads_gracefully():
    bot = make_bot()

    response = await bot._handle_webhook(FakeRequest(payload={"something": 1}))

    assert response.status == 200


# ---------------------------------------------------------------------------
# Bounded spawning
# ---------------------------------------------------------------------------


async def test_spawn_update_runs_the_coroutine():
    bot = make_bot()
    seen = []

    async def work():
        seen.append("ran")

    bot._spawn_update(work())
    await asyncio.gather(*list(bot._update_tasks))

    assert seen == ["ran"]


async def test_spawn_update_caps_concurrency():
    bot = make_bot(max_concurrent_updates=2)
    running = {"now": 0, "peak": 0}
    gate = asyncio.Event()

    async def work():
        running["now"] += 1
        running["peak"] = max(running["peak"], running["now"])
        await gate.wait()
        running["now"] -= 1

    for _ in range(6):
        bot._spawn_update(work())

    await asyncio.sleep(0)
    assert running["peak"] <= 2, "the semaphore must bound concurrency"

    gate.set()
    await asyncio.gather(*list(bot._update_tasks))

    assert running["peak"] <= 2


async def test_spawn_update_tracks_and_releases_tasks():
    bot = make_bot()

    async def work():
        return None

    bot._spawn_update(work())
    assert len(bot._update_tasks) == 1

    await asyncio.sleep(0)
    await asyncio.gather(*list(bot._update_tasks))

    assert len(bot._update_tasks) == 0


def test_max_concurrent_updates_is_at_least_one():
    bot = Bot(token=VALID_TOKEN, show_welcome=False, max_concurrent_updates=0)

    assert bot.max_concurrent_updates == 1

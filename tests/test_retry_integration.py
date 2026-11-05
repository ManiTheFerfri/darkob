"""The Retry policy must actually drive the Bot request loop."""

from __future__ import annotations

import pytest

from darkob import Bot
from darkob.bot.exceptions import BadGateway
from darkob.retry import Retry

from conftest import VALID_TOKEN, FakeResponse, attach


def make_bot(retry: Retry) -> Bot:
    return Bot(token=VALID_TOKEN, show_welcome=False, max_retries=9, retry=retry)


async def test_policy_limits_the_number_of_attempts():
    bot = make_bot(Retry(attempts=2, backoff=0.0, jitter=0.0))
    session = attach(bot, FakeResponse(502, text="a"), FakeResponse(502, text="b"))

    with pytest.raises(BadGateway):
        await bot.request("POST", "getMe", json={})

    assert session.count == 2, "max_retries=9 must be overridden by the policy"


async def test_policy_allows_a_later_success():
    bot = make_bot(Retry(attempts=3, backoff=0.0, jitter=0.0))
    session = attach(
        bot,
        FakeResponse(502, text="a"),
        FakeResponse(200, {"status": "OK"}),
    )

    result = await bot.request("POST", "getMe", json={})

    assert result["status"] == "OK"
    assert session.count == 2


async def test_single_attempt_policy_does_not_retry():
    bot = make_bot(Retry.none())
    session = attach(bot, FakeResponse(502, text="a"))

    with pytest.raises(BadGateway):
        await bot.request("POST", "getMe", json={})

    assert session.count == 1


async def test_without_a_policy_max_retries_still_applies():
    bot = Bot(token=VALID_TOKEN, show_welcome=False, max_retries=2)
    session = attach(bot, FakeResponse(502, text="a"), FakeResponse(502, text="b"))

    with pytest.raises(BadGateway):
        await bot.request("POST", "getMe", json={})

    assert session.count == 2

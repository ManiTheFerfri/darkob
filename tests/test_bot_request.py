"""Tests for Bot.request: retry policy and API-status error mapping."""

from __future__ import annotations

import aiohttp
import pytest

from darkob.bot.exceptions import (
    APIException,
    BadGateway,
    InvalidAccess,
    JSONDecode,
    Network,
    TooRequests,
)

from conftest import FakeResponse, attach


async def test_ok_response_is_returned(bot):
    session = attach(
        bot, FakeResponse(200, {"status": "OK", "data": {"user_id": "u0abc"}})
    )

    result = await bot.request("POST", "getMe", json={})

    assert result["status"] == "OK"
    assert result["data"]["user_id"] == "u0abc"
    assert session.count == 1


async def test_url_is_base_url_plus_endpoint(bot):
    session = attach(bot, FakeResponse(200, {"status": "OK"}))

    await bot.request("POST", "getMe", json={})

    _, url, _ = session.requests[0]
    assert url == f"{bot.base_url}/getMe"


async def test_retries_on_bad_gateway_then_succeeds(bot):
    bot.max_retries = 3
    session = attach(
        bot,
        FakeResponse(502, text="upstream down"),
        FakeResponse(200, {"status": "OK", "data": {}}),
    )

    result = await bot.request("POST", "getMe", json={})

    assert result["status"] == "OK"
    assert session.count == 2, "should retry once after a 502"


async def test_bad_gateway_raises_after_exhausting_retries(bot):
    bot.max_retries = 2
    attach(bot, FakeResponse(502, text="a"), FakeResponse(502, text="b"))

    with pytest.raises(BadGateway):
        await bot.request("POST", "getMe", json={})


async def test_http_error_status_raises_api_exception_without_retry(bot):
    session = attach(bot, FakeResponse(404, text="not found"))

    with pytest.raises(APIException):
        await bot.request("POST", "getMe", json={})

    assert session.count == 1, "4xx must not be retried"


@pytest.mark.parametrize(
    "status,expected",
    [
        ("INVALID_ACCESS", InvalidAccess),
        ("TOO_REQUESTS", TooRequests),
    ],
)
async def test_api_status_maps_to_typed_exception(bot, status, expected):
    attach(bot, FakeResponse(200, {"status": status, "dev_message": "nope"}))

    with pytest.raises(expected):
        await bot.request("POST", "getMe", json={})


async def test_invalid_json_raises_jsondecode(bot):
    attach(bot, FakeResponse(200, text="<html>not json</html>"))

    with pytest.raises(JSONDecode):
        await bot.request("POST", "getMe", json={})


async def test_connection_errors_raise_network_after_retries(bot):
    bot.max_retries = 2
    attach(
        bot,
        aiohttp.ClientConnectionError("boom"),
        aiohttp.ClientConnectionError("boom"),
    )

    with pytest.raises(Network):
        await bot.request("POST", "getMe", json={})

"""Shared fixtures and fakes for the darkob test suite.

Nothing in this suite opens a socket or contacts a real API: every HTTP
interaction goes through :class:`FakeSession`.
"""

from __future__ import annotations

import json
from typing import Any, List

import pytest

from darkob import Bot

#: Matches ``Bot.TOKEN_PATTERN`` (``^[A-Z]{5}[0-9A-Z]{59}$``) so constructing a
#: Bot never falls through to the interactive ``input()`` prompt.
VALID_TOKEN = "ABCDE" + "0" * 59


class FakeResponse:
    """Minimal stand-in for ``aiohttp.ClientResponse`` as a context manager."""

    def __init__(self, status: int = 200, payload: Any = None, text: str = ""):
        self.status = status
        self._payload = payload
        self._text = text

    async def __aenter__(self) -> "FakeResponse":
        return self

    async def __aexit__(self, *exc_info) -> bool:
        return False

    async def text(self) -> str:
        if self._text:
            return self._text
        return json.dumps({} if self._payload is None else self._payload)


class FakeSession:
    """Replays queued responses (or raises queued exceptions) and records calls."""

    def __init__(self, responses: List[Any]) -> None:
        self._responses = list(responses)
        self.requests: List[tuple] = []

    def request(self, method: str, url: str, **kwargs: Any):
        self.requests.append((method, url, kwargs))
        if not self._responses:
            raise AssertionError("FakeSession ran out of queued responses")
        item = self._responses.pop(0)
        if isinstance(item, BaseException):
            raise item
        return item

    @property
    def count(self) -> int:
        return len(self.requests)


def attach(bot: Bot, *responses: Any) -> FakeSession:
    """Attach a fake transport to ``bot`` and return it."""
    session = FakeSession(list(responses))

    async def _get_session():
        return session

    bot._get_session = _get_session  # type: ignore[method-assign]
    return session


@pytest.fixture(autouse=True)
def _no_retry_backoff(monkeypatch):
    """Neutralize exponential backoff so retry tests don't actually sleep."""
    import asyncio

    async def _sleep(_delay, *args, **kwargs):
        return None

    monkeypatch.setattr(asyncio, "sleep", _sleep)


@pytest.fixture
def bot() -> Bot:
    """A Bot instance with no network access and minimal retries."""
    return Bot(token=VALID_TOKEN, show_welcome=False, max_retries=2)

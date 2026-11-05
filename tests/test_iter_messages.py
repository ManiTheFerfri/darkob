"""Tests for the streaming message iterator."""

from __future__ import annotations

import pytest

from darkob.client.exceptions import InvalidInput
from darkob.client.messages.iter_messages import IterMessages


class FakeMessenger(IterMessages):
    def __init__(self, pages):
        self._pages = list(pages)
        self.payloads = []

    async def get_guid(self, chat):
        return "g0chat"

    async def request(self, method, input=None, **kwargs):
        self.payloads.append(dict(input or {}))
        return self._pages.pop(0) if self._pages else {"messages": []}


def page(ids, *, more=True, next_id=None):
    data = {"messages": [{"message_id": str(i)} for i in ids], "has_continue": more}
    if next_id is not None:
        data["new_min_id"] = str(next_id)
        data["new_max_id"] = str(next_id)
    return data


async def collect(client, **kwargs):
    return [message["message_id"] async for message in client.iter_messages("g0chat", **kwargs)]


async def test_yields_every_message_across_pages():
    client = FakeMessenger([page([1, 2], next_id=2), page([3], more=False)])

    assert await collect(client) == ["1", "2", "3"]


async def test_advances_the_cursor():
    client = FakeMessenger([page([1], next_id=1), page([2], more=False)])

    await collect(client)

    assert "min_id" not in client.payloads[0]
    assert client.payloads[1]["min_id"] == "1"


async def test_from_max_uses_max_id():
    client = FakeMessenger([page([9], next_id=9), page([8], more=False)])

    await collect(client, sort="FromMax")

    assert client.payloads[0]["sort"] == "FromMax"
    assert client.payloads[1]["max_id"] == "9"


async def test_stops_at_max_items():
    client = FakeMessenger([page([1, 2, 3], next_id=3)])

    assert await collect(client, max_items=2) == ["1", "2"]


async def test_does_not_yield_duplicate_ids():
    client = FakeMessenger([page([1, 2], next_id=2), page([2, 3], more=False)])

    assert await collect(client) == ["1", "2", "3"]


async def test_stops_when_the_server_has_no_more():
    client = FakeMessenger([page([1], more=False)])

    assert await collect(client) == ["1"]
    assert len(client.payloads) == 1


async def test_stops_when_the_cursor_stops_advancing():
    client = FakeMessenger([page([1], next_id=None)])

    assert await collect(client) == ["1"]
    assert len(client.payloads) == 1


async def test_empty_first_page_returns_nothing():
    client = FakeMessenger([{"messages": []}])

    assert await collect(client) == []


async def test_passes_the_filter_type():
    client = FakeMessenger([page([1], more=False)])

    await collect(client, filter_type="voice")

    assert client.payloads[0]["filter_type"] == "Voice"


async def test_rejects_an_invalid_sort():
    client = FakeMessenger([])

    with pytest.raises(InvalidInput):
        await collect(client, sort="sideways")


async def test_rejects_an_invalid_filter():
    client = FakeMessenger([])

    with pytest.raises(InvalidInput):
        await collect(client, filter_type="banana")


async def test_rejects_a_non_positive_page_size():
    client = FakeMessenger([])

    with pytest.raises(InvalidInput):
        await collect(client, page_size=0)

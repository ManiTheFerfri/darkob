"""Tests for FSM storage, context and state filtering."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from darkob import (
    FSMContext,
    JsonFileStorage,
    MemoryStorage,
    StateFilter,
)
from darkob.fsm import default_storage_key


# ---------------------------------------------------------------------------
# MemoryStorage
# ---------------------------------------------------------------------------


async def test_state_roundtrip():
    storage = MemoryStorage()

    assert await storage.get_state("chat") is None
    await storage.set_state("chat", "waiting")
    assert await storage.get_state("chat") == "waiting"


async def test_setting_none_clears_state():
    storage = MemoryStorage()
    await storage.set_state("chat", "waiting")
    await storage.set_state("chat", None)

    assert await storage.get_state("chat") is None


async def test_data_is_isolated_per_key():
    storage = MemoryStorage()
    await storage.set_data("a", {"x": 1})
    await storage.set_data("b", {"x": 2})

    assert await storage.get_data("a") == {"x": 1}
    assert await storage.get_data("b") == {"x": 2}


async def test_get_data_returns_a_copy():
    storage = MemoryStorage()
    await storage.set_data("a", {"x": 1})

    data = await storage.get_data("a")
    data["x"] = 999

    assert await storage.get_data("a") == {"x": 1}


async def test_clear_drops_state_and_data():
    storage = MemoryStorage()
    await storage.set_state("a", "s")
    await storage.set_data("a", {"x": 1})

    await storage.clear("a")

    assert await storage.get_state("a") is None
    assert await storage.get_data("a") == {}


# ---------------------------------------------------------------------------
# JsonFileStorage
# ---------------------------------------------------------------------------


async def test_json_storage_survives_reopening(tmp_path):
    path = str(tmp_path / "fsm.json")

    first = JsonFileStorage(path)
    await first.set_state("chat", "step-1")
    await first.set_data("chat", {"name": "Ada"})

    second = JsonFileStorage(path)

    assert await second.get_state("chat") == "step-1"
    assert await second.get_data("chat") == {"name": "Ada"}


async def test_json_storage_tolerates_a_corrupt_file(tmp_path):
    path = tmp_path / "fsm.json"
    path.write_text("{not valid json", encoding="utf-8")

    storage = JsonFileStorage(str(path))

    assert await storage.get_state("chat") is None
    await storage.set_state("chat", "ok")
    assert await storage.get_state("chat") == "ok"


async def test_json_storage_clear_is_persisted(tmp_path):
    path = str(tmp_path / "fsm.json")
    storage = JsonFileStorage(path)
    await storage.set_state("chat", "step-1")
    await storage.clear("chat")

    assert await JsonFileStorage(path).get_state("chat") is None


# ---------------------------------------------------------------------------
# FSMContext
# ---------------------------------------------------------------------------


async def test_context_update_data_merges():
    ctx = FSMContext(MemoryStorage(), key="chat")

    await ctx.update_data(name="Ada")
    await ctx.update_data(city="London")

    assert await ctx.get_data() == {"name": "Ada", "city": "London"}


async def test_context_set_and_clear():
    ctx = FSMContext(MemoryStorage(), key="chat")

    await ctx.set_state("waiting")
    await ctx.update_data(answer=42)
    assert await ctx.get_state() == "waiting"

    await ctx.clear()

    assert await ctx.get_state() is None
    assert await ctx.get_data() == {}


async def test_two_contexts_share_storage_by_key():
    storage = MemoryStorage()
    writer = FSMContext(storage, key="chat")
    reader = FSMContext(storage, key="chat")

    await writer.set_state("waiting")

    assert await reader.get_state() == "waiting"


async def test_context_from_event_uses_chat_id():
    storage = MemoryStorage()
    event = SimpleNamespace(chat_id="g0abc")

    ctx = FSMContext.from_event(storage, event)
    await ctx.set_state("waiting")

    assert await storage.get_state("g0abc") == "waiting"


# ---------------------------------------------------------------------------
# StateFilter
# ---------------------------------------------------------------------------


async def test_state_filter_matches_current_state():
    storage = MemoryStorage()
    event = SimpleNamespace(chat_id="chat")
    await storage.set_state("chat", "waiting")

    assert await StateFilter(storage, "waiting").evaluate(event) is True
    assert await StateFilter(storage, "done").evaluate(event) is False


async def test_state_filter_is_false_when_no_state_is_set():
    storage = MemoryStorage()
    event = SimpleNamespace(chat_id="chat")

    assert await StateFilter(storage, "waiting").evaluate(event) is False


async def test_state_filter_accepts_a_custom_key_function():
    storage = MemoryStorage()
    event = SimpleNamespace(chat_id="ignored", user_id="u1")
    await storage.set_state("u1", "waiting")

    filt = StateFilter(storage, "waiting", key_func=lambda e: e.user_id)

    assert await filt.evaluate(event) is True


@pytest.mark.parametrize(
    "event,expected",
    [
        (SimpleNamespace(chat_id="c1"), "c1"),
        (SimpleNamespace(object_guid="u0x"), "u0x"),
        (SimpleNamespace(), "default"),
    ],
)
def test_default_storage_key(event, expected):
    assert default_storage_key(event) == expected

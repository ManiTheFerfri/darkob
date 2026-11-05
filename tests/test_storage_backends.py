"""Tests for the SQLite and TTL storage backends."""

from __future__ import annotations

import asyncio

import pytest

from darkob.fsm import SQLiteStorage, TTLMemoryStorage


# ---------------------------------------------------------------------------
# TTLMemoryStorage
# ---------------------------------------------------------------------------


async def test_ttl_storage_roundtrip():
    storage = TTLMemoryStorage(ttl=60)

    await storage.set_state("chat", "waiting")
    await storage.set_data("chat", {"a": 1})

    assert await storage.get_state("chat") == "waiting"
    assert await storage.get_data("chat") == {"a": 1}


async def test_ttl_storage_expires_state_and_data(monkeypatch):
    storage = TTLMemoryStorage(ttl=10)
    await storage.set_state("chat", "waiting")
    await storage.set_data("chat", {"a": 1})

    # Move time forward past the TTL.
    import darkob.fsm as fsm_module

    real_time = fsm_module.time.time
    monkeypatch.setattr(fsm_module.time, "time", lambda: real_time() + 11)

    assert await storage.get_state("chat") is None
    assert await storage.get_data("chat") == {}


async def test_ttl_storage_clear_forgets_the_timestamp():
    storage = TTLMemoryStorage(ttl=60)
    await storage.set_state("chat", "waiting")

    await storage.clear("chat")

    assert await storage.get_state("chat") is None
    assert "chat" not in storage._touched


async def test_ttl_storage_rejects_a_non_positive_ttl():
    with pytest.raises(ValueError):
        TTLMemoryStorage(ttl=0)


# ---------------------------------------------------------------------------
# SQLiteStorage
# ---------------------------------------------------------------------------


async def test_sqlite_roundtrip(tmp_path):
    storage = SQLiteStorage(str(tmp_path / "fsm.db"))

    await storage.set_state("chat", "step-1")
    await storage.set_data("chat", {"name": "Ada"})

    assert await storage.get_state("chat") == "step-1"
    assert await storage.get_data("chat") == {"name": "Ada"}

    await storage.close()


async def test_sqlite_persists_across_reopening(tmp_path):
    path = str(tmp_path / "fsm.db")

    first = SQLiteStorage(path)
    await first.set_state("chat", "step-1")
    await first.set_data("chat", {"name": "Ada"})
    await first.close()

    second = SQLiteStorage(path)

    assert await second.get_state("chat") == "step-1"
    assert await second.get_data("chat") == {"name": "Ada"}

    await second.close()


async def test_sqlite_state_and_data_are_independent(tmp_path):
    storage = SQLiteStorage(str(tmp_path / "fsm.db"))

    await storage.set_data("a", {"x": 1})
    await storage.set_data("b", {"x": 2})

    assert await storage.get_data("a") == {"x": 1}
    assert await storage.get_data("b") == {"x": 2}
    assert await storage.get_state("a") is None

    await storage.close()


async def test_sqlite_clear_removes_the_row(tmp_path):
    storage = SQLiteStorage(str(tmp_path / "fsm.db"))
    await storage.set_state("chat", "s")
    await storage.set_data("chat", {"a": 1})

    await storage.clear("chat")

    assert await storage.get_state("chat") is None
    assert await storage.get_data("chat") == {}

    await storage.close()


async def test_sqlite_handles_concurrent_writes(tmp_path):
    storage = SQLiteStorage(str(tmp_path / "fsm.db"))

    async def write(index: int) -> None:
        await storage.set_data(f"chat{index}", {"index": index})

    await asyncio.gather(*(write(i) for i in range(25)))

    for i in range(25):
        assert await storage.get_data(f"chat{i}") == {"index": i}

    await storage.close()


async def test_sqlite_survives_corrupt_json(tmp_path):
    storage = SQLiteStorage(str(tmp_path / "fsm.db"))
    await storage.set_data("chat", {"a": 1})

    # Corrupt the stored payload directly.
    storage._connection.execute("UPDATE fsm SET data = 'not json' WHERE key = 'chat'")
    storage._connection.commit()

    assert await storage.get_data("chat") == {}

    await storage.close()

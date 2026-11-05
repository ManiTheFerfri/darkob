"""Tests for the offline send queue."""

from __future__ import annotations

import asyncio

import pytest

from darkob.bot.exceptions import Network
from darkob.queue import QueueFull, SendQueue


class FakeBot:
    def __init__(self, failing: bool = False):
        self.sent = []
        self.failing = failing

    async def send_message(self, **kwargs):
        if self.failing:
            raise Network("network is down")
        self.sent.append(kwargs)
        return {"status": "OK"}


async def test_put_sends_immediately_when_the_network_is_up():
    bot = FakeBot()
    queue = SendQueue(bot)

    delivered = await queue.put("g0chat", "hello")

    assert delivered is True
    assert queue.pending == 0
    assert bot.sent == [{"chat_id": "g0chat", "text": "hello"}]


async def test_put_queues_when_the_network_is_down():
    bot = FakeBot(failing=True)
    queue = SendQueue(bot)

    delivered = await queue.put("g0chat", "hello")

    assert delivered is False
    assert queue.pending == 1


async def test_flush_sends_pending_messages():
    bot = FakeBot(failing=True)
    queue = SendQueue(bot)
    await queue.put("g0chat", "one")

    bot.failing = False
    delivered = await queue.flush()

    assert delivered == 1
    assert queue.pending == 0
    assert bot.sent[-1]["text"] == "one"


async def test_flush_keeps_items_when_the_network_is_still_down():
    bot = FakeBot(failing=True)
    queue = SendQueue(bot)
    await queue.put("g0chat", "one")

    assert await queue.flush() == 0
    assert queue.pending == 1


async def test_flush_drops_a_message_that_is_permanently_invalid():
    class ScriptedBot:
        def __init__(self):
            self.mode = "down"
            self.sent = []

        async def send_message(self, **kwargs):
            if self.mode == "down":
                raise Network("down")
            if kwargs.get("text") == "bad":
                raise ValueError("invalid input")
            self.sent.append(kwargs)
            return {"status": "OK"}

    bot = ScriptedBot()
    queue = SendQueue(bot)
    await queue.put("g0chat", "bad")
    await queue.put("g0chat", "good")

    bot.mode = "up"
    delivered = await queue.flush()

    assert delivered == 1, "the invalid message is dropped, not retried forever"
    assert queue.pending == 0
    assert [m["text"] for m in bot.sent] == ["good"]


async def test_queue_is_bounded():
    bot = FakeBot(failing=True)
    queue = SendQueue(bot, max_size=2)

    await queue.put("g0chat", "one")
    await queue.put("g0chat", "two")

    with pytest.raises(QueueFull):
        await queue.put("g0chat", "three")


async def test_queue_persists_across_instances(tmp_path):
    path = str(tmp_path / "outbox.json")
    bot = FakeBot(failing=True)
    queue = SendQueue(bot, path=path)
    await queue.put("g0chat", "survives restart")

    reopened = SendQueue(FakeBot(failing=True), path=path)

    assert reopened.pending == 1
    assert reopened.drain()[0]["text"] == "survives restart"


async def test_corrupt_queue_file_is_ignored(tmp_path):
    path = tmp_path / "outbox.json"
    path.write_text("{not json", encoding="utf-8")

    queue = SendQueue(FakeBot(), path=str(path))

    assert queue.pending == 0


async def test_drain_empties_the_queue():
    bot = FakeBot(failing=True)
    queue = SendQueue(bot)
    await queue.put("g0chat", "one")
    await queue.put("g0chat", "two")

    items = queue.drain()

    assert len(items) == 2
    assert queue.pending == 0


async def test_start_creates_a_worker_and_stop_cancels_it():
    # The worker is a thin loop over flush(), which is covered above; this
    # only asserts the lifecycle, since the suite neutralises asyncio.sleep.
    queue = SendQueue(FakeBot(), retry_delay=0.01)

    task = queue.start()
    assert isinstance(task, asyncio.Task)

    await queue.stop()
    assert task.done() or task.cancelled()


async def test_put_does_not_queue_a_permanent_error():
    class BadBot:
        async def send_message(self, **kwargs):
            raise ValueError("this message is invalid")

    queue = SendQueue(BadBot())

    with pytest.raises(ValueError):
        await queue.put("g0chat", "bad")

    assert queue.pending == 0, "a permanent error must not enter the outbox"


async def test_stop_is_safe_without_a_worker():
    queue = SendQueue(FakeBot())

    await queue.stop()


def test_zero_max_size_is_rejected():
    with pytest.raises(ValueError):
        SendQueue(FakeBot(), max_size=0)


def test_repr_shows_pending_count():
    queue = SendQueue(FakeBot(), path="x.json")

    assert "pending=0" in repr(queue)

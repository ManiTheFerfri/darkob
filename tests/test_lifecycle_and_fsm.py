"""Lifecycle, transport affinity, FSM, and filter-failure regressions."""

from __future__ import annotations

import asyncio
import threading

import pytest

from darkob import FSMContext, MemoryStorage
from darkob.bot.filters import EventConstraint
from darkob.metrics import metrics as _metrics


_real_sleep = asyncio.sleep


class _FakeClientSession:
    def __init__(self, *, close_delay: float = 0.0) -> None:
        self.closed = False
        self.close_calls = 0
        self.close_delay = close_delay

    async def close(self) -> None:
        if self.close_delay:
            await _real_sleep(self.close_delay)
        self.close_calls += 1
        self.closed = True


async def _return_from_poll(_interval: float = 0.005) -> None:
    return None


async def test_start_drains_updates_before_shutdown_and_transport_close(bot, monkeypatch):
    """A transport close before its users finish loses the required ordering."""
    order = []
    started = asyncio.Event()
    release = asyncio.Event()

    async def update():
        started.set()
        await release.wait()
        order.append("update-finished")

    bot._spawn_update(update())

    async def poll(_interval):
        await started.wait()
        release.set()

    async def close():
        order.append("close")

    monkeypatch.setattr(bot, "_poll_loop", poll)
    monkeypatch.setattr(bot, "close", close)
    bot._registry.store_shutdown(lambda _: order.append("shutdown"))

    await bot.start()

    assert order == ["update-finished", "shutdown", "close"]


async def test_shutdown_hook_can_use_session_before_transport_closes(bot, monkeypatch):
    """Closing first leaves the session created by this hook open after start."""
    monkeypatch.setattr(bot, "_poll_loop", _return_from_poll)
    transport = None

    async def on_shutdown(current_bot):
        nonlocal transport
        transport = await current_bot._get_session()
        assert not transport.closed

    bot._registry.store_shutdown(on_shutdown)
    try:
        await bot.start()
        assert transport is not None
        assert transport.closed
        assert bot._session is None
    finally:
        if transport is not None and not transport.closed:
            await transport.close()


@pytest.mark.parametrize("error", [RuntimeError("boom"), asyncio.CancelledError()])
async def test_start_closes_transport_when_shutdown_hook_raises_or_cancels(
    bot, monkeypatch, error
):
    """Skipping the outer finally on hook failures leaks the transport."""
    monkeypatch.setattr(bot, "_poll_loop", _return_from_poll)
    order = []

    async def close():
        order.append("close")

    async def on_shutdown(_):
        order.append("shutdown")
        raise error

    monkeypatch.setattr(bot, "close", close)
    bot._registry.store_shutdown(on_shutdown)

    if isinstance(error, asyncio.CancelledError):
        with pytest.raises(asyncio.CancelledError):
            await bot.start()
    else:
        await bot.start()

    assert order == ["shutdown", "close"]


async def test_disconnect_on_owner_loop_schedules_real_close(bot):
    """The same-loop path must schedule, rather than synchronously deadlock."""
    transport = _FakeClientSession()
    bot._session = transport
    bot._session_loop = asyncio.get_running_loop()

    bot.disconnect()
    close_task = bot._close_task
    assert close_task is not None
    await close_task

    assert transport.close_calls == 1
    assert transport.closed
    assert bot._session is None


def test_disconnect_waits_for_cross_thread_running_owner(bot):
    """Fire-and-forget makes synchronous disconnect return with a live session."""
    owner = asyncio.new_event_loop()
    ready = threading.Event()

    def run_owner():
        asyncio.set_event_loop(owner)
        ready.set()
        owner.run_forever()

    thread = threading.Thread(target=run_owner, daemon=True)
    thread.start()
    assert ready.wait(1)
    transport = _FakeClientSession(close_delay=0.05)
    bot._session = transport
    bot._session_loop = owner
    try:
        bot.disconnect()

        assert transport.closed
        assert transport.close_calls == 1
        assert bot._session is None
    finally:
        if not transport.closed:
            asyncio.run_coroutine_threadsafe(transport.close(), owner).result(1)
        owner.call_soon_threadsafe(owner.stop)
        thread.join(1)
        owner.close()


def test_disconnect_runs_stopped_owner_to_completion(bot):
    """A stopped, open owner can close its transport from synchronous code."""
    owner = asyncio.new_event_loop()
    transport = _FakeClientSession()
    bot._session = transport
    bot._session_loop = owner
    try:
        bot.disconnect()

        assert transport.closed
        assert bot._session is None
    finally:
        if not transport.closed:
            owner.run_until_complete(transport.close())
        owner.close()


async def test_disconnect_from_running_loop_rejects_stopped_owner_without_discard(bot):
    """Discarding this reference is unsafe because run_until_complete cannot nest."""
    owner = asyncio.new_event_loop()
    transport = _FakeClientSession()
    bot._session = transport
    bot._session_loop = owner
    try:
        with pytest.raises(RuntimeError, match="stopped"):
            bot.disconnect()

        assert not transport.closed
        assert bot._session is transport
        assert bot._session_loop is owner
    finally:
        await transport.close()
        owner.close()


def test_disconnect_rejects_closed_owner_without_discarding_live_transport(bot):
    """A closed owner requires actionable cleanup, not silent reference loss."""
    owner = asyncio.new_event_loop()
    owner.close()
    transport = _FakeClientSession()
    bot._session = transport
    bot._session_loop = owner

    with pytest.raises(RuntimeError, match="closed"):
        bot.disconnect()

    assert not transport.closed
    assert bot._session is transport
    assert bot._session_loop is owner


async def test_failed_async_close_does_not_forget_live_transport(bot):
    """Forgetting after an exception prevents a later cleanup retry."""

    class BrokenTransport(_FakeClientSession):
        async def close(self):
            self.close_calls += 1
            raise OSError("close failed")

    transport = BrokenTransport()
    bot._session = transport
    bot._session_loop = asyncio.get_running_loop()

    await bot.close()

    assert not transport.closed
    assert transport.close_calls == 1
    assert bot._session is transport
    assert bot._session_loop is not None


class _YieldingStorage(MemoryStorage):
    async def get_data(self, key):
        data = await super().get_data(key)
        await _real_sleep(0)
        return data


async def test_concurrent_context_updates_share_a_lock_for_the_exact_storage_key():
    """Without a shared context lock, both transactions overwrite one field."""
    storage = _YieldingStorage()
    first = FSMContext(storage, key="chat")
    second = FSMContext(storage, key="chat")
    await storage.set_state("chat", "waiting")

    await asyncio.gather(first.update_data(first=1), second.update_data(second=2))

    assert await first.get_data() == {"first": 1, "second": 2}
    assert await second.get_state() == "waiting"


class _IndependentlyYieldingStorage(MemoryStorage):
    def __init__(self):
        super().__init__()
        self.entered = {"first": asyncio.Event(), "second": asyncio.Event()}
        self.release = {"first": asyncio.Event(), "second": asyncio.Event()}

    async def get_data(self, key):
        data = await super().get_data(key)
        self.entered[key].set()
        await self.release[key].wait()
        return data


async def test_update_locks_do_not_serialize_different_storage_keys():
    """A global update lock prevents key two from reaching its own read."""
    storage = _IndependentlyYieldingStorage()
    first = FSMContext(storage, key="first")
    second = FSMContext(storage, key="second")

    first_task = asyncio.create_task(first.update_data(first=1))
    await asyncio.wait_for(storage.entered["first"].wait(), timeout=1)
    second_task = asyncio.create_task(second.update_data(second=2))
    try:
        await asyncio.wait_for(storage.entered["second"].wait(), timeout=1)
    finally:
        storage.release["first"].set()
        storage.release["second"].set()
        await asyncio.gather(first_task, second_task)

    assert await first.get_data() == {"first": 1}
    assert await second.get_data() == {"second": 2}


async def test_constraint_error_reports_exact_event_and_counts_once(bot, monkeypatch):
    """Returning false before report_error hides filter crashes and their metric."""
    registry = bot._registry
    error = ValueError("bad filter")
    event = object()
    received = []
    later_evaluations = 0
    handler_calls = 0

    class Explode(EventConstraint):
        async def evaluate(self, actual_event):
            assert actual_event is event
            raise error

    class MustNotRun(EventConstraint):
        async def evaluate(self, actual_event):
            nonlocal later_evaluations
            later_evaluations += 1
            return True

    async def handler(_, actual_event):
        nonlocal handler_calls
        handler_calls += 1

    @bot.on_error()
    async def on_error(actual_bot, actual_error, actual_event):
        received.append((actual_bot, actual_error, actual_event))

    registry.store(handler, Explode(), MustNotRun())
    monkeypatch.setattr(_metrics, "enabled", True)
    previous_errors = _metrics.counters.get("darkob.handlers.errors", 0)

    await registry.feed(event)

    assert len(received) == 1
    assert received[0][0] is bot
    assert received[0][1] is error
    assert received[0][2] is event
    assert later_evaluations == 0
    assert handler_calls == 0
    assert _metrics.counters["darkob.handlers.errors"] == previous_errors + 1

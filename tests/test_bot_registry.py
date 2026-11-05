"""Tests for the Bot handler registry and dispatch pipeline."""

from __future__ import annotations

from types import SimpleNamespace

from darkob.bot.filters import EventConstraint
from darkob.bot.registry import HandlerRegistry


class Allow(EventConstraint):
    def __init__(self, value: bool = True) -> None:
        self.value = value

    async def evaluate(self, event):
        return self.value


def make_registry(run_all: bool = True):
    bot = SimpleNamespace(run_all_handlers=run_all)
    return HandlerRegistry(bot), bot


async def test_handler_runs_for_matching_event():
    registry, bot = make_registry()
    seen = []

    @registry.store
    async def handler(bot, event):
        seen.append(event)

    await registry.feed({"n": 1})

    assert seen == [{"n": 1}]


async def test_handler_is_skipped_when_constraint_fails():
    registry, bot = make_registry()
    seen = []

    registry.store(_recorder(seen), Allow(False))

    await registry.feed({"n": 1})

    assert seen == []


async def test_run_all_handlers_true_runs_every_match():
    registry, bot = make_registry(run_all=True)
    seen = []

    registry.store(_recorder(seen, "first"))
    registry.store(_recorder(seen, "second"))

    await registry.feed({})

    assert seen == ["first", "second"]


async def test_run_all_handlers_false_stops_after_first_match():
    registry, bot = make_registry(run_all=False)
    seen = []

    registry.store(_recorder(seen, "first"))
    registry.store(_recorder(seen, "second"))

    await registry.feed({})

    assert seen == ["first"]


async def test_failing_handler_does_not_stop_the_next_one():
    registry, bot = make_registry()
    seen = []

    @registry.store
    async def boom(bot, event):
        raise RuntimeError("handler exploded")

    registry.store(_recorder(seen, "survived"))

    await registry.feed({})

    assert seen == ["survived"]


async def test_sync_handler_is_supported():
    registry, bot = make_registry()
    seen = []

    @registry.store
    def sync_handler(bot, event):
        seen.append("sync")

    await registry.feed({})

    assert seen == ["sync"]


async def test_middleware_runs_before_handlers():
    registry, bot = make_registry()
    order = []

    @registry.store_middleware
    async def middleware(bot, event, call_next):
        order.append("before")
        await call_next()
        order.append("after")

    registry.store(_recorder(order, "handler"))

    await registry.feed({})

    assert order == ["before", "handler", "after"]


async def test_middleware_can_stop_the_chain():
    registry, bot = make_registry()
    seen = []

    @registry.store_middleware
    async def blocking(bot, event, call_next):
        seen.append("middleware")
        return None  # never calls next

    registry.store(_recorder(seen, "handler"))

    await registry.feed({})

    assert seen == ["middleware"]


async def test_middleware_exception_does_not_break_dispatch():
    registry, bot = make_registry()
    seen = []

    @registry.store_middleware
    async def broken(bot, event, call_next):
        raise RuntimeError("middleware exploded")

    registry.store(_recorder(seen, "handler"))

    await registry.feed({})
    # The middleware failed before reaching the handler.

    assert seen == []


async def test_startup_and_shutdown_callbacks():
    registry, bot = make_registry()
    events = []

    @registry.store_startup
    async def on_start(bot):
        events.append("start")

    @registry.store_shutdown
    def on_stop(bot):
        events.append("stop")

    await registry.fire_startup()
    await registry.fire_shutdown()

    assert events == ["start", "stop"]


def _recorder(sink, label="ran"):
    async def handler(bot, event):
        sink.append(label)

    return handler

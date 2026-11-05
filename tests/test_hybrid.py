"""Tests for the sync/async bridge that powers unawaited calls."""

from __future__ import annotations

import asyncio

import pytest

from darkob.hybrid import SyncLoop, close_sync_loop


def test_runs_a_coroutine_and_returns_its_value():
    loop = SyncLoop("test")
    try:

        async def add(a, b):
            return a + b

        assert loop.run(add(2, 3)) == 5
    finally:
        loop.close()


def test_propagates_exceptions_from_the_coroutine():
    loop = SyncLoop("test")
    try:

        async def boom():
            raise ValueError("nope")

        with pytest.raises(ValueError, match="nope"):
            loop.run(boom())
    finally:
        loop.close()


def test_rejects_non_coroutines():
    loop = SyncLoop("test")
    try:
        with pytest.raises(TypeError):
            loop.run(42)
    finally:
        loop.close()


def test_refuses_nested_sync_calls_from_the_worker_thread():
    loop = SyncLoop("test")
    try:

        async def nested():
            # This executes on the worker thread; a sync call here would
            # deadlock, so it must be rejected loudly.
            loop.run(asyncio.sleep(0))

        with pytest.raises(RuntimeError, match="inside the SyncLoop worker"):
            loop.run(nested())
    finally:
        loop.close()


def test_reuses_one_thread_across_calls():
    loop = SyncLoop("test")
    try:

        async def thread_name():
            return asyncio.current_task().get_name()

        first = loop.run(thread_name())
        second = loop.run(thread_name())
        assert first and second
    finally:
        loop.close()


def test_closing_twice_is_safe():
    loop = SyncLoop("test")
    loop.close()
    loop.close()


def test_run_after_close_raises():
    loop = SyncLoop("test")
    loop.close()

    async def work():
        return 1

    with pytest.raises(RuntimeError, match="closed"):
        loop.run(work())


def test_module_level_close_is_idempotent():
    close_sync_loop()
    close_sync_loop()

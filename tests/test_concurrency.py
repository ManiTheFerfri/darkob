"""Tests for structured-concurrency helpers (``darkob.utils.concurrency``)."""

from __future__ import annotations

import asyncio

import pytest

from darkob.utils.concurrency import (
    TaskGroup,
    TaskGroupError,
    _FallbackTaskGroup,
    _Timeout,
    native_task_group,
    native_timeout,
    timeout_after,
)

#: ``conftest`` patches ``asyncio.sleep`` to a no-op for the whole suite; the
#: timeout tests need the real thing back.
REAL_SLEEP = asyncio.sleep


def flatten(error: BaseException) -> list:
    """Every underlying exception, whatever the interpreter version."""
    nested = getattr(error, "exceptions", None)
    return list(nested) if nested else [error]


async def boom() -> None:
    raise ValueError("boom")


# ---------------------------------------------------------------------------
# TaskGroup
# ---------------------------------------------------------------------------


def test_version_flags_are_booleans():
    assert isinstance(native_task_group, bool)
    assert isinstance(native_timeout, bool)


@pytest.mark.parametrize("group_cls", [TaskGroup, _FallbackTaskGroup])
async def test_group_runs_every_task(group_cls):
    seen = []

    async def record(value: int) -> None:
        seen.append(value)

    async with group_cls() as group:
        group.create_task(record(1))
        group.create_task(record(2))

    assert sorted(seen) == [1, 2]


@pytest.mark.parametrize("group_cls", [TaskGroup, _FallbackTaskGroup])
async def test_group_propagates_failures_with_exceptions(group_cls):
    with pytest.raises(BaseException) as info:
        async with group_cls() as group:
            group.create_task(boom(), name="boom")

    assert any(isinstance(error, ValueError) for error in flatten(info.value))


@pytest.mark.parametrize("group_cls", [TaskGroup, _FallbackTaskGroup])
async def test_group_cancels_siblings(group_cls):
    cancelled = {"value": False}

    async def stubborn() -> None:
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            cancelled["value"] = True
            raise

    with pytest.raises(BaseException):
        async with group_cls() as group:
            group.create_task(boom())
            group.create_task(stubborn())

    assert cancelled["value"] is True


@pytest.mark.parametrize("group_cls", [TaskGroup, _FallbackTaskGroup])
async def test_create_task_outside_the_context_is_rejected(group_cls):
    group = group_cls()
    coro = asyncio.sleep(0)

    with pytest.raises(RuntimeError):
        group.create_task(coro)


@pytest.mark.parametrize("group_cls", [TaskGroup, _FallbackTaskGroup])
async def test_create_task_after_exit_is_rejected(group_cls):
    async with group_cls() as group:
        pass

    with pytest.raises(RuntimeError):
        group.create_task(asyncio.sleep(0))


async def test_task_group_error_exposes_errors():
    inner = ValueError("x")
    error = TaskGroupError("failed", (inner,))

    assert error.errors == (inner,)
    assert "failed" in str(error)


# ---------------------------------------------------------------------------
# timeout_after
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("factory", [timeout_after, _Timeout])
async def test_timeout_fires(factory, monkeypatch):
    monkeypatch.setattr(asyncio, "sleep", REAL_SLEEP)

    with pytest.raises(TimeoutError):
        async with factory(0.01) as scope:
            await asyncio.sleep(5)
            scope.cancel()


@pytest.mark.parametrize("factory", [timeout_after, _Timeout])
async def test_fast_body_is_not_interrupted(factory):
    async with factory(5.0) as scope:
        value = 1 + 1

    assert value == 2
    assert scope is not None


async def test_none_means_no_timeout():
    async with timeout_after(None):
        await asyncio.sleep(0)


@pytest.mark.parametrize("factory", [timeout_after, _Timeout])
async def test_other_exceptions_pass_through(factory):
    with pytest.raises(ValueError):
        async with factory(5.0):
            raise ValueError("not a timeout")


async def test_fallback_timeout_reports_the_limit():
    with pytest.raises(TimeoutError) as info:
        async with _Timeout(0.01) as scope:
            await asyncio.Future()
            scope.cancel()

    assert "0.01" in str(info.value)


async def test_cancelling_the_timeout_disables_it(monkeypatch):
    monkeypatch.setattr(asyncio, "sleep", REAL_SLEEP)

    async with _Timeout(0.01) as scope:
        scope.cancel()
        await asyncio.sleep(0.05)

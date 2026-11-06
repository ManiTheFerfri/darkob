"""Structured-concurrency helpers that work on every supported Python.

Python 3.11 added :class:`asyncio.TaskGroup` and :func:`asyncio.timeout`, both
of which give *automatic* cancellation and error propagation. darkob supports
3.9, so it cannot import them unconditionally. This module wraps them so the
library can write one structured-concurrency style everywhere::

    from darkob.utils.concurrency import TaskGroup, timeout_after

    async with TaskGroup() as group:
        group.create_task(fetch(a))
        group.create_task(fetch(b))
    # both finished, or the first failure cancelled the other one

    async with timeout_after(5.0):
        await slow_call()

On 3.11+ these are thin wrappers around the standard library. On 3.9 and 3.10 a
correct reimplementation is used: a failing task cancels its siblings and the
exception is re-raised with the failures attached as ``.exceptions``.

The failure type therefore differs by version, which callers should not rely
on: prefer ``except BaseException`` for cancellation and read ``.exceptions``
when present. :class:`TaskGroupError` is raised on 3.9/3.10 and is a plain
``Exception`` subclass; on 3.11+ the interpreter's native ``ExceptionGroup``
is raised instead.
"""

from __future__ import annotations

import asyncio
import sys
from types import TracebackType
from typing import Any, Awaitable, List, Optional, Set, Tuple, Type, TypeVar

__all__ = [
    "LazyLock",
    "TaskGroup",
    "TaskGroupError",
    "TimeoutError_",
    "native_task_group",
    "native_timeout",
    "timeout_after",
]

_T = TypeVar("_T")

#: True when the running interpreter has ``asyncio.TaskGroup`` (3.11+).
native_task_group = sys.version_info >= (3, 11)
#: True when the running interpreter has ``asyncio.timeout`` (3.11+).
native_timeout = sys.version_info >= (3, 11)

# ``asyncio.TimeoutError`` is ``TimeoutError`` from 3.11 onwards; alias it so
# callers can be version-agnostic.
TimeoutError_ = TimeoutError


class LazyLock:
    """An ``asyncio.Lock`` created on first use, not on construction.

    Python 3.9 binds a lock to the running loop when it is built, and raises
    ``RuntimeError: There is no current event loop`` when there is none. That
    makes eager construction a footgun for anything a user builds at import
    time — a ``TokenBucket``, a ``SendQueue``, or a storage backend::

        limiter = RateLimiter(rate=20)   # module scope, no loop yet

    Creating the lock inside the first ``async with`` removes that ordering
    requirement on every version, and changes nothing on 3.10+, where locks
    are already loop-agnostic.

    It is a drop-in replacement for ``asyncio.Lock`` in the ``async with``
    pattern. Use it wherever a lock lives on an object that can be built
    outside a coroutine.
    """

    __slots__ = ("_lock",)

    def __init__(self) -> None:
        self._lock: Optional["asyncio.Lock"] = None

    def _resolve(self) -> "asyncio.Lock":
        lock = self._lock
        if lock is None:
            lock = asyncio.Lock()
            self._lock = lock
        return lock

    async def __aenter__(self) -> "LazyLock":
        await self._resolve().acquire()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> bool:
        lock = self._lock
        if lock is not None and lock.locked():
            lock.release()
        return False

    def locked(self) -> bool:
        """``True`` when the underlying lock is held."""
        return self._lock is not None and self._lock.locked()

    def __repr__(self) -> str:
        return f"LazyLock(created={self._lock is not None})"


class TaskGroupError(Exception):
    """Raised on Python 3.9/3.10 when one or more tasks in a group failed.

    Carries the same ``.exceptions`` attribute as the interpreter's own
    ``ExceptionGroup``, so downstream code can handle both uniformly.
    """

    def __init__(self, message: str, exceptions: Tuple[BaseException, ...]) -> None:
        super().__init__(message)
        self.exceptions: Tuple[BaseException, ...] = exceptions

    @property
    def errors(self) -> Tuple[BaseException, ...]:
        """Alias for :attr:`exceptions`."""
        return self.exceptions


class _FallbackTaskGroup:
    """``asyncio.TaskGroup`` equivalent for Python 3.9 and 3.10."""

    __slots__ = ("_tasks", "_entered", "_exited", "_errors", "_on_error")

    def __init__(
        self,
        *,
        on_error: Optional[Any] = None,
    ) -> None:
        self._tasks: Set["asyncio.Task[Any]"] = set()
        self._entered = False
        self._exited = False
        self._errors: List[BaseException] = []
        self._on_error = on_error

    # -- lifecycle --------------------------------------------------------

    async def __aenter__(self) -> "_FallbackTaskGroup":
        if self._entered:
            raise RuntimeError("A TaskGroup may only be entered once.")
        self._entered = True
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> bool:
        self._exited = True

        if isinstance(exc, asyncio.CancelledError):
            # We were cancelled from outside. Tear the children down and let
            # the cancellation propagate untouched.
            self._cancel_all()
            await self._drain()
            return False

        if exc is not None:
            # A body exception cancels the children, and the children's own
            # failures are collected alongside it.
            self._cancel_all()
            self._errors.append(exc)
            self._errors.extend(await self._drain())
        else:
            while self._tasks:
                # FIRST_EXCEPTION, not gather(): gather() waits for *every*
                # task, so a task blocked forever would deadlock the group
                # instead of being cancelled when a sibling fails.
                done, _ = await asyncio.wait(
                    set(self._tasks), return_when=asyncio.FIRST_EXCEPTION
                )
                failed = False
                for task in done:
                    if task.cancelled():
                        continue
                    error = task.exception()
                    if error is not None:
                        self._errors.append(error)
                        failed = True
                if failed:
                    self._cancel_all()
                    self._errors.extend(await self._drain())
                    break

        if self._errors:
            raise TaskGroupError(
                f"TaskGroup failed with {len(self._errors)} error(s)",
                tuple(self._errors),
            )

        return False

    async def _drain(self) -> List[BaseException]:
        """Cancel-wait, then collect the real exceptions from finished tasks.

        ``gather(return_exceptions=True)`` is used purely to wait: it blocks
        until every task has finished, whatever the outcome, without
        re-raising. The exceptions are then read off each task, so a
        deliberate cancellation is not mistaken for a failure — while a
        cancellation of *this* task still propagates.
        """
        tasks = list(self._tasks)
        if not tasks:
            return []
        await asyncio.gather(*tasks, return_exceptions=True)

        errors: List[BaseException] = []
        for task in tasks:
            if not task.done() or task.cancelled():
                continue
            error = task.exception()
            if error is not None:
                errors.append(error)
        return errors

    # -- api --------------------------------------------------------------

    def create_task(
        self,
        coro: Awaitable[_T],
        *,
        name: Optional[str] = None,
    ) -> "asyncio.Task[_T]":
        """Spawn *coro* inside the group."""
        if not self._entered:
            if hasattr(coro, "close"):
                coro.close()  # type: ignore[union-attr]
            raise RuntimeError(
                "create_task() called outside the TaskGroup's context manager."
            )
        if self._exited:
            if hasattr(coro, "close"):
                coro.close()  # type: ignore[union-attr]
            raise RuntimeError(
                "create_task() called after the TaskGroup has exited."
            )

        task = asyncio.ensure_future(coro)  # type: ignore[arg-type]
        if name is not None:
            try:
                task.set_name(name)
            except AttributeError:  # pragma: no cover - 3.7 only
                pass
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    def _cancel_all(self) -> None:
        for task in self._tasks:
            if not task.done():
                task.cancel()

    async def join(self) -> None:
        """Wait for the group's current tasks (does not close the group)."""
        if not self._tasks:
            return
        results = await asyncio.gather(
            *list(self._tasks), return_exceptions=True
        )
        for child_error in results:
            if isinstance(child_error, BaseException):
                raise child_error


# ``TaskGroup`` is resolved with getattr, not attribute access: pyright is
# configured for Python 3.10 (the project supports 3.9+), where the attribute
# does not exist, and a plain ``asyncio.TaskGroup`` reference is a hard type
# error there even though the branch is unreachable at runtime.
TaskGroup: Any
if native_task_group:
    TaskGroup = getattr(asyncio, "TaskGroup")
else:
    TaskGroup = _FallbackTaskGroup


class _Timeout:
    """``asyncio.timeout`` equivalent for Python 3.9 and 3.10.

    Schedules a ``loop.call_at`` deadline that cancels the current task, which
    is exactly how the standard library implements it. Without that callback
    the object would be a no-op, so this is the part that matters.
    """

    __slots__ = (
        "_seconds",
        "_deadline",
        "_task",
        "_handle",
        "_expiring",
        "_cancelled",
    )

    def __init__(self, seconds: Optional[float]) -> None:
        self._seconds = seconds
        self._deadline = 0.0
        self._task: Optional["asyncio.Task[Any]"] = None
        self._handle: Optional[asyncio.TimerHandle] = None
        self._expiring = False
        self._cancelled = False

    async def __aenter__(self) -> "_Timeout":
        loop = asyncio.get_running_loop()
        self._task = asyncio.current_task()
        if self._seconds is None:
            self._deadline = float("inf")
            return self
        self._deadline = loop.time() + float(self._seconds)
        self._handle = loop.call_at(self._deadline, self._on_deadline)
        return self

    def _on_deadline(self) -> None:
        """Fired by the loop: cancel the body so it raises CancelledError."""
        self._expiring = True
        if self._task is not None and not self._task.done():
            self._task.cancel()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> bool:
        handle = self._handle
        self._handle = None
        if handle is not None:
            handle.cancel()

        if exc_type is asyncio.CancelledError and self._expiring:
            raise TimeoutError(f"timed out after {self._seconds:g}s") from None
        return False

    def expired(self) -> bool:
        """``True`` when the deadline has passed."""
        if self._expiring:
            return True
        if self._seconds is None:
            return False
        return asyncio.get_running_loop().time() >= self._deadline

    def cancel(self) -> None:
        """Disable the timeout."""
        self._cancelled = True
        handle = self._handle
        self._handle = None
        if handle is not None:
            handle.cancel()


def timeout_after(seconds: Optional[float]) -> Any:
    """Awaitable context manager bounding the body by *seconds*.

    Uses :func:`asyncio.timeout` on 3.11+ and a compatible reimplementation
    below that. A ``None`` delay means "no timeout".
    """
    if seconds is None:
        return _NullTimeout()
    if native_timeout:
        # getattr for the same reason as TaskGroup above: pyright targets 3.10.
        return getattr(asyncio, "timeout")(seconds)
    return _Timeout(seconds)


class _NullTimeout:
    """A no-op timeout context manager."""

    __slots__ = ()

    async def __aenter__(self) -> "_NullTimeout":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> bool:
        return False

    def expired(self) -> bool:
        return False

    def cancel(self) -> None:
        return None

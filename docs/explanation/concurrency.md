# Concurrency

darkob runs on one event loop and owns its state without locks — which is why it is safe to share a client between tasks, and unsafe to share it between loops or threads.

## One loop owns everything

Every mutable structure inside the library belongs to the event loop that
is running it:

| State | Where it lives |
| --- | --- |
| Handler dispatch index | `Api._dispatch_index` |
| Endpoint latency averages | `Api._latency` |
| Circuit breakers | `Api._breakers` |
| Rate-limit buckets | `RateLimiter._global`, `RateLimiter._chats` |
| Conversation registry | `ConversationManager._waiters` |
| Metric registry | `darkob.metrics.metrics` |

None of these needs a lock, because `asyncio` is cooperative: a section of
code that never awaits cannot be interleaved with another task. Every
mutation above is such a section — a dict read followed by a dict write, a
counter increment, a deque append. Where an operation genuinely has to span
an await, the code uses an `asyncio.Lock` instead of a thread lock:

- `TokenBucket` locks around refill-plus-take, and sleeps *outside* the
  lock;
- `SendQueue` locks around the whole flush so two flushes cannot interleave.

`asyncio.Lock` itself only works on one loop, which is another way of
saying the same thing.

!!! warning "One client per loop, one loop per client"
    darkob is **not** safe to share across threads or across event loops.
    Awaiting one `Bot` from two `asyncio.run()` calls, or from a second
    thread's loop, can corrupt the dispatch index, the breakers and the
    buckets — the exact failures the lock-free design avoids by assuming a
    single loop. Create the client inside the loop that will use it and
    keep it there.

Sharing a client between **tasks** on that loop is fine and is the intended
model: a handler, a background task and a metrics scrape can all use the
same object.

## The sync bridge does not change the rule

Calling an async method without `await` runs it on a dedicated worker
thread's loop (`darkob/hybrid.py`). That is still exactly one loop, so it
is safe — as long as you do not also drive the same client from your own
loop. The wrapper detects a running loop and returns the coroutine
unchanged, so mixed style within one process means "pick one per client".

## `darkob.utils.concurrency`

`asyncio.TaskGroup` and `asyncio.timeout` are Python 3.11 additions, and
darkob supports 3.9. This module makes one style available everywhere:

```python
from darkob.utils.concurrency import TaskGroup, timeout_after

async with TaskGroup() as group:
    group.create_task(fetch(a))
    group.create_task(fetch(b))
# both finished, or the first failure cancelled the other one

async with timeout_after(5.0):
    await slow_call()
```

| Name | Meaning |
| --- | --- |
| `native_task_group` / `native_timeout` | `True` on 3.11+, `False` below |
| `TaskGroup` | `asyncio.TaskGroup` on 3.11+, else a compatible reimplementation |
| `timeout_after(seconds)` | `asyncio.timeout` on 3.11+, else a compatible reimplementation; `None` means no timeout |
| `TaskGroupError` | Raised on 3.9/3.10 when one or more grouped tasks fail |

The failure type therefore differs by interpreter, and callers should not
depend on it:

- on 3.9/3.10 a `TaskGroupError` is raised, a plain `Exception` subclass
  carrying `.exceptions` (and `.errors`) as a tuple;
- on 3.11+ the interpreter's native `ExceptionGroup` is raised.

A failing task cancels its siblings in both cases, which is the whole point
of structured concurrency — and the reason the library does not use it
everywhere.

## Why handler dispatch does not use `TaskGroup`

Handlers are independent. One failing handler must not cancel the others,
and one slow handler must not take its siblings down with it. Structured
concurrency gives the opposite guarantee: the first failure cancels the
group. So:

- **Bot** dispatch awaits each handler in turn, inside a `try/except` that
  logs the failure and keeps going (`HandlerRegistry._invoke`).
- **Messenger/Shad** dispatch spawns each matching handler as a task and
  keeps a strong reference to it, with a done-callback that logs the
  exception (`Api._spawn`). One handler's exception is a log line, not a
  cancellation of the rest.

Wrapping either in a `TaskGroup` would be a regression: a broken command in
one handler would silently cancel the sibling that was still replying.

The same reasoning applies to health checks. `HealthRegistry.report()`
runs every probe with `asyncio.gather`, not `TaskGroup`, so that one failing
probe still lets the others report — a liveness endpoint that hides six
green checks because the seventh raised is worse than useless.

## Free-threaded builds (PEP 703)

!!! warning "Not validated"
    darkob has never been run on a free-threaded interpreter. Nothing in
    the codebase special-cases a `--disable-gil` build.

The GIL is load-bearing for the lock-free updates described above:
`dict.get()` followed by `dict[key] = value`, or `counter += 1`, is atomic
only while a single thread holds the GIL. On a free-threaded build those
sequences can interleave, so the "no locks needed" argument stops holding.

The supported configuration on such a build is unchanged: **one client, one
event loop, one thread driving it.** Do not treat the absence of locks as a
promise of thread safety — it is a consequence of the single-loop rule.
(On CPython 3.13 and later, `sys._is_gil_enabled()` reports whether the GIL
is active in the running interpreter.)

## Practical rules

1. Construct clients inside the loop that will use them.
2. Share a client across tasks; never across loops or threads.
3. Use `asyncio.create_task` for fire-and-forget work and keep a reference
   to the task, so it is not garbage-collected mid-flight.
4. Bound concurrency: `max_concurrent_updates` (default 32) caps updates,
   `RateLimiter` caps outgoing calls.
5. Prefer `timeout_after()` over hand-rolled `wait_for` when the code has to
   run on 3.9 as well as 3.11+.

## See also

- [Architecture](architecture.md)
- [Reliability](reliability.md)
- [Errors](../guides/errors.md)
- [Sync and async](../guides/sync-and-async.md)
- [Project layout](../guides/project-layout.md)

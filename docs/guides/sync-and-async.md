# Sync and async

Every public method exists in both flavours.

## The rule

- Called with `await` → runs on the current event loop.
- Called without `await` → darkob submits the coroutine to one shared
  background loop and blocks until it returns.

```python
me = await bot.get_me()     # async
me = bot.get_me()           # sync, same result
```

## How it works

`darkob.hybrid` starts one daemon thread when the first sync call is
made. That thread owns an asyncio loop; sync calls hand work to it with
`run_coroutine_threadsafe` and wait. There is no per-call thread, and the
loop is shut down at interpreter exit.

## Choosing a style

| Style | Use when |
| --- | --- |
| `async` | You already run a loop, or you need concurrency |
| `sync` | A script, a cron job, a quick prototype |

Pick one per codebase. Inside a running event loop, a hybrid method returns
a coroutine just like any other `async def`: if you do not `await` it, it does
not execute. Use `await` inside async handlers.

## Calling sync code inside an async handler

If you must, hand it to a thread so the loop keeps running:

```python
import asyncio

@bot.on_command("report")
async def report(bot, event):
    await asyncio.to_thread(bot.get_me)      # sync form in a separate thread
```

Prefer rewriting the call as `await`.

## Comparing with the original library

maxrubika derived sync behaviour from the same idea. darkob additionally:

- uses a **bounded** executor for blocking handlers, so a burst of events
  cannot spawn unbounded OS threads;
- rejects a sync call made from inside the worker thread itself (it would
  deadlock otherwise) with a clear `RuntimeError`.

## Shutting down

```python
from darkob.hybrid import close_sync_loop

close_sync_loop()    # optional; also runs at exit
```

Long-running processes rarely need this. Tests that use the sync API
should close the loop so the interpreter exits promptly.

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

Pick one per codebase. Mixing works, but sync calls inside an async
handler block the loop while they wait.

## Calling sync code inside an async handler

If you must, hand it to a thread so the loop keeps running:

```python
import asyncio

@bot.on_command("report")
async def report(bot, event):
    await asyncio.to_thread(bot.get_chats)   # careful: pre-bound args
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

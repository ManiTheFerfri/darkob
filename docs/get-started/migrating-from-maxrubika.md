# Migrating from maxrubika

darkob is a fork of [maxrubika](https://github.com/MEH2RAB/maxrubika).
It keeps the same concepts and most of the same method names, so most
bots port in minutes.

## 1. Change the package name

```bash
pip uninstall maxrubika
pip install darkob
```

```diff
- import maxrubika
- from maxrubika import Bot
+ import darkob
+ from darkob import Bot
```

The exported names are unchanged: `Bot`, `bot`, `Client`, `Messenger`,
`messenger`, `Shad`, `shad`.

## 1b. Or change nothing but the import

If you would rather migrate later, run the existing code through
the compatibility shim — the only change is the import line:

```diff
- from maxrubika import Messenger
+ from darkob.compat.maxrubika import Messenger
```

Everything maxrubika exported is re-exported there, plus the new
darkob APIs, so a half-migrated file still imports cleanly. The
module emits a `DeprecationWarning` on import to remind you it is a
migration aid, not a destination.

## 2. Re-authenticate existing sessions

!!! warning "Old session files will not load"
    darkob derives its session encryption key from a different salt than
    maxrubika, and prefixes session files with `darkob_` instead of
    `maxrubika_`. Existing encrypted sessions, string sessions and bot
    tokens cannot be carried over — log in again and store the new
    credentials.

This is deliberate: a fork should not silently reuse key material from a
different package.

## 3. Behaviour that changed

| Area | Change | Action needed |
| --- | --- | --- |
| Import | No PyPI update check at import | None. Call `darkob.check_for_updates()` if you want it |
| TLS | Verification **on** by default | If you use a proxy that cannot verify upstreams, pass `verify_ssl=False` |
| Errors | Bare `except:` blocks narrowed | Failures you previously never saw may now surface as exceptions — this is intentional |
| Retries | `max_retries` is a per-request budget, not per endpoint | Expect faster failure and fewer duplicate requests |
| Dispatch | Handlers are indexed by update name | None; ordering within a name is preserved |
| Threads | Sync handlers use a bounded executor | None for normal handlers |
| Sessions | Downloads reuse a pooled session | `download_file` now raises `NoConnection` if you never called `start()` |

## 4. New capabilities

- [`Router`](../guides/routers.md) — group handlers into modules
- [`FSMContext`](../guides/fsm.md) — multi-step conversations
- Generated [API reference](../api/bot.md) that matches the runtime

## 5. Verify

```python
import darkob
print(darkob.__version__)   # 0.2.x
```

Then run your bot through its normal path. If something that used to log
and continue now raises, that is the stability work doing its job — open
an issue if the new behaviour is wrong.

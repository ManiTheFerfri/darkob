# Roadmap

Everything here is a code change. No partnerships, no marketing, no
"community initiatives". If an item is not a commit, it is not on this
list.

Status legend: **shipped** · **next** · **planned**

## Where we are

Shipped in 0.1–0.2:

- Indexed dispatch (handlers grouped by update name, built once).
- Bounded retry budget with endpoint rotation, jitter, `429`/`TOO_REQUESTS`
  backoff, and endpoint promotion.
- Pooled HTTP sessions; no per-download TLS handshake.
- TLS verification on by default.
- No network I/O at import.
- Dispatch race removed (`original_event`); background handler failures are
  now logged immediately instead of at GC time.
- `Router`, `FSMContext` + storage backends, `Keyboard` builders, text
  formatting helpers.
- `Bot.reply` / `edit` / `delete`, `Bot.iter_updates`, `Bot.on_error`.
- Session stability: credentials are restored from a saved session,
  sessions live outside the working directory, and an unreadable session
  file is quarantined instead of deleted.
- `get_me` cached on both surfaces (`refresh=True` to bypass).
- `iter_messages` streams a chat page by page instead of buffering
  the whole history.
- `Event.when` returns a timezone-aware UTC datetime.
- `darkob.testing` ships `FakeBot`, `FakeEvent` and `make_message`.
- `py.typed` marker, so editors and type checkers see the annotations.
- 290 tests, CI on 3.9–3.14 + Windows, generated API docs.

## P0 — next

### New methods

| Method | Behaviour | Why |
| --- | --- | --- |
| `iter_messages` | `async for msg in bot.iter_messages(chat, limit=None)` | Cursor handling is the most common source of duplicated and skipped messages. |
| `iter_chats` | `async for chat in bot.iter_chats()` | Same, for the chat list. |
| `iter_members` | `async for member in bot.iter_members(chat)` | Large groups without manual paging. |
| `Bot.reply` | `await bot.reply(event, text)` | One call instead of chat id + `reply_to_message_id`. |
| `Bot.edit` | `await bot.edit(event, text)` | Symmetric with `reply`. |
| `Bot.on_error` | `@bot.on_error` | Global handler for exceptions escaping any handler. |
| `Event.when` | Localised timestamp property | Timestamp parsing is the most repeated snippet in user code. |

### Stability

| Fix | Detail |
| --- | --- |
| Background task exceptions | **shipped** — logged when they happen. |
| Handler state race | **shipped** — `original_event` removed. |
| `StopHandler` from background tasks | Must cancel siblings instead of silently passing. |
| Webhook payload validation | Reject malformed bodies instead of trusting them. |
| `max_retries=0` | Must mean "one attempt"; currently ambiguous. |
| `Client.__del__` during shutdown | `disconnect()` can raise on a closed loop. |

### Faster

Measured, not assumed:

| Item | Result | Status |
| --- | --- | --- |
| Cache `get_me` | Removes a round-trip from every startup and profile read | **shipped** |
| Lazy `rich` import | Measured: `rich` costs ~8 ms of a 603 ms import. Not worth the churn | **rejected** |
| Eager filter regexes | Already eager — `Text`/`TextMatch` compile in `__init__` | **already done** |
| `orjson` when installed | Unmeasured; needs a payload benchmark first | planned |
| Import time | 603 ms total, of which `aiohttp` is 340 ms; `darkob` adds ~260 ms | investigate |

## P1 — planned

### More Bot API methods

- `send_album` / multi-file messages.
- `pin`, `unpin`, `forward` shortcuts on `Event`.
- `get_webhook_info`, `set_webhook`, `delete_webhook` as first-class methods.
- `remove_commands()` — only `set_commands` exists today.
- Input validation and typed results on `get_updates`.

### More Messenger methods

- `iter_messages` / `iter_chats` on the userbot surface.
- `VoiceChat` wrapper with explicit state instead of loose calls.
- `sync_contacts` from a list.
- `ban_many` / `unban_many` returning per-item results instead of
  all-or-nothing.

### Easier coding

| Item | Detail |
| --- | --- |
| `MessageBuilder` | Compose text + metadata + keypad, then `.send()`. |
| Typed event properties | `event.text`, `event.chat_id`, `event.is_group` without `getattr` fallbacks. |
| `Retry` policy object | Per-call overrides instead of only client-wide `max_retries`. |
| `darkob.testing` | `FakeEvent`, `FakeBot`, `make_message()` — no token needed. |
| More `Storage` backends | Redis, SQLite, in-memory TTL. |
| Router middleware | Middleware scoped to a router subtree. |

### Performance targets

Measured with a benchmark harness, not guessed:

| Metric | Target |
| --- | --- |
| Dispatch per event (10 handlers) | < 20 µs |
| Import time | < 300 ms |
| `send_message` overhead over raw `aiohttp` | < 5% |
| Memory per pooled session | unchanged |

### Typing

- `py.typed` marker and full annotations on the public surface.
- `mypy --strict` starting with `router.py`, `fsm.py`, `keyboards.py`,
  `formatting.py`, then the rest.
- Type stubs for `types/event.py` — currently the least discoverable part.

## P2 — larger work

- **Resumable uploads/downloads** with byte-range checkpoints. Large media
  on unstable networks is the top real-world failure.
- **Circuit breaker per endpoint** so a dead data centre stops being tried.
- **Rate-limit governor**: token bucket per chat and global.
- **Offline send queue**: buffer and flush on reconnect.
- **Protocol version tracking** for the Messenger surface, with a
  compatibility table and a fast release path when Rubika changes.
- **Session migration** from `maxrubika` by re-deriving the old key, so
  switching is not a re-login cliff.
- **Benchmark suite in CI** with regression thresholds.

## Known issues ledger

| Issue | Severity | Status |
| --- | --- | --- |
| `darkob.bot` is the Bot class alias, shadowing the `darkob.bot` package for `import darkob.bot.x as y` | Low | Documented; renaming would break users |
| `Shad` mirrors `Messenger` by construction, not by test | Medium | Planned |
| Handlers are re-registered on every `apply()` call | Low | Planned |
| `Client` is deprecated but still exported | Low | Planned |
| 43 unused imports in the inherited tree | Low | Planned (extend ruff `F401`) |

## Non-goals

- GUI, hosted runtime, marketplace, plugin directory.
- Anything that mass-messages or scrapes accounts.
- Rewriting the transport again; the current design is measured and sound.

## How work is prioritised

1. A crash or silent failure beats everything.
2. A missing method that forces users to hand-roll beats a new abstraction.
3. Anything that makes generated code shorter beats nothing.
4. Refactors that do not move a metric do not ship.

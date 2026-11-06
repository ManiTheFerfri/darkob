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
| `MessageBuilder` | **shipped** — `darkob.builders` |
| Typed event properties | `event.text`, `event.chat_id`, `event.is_group` without `getattr` fallbacks. |
| `Retry` policy object | **shipped** — honoured by both surfaces |
| `darkob.testing` | `FakeEvent`, `FakeBot`, `make_message()` — no token needed. |
| More `Storage` backends | **shipped** — `SQLiteStorage`, `TTLMemoryStorage` |
| Router middleware | **shipped** — `router.middleware()` |

### Performance targets

Measured with a benchmark harness, not guessed:

| Metric | Target |
| --- | --- |
| Dispatch per event (10 handlers) | < 20 µs |
| Import time | < 300 ms |
| `send_message` overhead over raw `aiohttp` | < 5% |
| Memory per pooled session | unchanged |

### Typing

- `py.typed` marker shipped and verified inside the wheel.
- `mypy --strict` on `router.py`, `retry.py`, `builders.py`,
  `keyboards.py`, `formatting.py` and `testing.py` — **enforced in CI**.
- Full annotations across the inherited tree: still pending.

## Official Bot API parity

Audited against <https://rubika.ir/botapi> (methods, models and
group/channel pages). The documentation defines **18 methods**:

`sendMessage`, `editMessageText`, `editChatKeypad`, `sendFile`,
`requestSendFile`, `getFile`, `sendLocation`, `sendContact`, `sendPoll`,
`forwardMessage`, `deleteMessage`, `banChatMember`, `unbanChatMember`,
`getChat`, `getMe`, `getUpdates`, `setCommands`, `updateBotEndpoints`.

Every one of them is implemented, and every endpoint string matches.

Two methods exist in darkob that the public docs do not list:
`getChatMember` and `editMessageKeypad`. They are kept — removing a
working method because a page omits it would break users — but they are
undocumented upstream, so treat them as unsupported by Rubika.

### Live verification

Run against a real bot in a real chat (`scripts/conformance.py` and the
one-off probes behind these numbers):

| Verified working against the API | |
| --- | --- |
| `getMe` | returns bot id, title, username |
| `getUpdates` | returns updates with `next_offset_id` |
| `getChat` | returns the chat object |
| `sendMessage` | returns `data.message_id` |
| `editMessageText` | `OK` |
| `editMessageKeypad` | `OK` |
| `forwardMessage` | `OK` |
| `deleteMessage` | `OK` |
| `sendLocation` / `sendContact` / `sendPoll` | `OK` |
| `requestSendFile` | returns an upload URL |
| `uploadFile` | returns a `file_id` |
| `getFile` | returns `download_url` |
| `sendFile` by `file_id` and by local path | `OK` |
| `editChatKeypad` / `remove_chat_keypad` | `OK` |
| `banChatMember` / `unbanChatMember` | reject bogus ids, so the endpoints exist |

Not verifiable with a bot-only token:

- `setCommands` — there is no `getCommands`, so any write destroys the
  original list with no way to restore it.
- `updateBotEndpoints` — changes where the bot receives updates.
- `getChatMember`, `member_is_admin`, `member_is_joined`,
  `member_is_owner` — our validator (correctly) rejects `b0` chats, so
  these need a group or channel to test. Still unproven.

### The documentation is wrong in one place

The reference page has a section headed **`editMessageKeypad`**, but its
cURL/Python/Node samples POST to **`editInlineKeypad`**. Live probing:

```
POST editInlineKeypad  -> {"status": "INVALID_INPUT", "dev_message": "Invalid Method"}
POST editMessageKeypad -> {"status": "OK", "data": {}}
```

The prose is right and the samples are stale. darkob calls
`editMessageKeypad`, and a regression test pins it.

### Fixed by the audit

- `edit_message` now accepts `inline_keypad`. The docs list it for
  `editMessageText`; darkob previously ignored it, so a handler could not
  change buttons after a callback.
- `remove_commands()` added, matching the documented `setCommands` with an
  empty `bot_commands` list.

### Confirmed absent from the API

These were previously listed as "awaiting documentation". The audit shows
the endpoints do not exist, so they are settled rather than pending:

| Feature | Reality |
| --- | --- |
| `send_album` | No multi-file endpoint; use several `send_file` calls |
| `set_webhook` / `get_webhook_info` / `delete_webhook` | No such endpoints; `updateBotEndpoints` registers a URL but exposes no read/delete |
| Bot-side `pin_message` / `unpin_message` | Not part of the Bot API |
| `sync_contacts` | Messenger-only; the Bot API has no contact sync |

## P2 — larger work

All four items are shipped:

- **Resumable downloads** — **shipped**. `download_file` streams to disk,
  resumes from the existing byte count with a `Range` request, and handles
  a server that ignores the range by restarting instead of appending. If
  the file is already complete the server's `416` is treated as success.
- **Circuit breaker per endpoint** — **shipped**.
- **Rate-limit governor** — **shipped**.
- **Offline send queue** — **shipped**. `SendQueue` sends immediately when
  it can, otherwise keeps the message (optionally on disk) and flushes on
  reconnect. Permanent errors are dropped rather than blocking the queue.
- **Protocol-version tracker** — **shipped**. `ProtocolTracker` snapshots
  the discovered data-centre layout and reports endpoint, socket, platform
  or app-version drift.

Uploads cannot be made resumable: `requestSendFile` returns a `file_id`
only for a complete body, so there is no chunked upload endpoint to build
on.

## Official Bot API parity

Audited against <https://rubika.ir/botapi> (methods, models and
group/channel pages). The documentation defines **18 methods**:

`sendMessage`, `editMessageText`, `editChatKeypad`, `sendFile`,
`requestSendFile`, `getFile`, `sendLocation`, `sendContact`, `sendPoll`,
`forwardMessage`, `deleteMessage`, `banChatMember`, `unbanChatMember`,
`getChat`, `getMe`, `getUpdates`, `setCommands`, `updateBotEndpoints`.

Every one of them is implemented, and every endpoint string matches.

Two methods exist in darkob that the public docs do not list:
`getChatMember` and `editMessageKeypad`. They are kept — removing a
working method because a page omits it would break users — but they are
undocumented upstream, so treat them as unsupported by Rubika.

### Live verification

Run against a real bot in a real chat (`scripts/conformance.py` and the
one-off probes behind these numbers):

| Verified working against the API | |
| --- | --- |
| `getMe` | returns bot id, title, username |
| `getUpdates` | returns updates with `next_offset_id` |
| `getChat` | returns the chat object |
| `sendMessage` | returns `data.message_id` |
| `editMessageText` | `OK` |
| `editMessageKeypad` | `OK` |
| `forwardMessage` | `OK` |
| `deleteMessage` | `OK` |
| `sendLocation` / `sendContact` / `sendPoll` | `OK` |
| `requestSendFile` | returns an upload URL |
| `uploadFile` | returns a `file_id` |
| `getFile` | returns `download_url` |
| `sendFile` by `file_id` and by local path | `OK` |
| `editChatKeypad` / `remove_chat_keypad` | `OK` |
| `banChatMember` / `unbanChatMember` | reject bogus ids, so the endpoints exist |

Not verifiable with a bot-only token:

- `setCommands` — there is no `getCommands`, so any write destroys the
  original list with no way to restore it.
- `updateBotEndpoints` — changes where the bot receives updates.
- `getChatMember`, `member_is_admin`, `member_is_joined`,
  `member_is_owner` — our validator (correctly) rejects `b0` chats, so
  these need a group or channel to test. Still unproven.

### The documentation is wrong in one place

The reference page has a section headed **`editMessageKeypad`**, but its
cURL/Python/Node samples POST to **`editInlineKeypad`**. Live probing:

```
POST editInlineKeypad  -> {"status": "INVALID_INPUT", "dev_message": "Invalid Method"}
POST editMessageKeypad -> {"status": "OK", "data": {}}
```

The prose is right and the samples are stale. darkob calls
`editMessageKeypad`, and a regression test pins it.

### Fixed by the audit

- `edit_message` now accepts `inline_keypad`. The docs list it for
  `editMessageText`; darkob previously ignored it, so a handler could not
  change buttons after a callback.
- `remove_commands()` added, matching the documented `setCommands` with an
  empty `bot_commands` list.

### Confirmed absent from the API

These were previously listed as "awaiting documentation". The audit shows
the endpoints do not exist, so they are settled rather than pending:

| Feature | Reality |
| --- | --- |
| `send_album` | No multi-file endpoint; use several `send_file` calls |
| `set_webhook` / `get_webhook_info` / `delete_webhook` | No such endpoints; `updateBotEndpoints` registers a URL but exposes no read/delete |
| Bot-side `pin_message` / `unpin_message` | Not part of the Bot API |
| `sync_contacts` | Messenger-only; the Bot API has no contact sync |

## P2 — larger work

- **Resumable uploads/downloads**: downloads now borrow the pooled
  session (they used to open their own, one TLS handshake per file)
  and were verified against the live API. Byte-range resume is still
  to do; uploads cannot resume because the endpoint returns a
  `file_id` only for a complete body.
- **Circuit breaker per endpoint** — **shipped** (`darkob.CircuitBreaker`).
- **Rate-limit governor** — **shipped** (`darkob.RateLimiter`,
  global + per-chat token buckets, applied to every attempt).
- **Offline send queue**: buffer and flush on reconnect.
- **Protocol version tracking** for the Messenger surface, with a
  compatibility table and a fast release path when Rubika changes.
- **Session migration** from `maxrubika` by re-deriving the old key, so
  switching is not a re-login cliff.
- **Benchmark suite in CI** with regression thresholds.

## Verification

Static review can prove an endpoint name and payload key match the
documentation. It cannot prove the server accepts them. Two tools
bridge that gap:

- `scripts/benchmark.py` — measures the library's own overhead.
- `scripts/conformance.py` — calls every Bot API method against a
  real token, reports pass/fail/skip per method, cleans up after
  itself, and exits non-zero on failure.

Run the conformance check before tagging a release:

```bash
export DARKOB_BOT_TOKEN=...
export DARKOB_CHAT_ID=g0...
python scripts/conformance.py --writes
```

## v1.0 groundwork (Phases 2, 3, 6)

- **Latency-aware failover.** Each endpoint keeps an exponential
  moving average of its response time; candidates are ordered
  healthy-first, fastest-first, with discovery order as the
  tie-break. Combined with the circuit breaker, a slow or dead node is
  demoted instead of being retried blindly.
- **Flood ceiling.** `Client(flood_sleep_threshold=60)` refuses to
  sleep through a long rate-limit wait: above the ceiling the request
  fails fast with a log line instead of hanging a handler.
- **WebSocket gap recovery.** After a reconnect the client pulls
  missed updates before resuming the live stream.
- **Crypto engine.** `darkob.CryptoEngine` caches the AES key, IV and
  parsed RSA signer for the session, and payloads at or above 256 KB
  are encrypted on a worker thread so the loop keeps serving handlers.
- **`darkob.compat.maxrubika`.** A one-import migration shim.

## v1.0 groundwork (Phase 4)

- **`bot.ask()` / `client.ask()`.** Await the next matching message in
  a chat; the reply is consumed before normal dispatch, so a two-step
  flow needs no state flag. Filters, timeouts (`NoReply`) and a prompt
  with a keypad are supported.
- **`StatesGroup` / `State`.** Declarative, namespaced conversation
  states that are `str` subclasses, so they work with every existing
  storage backend and `StateFilter` unchanged.

## v1.0 groundwork (Phase 1)

- **Dependency diet.** `mutagen` and `rich` are no longer core
  dependencies. `async with`-style console output falls back to a
  tiny stand-in, and media metadata is parsed from binary headers.
  No public method or export was removed (verified by diffing the
  public surface against the previous release: Bot 49, Messenger
  329, Shad 330, exports 43 — identical).
- **`darkob.utils.media_parser`.** PNG, JPEG, GIF, WebP, MP3 and
  MP4 header parsing in pure Python: dimensions, duration, bitrate,
  sample rate and the ID3 artist, in memory, in about 0.8 us for a
  PNG.
- **`darkob.utils.json_backend`.** Uses `msgspec` when installed and
  falls back to the standard library otherwise; wired into the
  cipher and the Bot request path.
- **Optional extras:** `darkob[speed]` (msgspec) and `darkob[cli]`
  (rich).

## Closed after the deep audit

- Webhook requests can now be authenticated with a shared secret;
  previously any POST was dispatched as an update.
- Inbound updates (webhook and WebSocket) run under a semaphore;
  the keep-alive loop can no longer be started twice.
- The last five per-call `ClientSession` sites now borrow the pooled
  session, so no path pays a fresh TLS handshake.
- `Data` builds a key index on first access: deep payload lookups
  went from 3.9 us to 0.5 us, which matters because an Event
  exposes ~40 such properties.
- Nineteen silent `except: pass` blocks now log at debug level; the
  one that remains is `__del__`, where logging can itself fail.
- `ruff` F401 is enabled, so unused imports cannot accumulate.
- CI fails if coverage drops below 30%.

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

# Roadmap

Everything here is a code change. No partnerships, no marketing, no
"community initiatives". If an item is not a commit, it is not on this list.

Status legend: **shipped** · **next** · **planned** · **rejected**

## Where we are

Shipped through 0.19:

**Speed**

- Indexed dispatch: handlers are grouped by update name once, so routing cost
  scales with the handlers that match, not the handlers that exist.
- Payload key index built on first access; deep lookups dropped from 3.9 µs to
  0.5 µs, which matters because an `Event` exposes ~40 such properties.
- Multi-key lookups (`event.text` searches `text` then `caption`) are served
  from the same index instead of walking the structure.
- Memoised update-name capitalisation; a pending `ask()` costs one integer
  check per update rather than an `Event` construction.
- Latency-aware endpoint ordering and a per-endpoint circuit breaker.
- Bounded retry budget for the whole request, not per endpoint.
- Pooled HTTP sessions; no per-download TLS handshake.
- Payloads at or above 256 KB are encrypted on a worker thread.

**Upstream v1.18.0 / v1.18.1 (new in 0.19.x)**

- Merged upstream's grouped endpoints and new `Rubino`, `RubiAI`, `RubikaTV`
  surfaces without deleting a pre-existing method or any of darkob's hardening.
- Preserved darkob's request signatures, `send_message` file/sticker dispatch,
  `download_file` return types and both `.max` and legacy session formats.
- Bounded Rubino retries globally; forwarded proxy/timeout and TLS settings on
  every new surface; offloaded media parsing from the event loop.
- Generated references for all six clients and added offline coverage for old
  call shapes, new transport behavior and legacy session migration.

**Reliability**

- Flood ceiling: `flood_sleep_threshold` refuses to sleep through a long
  rate-limit wait instead of hanging a handler.
- WebSocket gap recovery after a reconnect.
- `SendQueue` for durable outbound messages.
- `RateLimiter` (global + per-chat token buckets) and, new in 0.18,
  `AdaptiveRateLimiter` — additive-increase/multiplicative-decrease control
  that reacts to real `429`/`TOO_REQUESTS` responses and honours
  `Retry-After`.
- Session stability: credentials restored from a saved session, sessions kept
  outside the working directory, an unreadable file quarantined rather than
  deleted.
- TLS verification on by default; no network I/O at import.
- Background handler failures are logged when they happen, not at GC time.
- Webhook requests can be authenticated with a shared secret.

**Ergonomics**

- `Router`, `FSMContext` + four storage backends, `Keyboard` builders, text
  formatting helpers, `MessageBuilder`.
- `Bot.reply` / `edit` / `delete`, `Bot.iter_updates`, `Bot.on_error`,
  `iter_messages` streaming page by page.
- `bot.ask()` inline conversations with filters, timeouts and a prompt keypad.
- `StatesGroup` / `State`, declarative and `str`-compatible.
- `darkob.testing` — `FakeBot`, `FakeEvent`, `make_message()`, no token
  needed.
- `darkob.compat.maxrubika` one-import migration shim.

**Production readiness (new in 0.18)**

- `darkob.metrics` — counters, gauges and bounded histograms, with a
  Prometheus text renderer. Disabled by default; the instrumentation costs one
  attribute read per hot-path call when off.
- `darkob.health` — liveness/readiness registry with a dependency-free ASGI
  app and an aiohttp handler.
- `darkob.plugin` — plugin development kit. The inherited manager gained four
  pipeline hooks (`on_update`, `before_request`, `after_response`, `on_error`)
  that the client actually calls, plus `PluginTester`.
- `darkob.utils.concurrency` — `TaskGroup` and `timeout_after` that work on
  3.9 through 3.14.

**Process**

- 800 tests, CI on 3.9–3.14 plus Windows, generated API docs for all six
  clients, `py.typed`.
- `benchmarks/benchmark_suite.py` (head-to-head) and `benchmarks/scenarios.py`
  (realistic load), with `check_regression.py` gating CI.
- Every `>>>` docstring example is executed in CI, with a ratchet so examples
  cannot be quietly deleted.
- Community health files, security policy, issue/PR templates, Dependabot.

## Next

### Correctness

| Fix | Detail |
| --- | --- |
| `StopHandler` from a background task | Must cancel siblings instead of silently passing. |
| Webhook payload validation | Reject malformed bodies instead of trusting them. |
| `max_retries=0` | Must mean "one attempt"; currently ambiguous. |
| `Client.__del__` during shutdown | `disconnect()` can raise on a closed loop. |

### Documentation

| Item | Detail |
| --- | --- |
| Docstring examples | 24 runnable examples against ~2,000 public members. The harness and the ratchet are in place; the backlog is real and large. Drive it up module by module, starting with the modules an autocomplete hits first. |

### Performance

| Item | Detail | Status |
| --- | --- | --- |
| `orjson` when installed | Needs a payload benchmark before it is worth a dependency. | planned |
| Import time | `aiohttp` is 340 ms of it; `darkob` adds ~260 ms. | investigate |
| Lazy `rich` import | Measured at ~8 ms of a 603 ms import. Not worth the churn. | **rejected** |

## Planned

### More Bot API methods

- `send_album` — **not possible**: the API has no multi-file endpoint.
- `pin` / `unpin` shortcuts on `Event` — the Bot API has no pin endpoint.
- Webhook management methods — **not possible**: `updateBotEndpoints` registers
  a URL but exposes no read, update or delete.

The list above is what an earlier roadmap wanted. The API does not have those
endpoints, so they are settled rather than pending.

### More Messenger methods

- `iter_messages` / `iter_chats` on the userbot surface.
- A `VoiceChat` wrapper with explicit state instead of loose calls.
- `sync_contacts` from a list.
- `ban_many` / `unban_many` returning per-item results instead of all-or-nothing.

### Performance targets

Measured, not guessed:

| Metric | Target | Status |
| --- | --- | --- |
| Dispatch per event (10 handlers) | < 20 µs | met |
| `send_message` overhead over raw `aiohttp` | < 5% | met |
| Import time | < 300 ms | not met (~600 ms) |
| Memory per pooled session | unchanged | met |

### Typing

- `py.typed` shipped and verified inside the wheel.
- `mypy --strict` on `router.py`, `retry.py`, `builders.py`, `keyboards.py`,
  `formatting.py`, `testing.py` — **enforced in CI**.
- `pyright` clean on the curated modules — **enforced in CI**.
- Full annotations across the inherited tree: still pending, and it is the
  last real blocker before 1.0.

## Official Bot API parity

Audited against <https://rubika.ir/botapi>. The documentation defines **18
methods**:

`sendMessage`, `editMessageText`, `editChatKeypad`, `sendFile`,
`requestSendFile`, `getFile`, `sendLocation`, `sendContact`, `sendPoll`,
`forwardMessage`, `deleteMessage`, `banChatMember`, `unbanChatMember`,
`getChat`, `getMe`, `getUpdates`, `setCommands`, `updateBotEndpoints`

Every one is implemented and every endpoint string matches. Two methods exist
in darkob that the public docs do not list: `getChatMember` and
`editMessageKeypad`. They are kept — removing a working method because a page
omits it would break users — but treat them as unsupported upstream.

### Live verification

Run against a real bot in a real chat with `scripts/conformance.py`:

| Verified against the API | |
| --- | --- |
| `getMe` | returns bot id, title, username |
| `getUpdates` | returns updates with `next_offset_id` |
| `getChat` | returns the chat object |
| `sendMessage` | returns `data.message_id` |
| `editMessageText` | `OK` |
| `editMessageKeypad` | `OK` |
| `forwardMessage` / `deleteMessage` | `OK` |
| `sendLocation` / `sendContact` / `sendPoll` | `OK` |
| `requestSendFile` | returns an upload URL |
| `uploadFile` | returns a `file_id` |
| `getFile` | returns `download_url` |
| `sendFile` by `file_id` and by local path | `OK` |
| `editChatKeypad` / `remove_chat_keypad` | `OK` |
| `banChatMember` / `unbanChatMember` | reject bogus ids, so the endpoints exist |

Still unproven, and honestly labelled as such:

- `setCommands` — there is no `getCommands`, so a write destroys the original
  list with no way to restore it. `remove_commands()` exists for the same
  reason.
- `updateBotEndpoints` — changes where the bot receives updates.
- `getChatMember`, `member_is_admin`, `member_is_joined`, `member_is_owner` —
  the validator correctly rejects `b0` chats, so these need a group or channel.

The nightly `conformance` workflow runs this against a live token and files an
issue when it breaks, which is how API drift gets noticed without anyone
watching.

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

- `edit_message` accepts `inline_keypad`. The docs list it for
  `editMessageText`; darkob previously ignored it, so a handler could not
  change buttons after a callback.
- A bare `Payment` button is rejected by the server; `Button.payment()` now
  demands its fields instead of failing at send time.

## Larger work

- **Resumable downloads** — **shipped**. Streams to disk, resumes with a
  `Range` request, restarts if the server ignores the range, treats `416` as
  success.
- **Circuit breaker per endpoint** — **shipped**.
- **Rate-limit governor** — **shipped**, and now adaptive.
- **Offline send queue** — **shipped**.
- **Protocol tracker** — **shipped**. `ProtocolTracker` snapshots the
  discovered data-centre layout and reports endpoint, socket, platform or
  app-version drift.
- **Session migration from maxrubika** by re-deriving the old key, so
  switching is not a re-login cliff.
- **Benchmark suite in CI with regression thresholds** — **shipped**.

Uploads cannot be made resumable: `requestSendFile` returns a `file_id` only
for a complete body, so there is no chunked upload endpoint to build on.

## Verification tools

Static review can prove an endpoint name and payload key match the
documentation. It cannot prove the server accepts them. Three tools bridge
that gap:

- `benchmarks/benchmark_suite.py` — head-to-head against maxrubika.
- `benchmarks/scenarios.py` — realistic load, calibration-normalised.
- `scripts/conformance.py` — calls every Bot API method against a real token,
  reports pass/fail/skip per method, cleans up after itself, and exits
  non-zero on failure. Run it before tagging a release.

```bash
export DARKOB_BOT_TOKEN=...
export DARKOB_CHAT_ID=g0...
python scripts/conformance.py --writes
```

## Known issues ledger

| Issue | Severity | Status |
| --- | --- | --- |
| `darkob.bot` is the Bot class alias, shadowing the `darkob.bot` package for `import darkob.bot.x as y` | Low | Documented; renaming would break users |
| Docstring examples cover a small fraction of the public API | Medium | Harness + ratchet shipped; backlog open |
| `Shad` mirrors `Messenger` by construction, not by test | Medium | Planned |
| Handlers are re-registered on every `apply()` call | Low | Planned |
| `Client` is deprecated but still exported | Low | Planned |
| Free-threaded (`--disable-gil`) Python is untested | Low | Documented as unsupported |

## Non-goals

- GUI, hosted runtime, marketplace, plugin directory.
- Anything that mass-messages or scrapes accounts.
- Rewriting the transport again; the current design is measured and sound.

## How work is prioritised

1. A crash or silent failure beats everything.
2. A missing method that forces users to hand-roll beats a new abstraction.
3. Anything that makes generated code shorter beats nothing.
4. Refactors that do not move a metric do not ship.
5. A number in the README that cannot be reproduced is a bug.

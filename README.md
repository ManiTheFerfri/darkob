<p align="center">
  <img src="https://manitheferfri.github.io/darkob/assets/darkob-logo.png" alt="darkob" width="140"/>
</p>

<h1 align="center">darkob</h1>

<p align="center">
  <b>Fast, stable async Python for the Rubika &amp; Shad platforms.</b><br/>
  Bots and userbots that stay up — with an API verified against the real server.
</p>

<p align="center">
  <a href="https://pypi.org/project/darkob/"><img src="https://shieldcn.dev/pypi/darkob.svg" alt="PyPI"></a>
  <img src="https://shieldcn.dev/badge/python-3.9--3.14-4f46e5.svg" alt="Python 3.9-3.14">
  <a href="https://github.com/ManiTheFerfri/darkob/actions/workflows/ci.yml"><img src="https://shieldcn.dev/github/ci/ManiTheFerfri/darkob.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://shieldcn.dev/github/license/ManiTheFerfri/darkob.svg" alt="License"></a>
  <a href="https://github.com/ManiTheFerfri/darkob/stargazers"><img src="https://shieldcn.dev/github/stars/ManiTheFerfri/darkob.svg" alt="Stars"></a>
</p>

<p align="center">
  <a href="https://manitheferfri.github.io/darkob/"><b>Docs</b></a> ·
  <a href="https://manitheferfri.github.io/darkob/llms-full.txt">AI context</a> ·
  <a href="https://pypi.org/project/darkob/">PyPI</a> ·
  <a href="https://manitheferfri.github.io/darkob/roadmap/">Roadmap</a>
</p>

---

```bash
pip install darkob
```

```python
from darkob import Bot, Keyboard

bot = Bot(token="YOUR_BOT_TOKEN")

@bot.on_command("start")
async def start(bot, event):
    await event.reply(
        "Welcome 👋",
        inline_keypad=Keyboard().row("Docs", "Support"),
    )

bot.run()
```

---

## Why darkob

A fork of [maxrubika](https://github.com/MEH2RAB/maxrubika), rebuilt so
failures are visible, the fast paths are actually fast, and the API surface
matches the server.

| Inherited problem | What darkob does |
| --- | --- |
| Contacted PyPI at import time | Importing performs **no network I/O** |
| TLS verification disabled everywhere | Verification **on by default**, opt-out explicit |
| Bare `except:` swallowed `KeyboardInterrupt` | Narrowed to `Exception`, and logged |
| Background handler crashes vanished at GC | Logged the moment they happen |
| Every event scanned all handlers | **Indexed dispatch**, built once |
| Retries were `endpoints × max_retries` | **Bounded budget** with jitter and `429` handling |
| A new TLS handshake per download | **Pooled sessions** everywhere, including files |
| Saved sessions opened but never read | Credentials **restored**; sessions survive restarts |
| A corrupt session file was deleted | **Quarantined**, never destroyed |
| Keypad editing called a non-existent endpoint | Fixed by live testing, pinned by a regression test |

## What's inside

<table>
<tr><td width="50%" valign="top">

**Two surfaces, one library**

`Bot` for the official Bot API. `Messenger` for real user accounts —
channels, groups, voice chats, settings. `Shad` is the same protocol
against Shad's hosts.

</td><td width="50%" valign="top">

**Async first, sync friendly**

Every method works with `await` or without it. One background loop, no
per-call threads.

</td></tr>
<tr><td valign="top">

**Handlers, filters, routers**

Decorators, 42 filters composing with `&`, `|`, `~`, middleware, nested
routers, and a global `on_error` handler.

</td><td valign="top">

**Conversations**

`FSMContext` with four storage backends: memory, TTL memory, JSON file,
and SQLite (WAL, concurrent-safe).

</td></tr>
<tr><td valign="top">

**Keyboards for every button type**

`Keyboard().row(...)` builders for all **19 documented button types** —
selection, calendar, number/string pickers, location, textbox, barcode,
camera and gallery variants.

</td><td valign="top">

**Message helpers**

`MessageBuilder` for text + keypad + reply target, `bold()` / `link()` /
`code()` formatting, and `event.reply(...)` shortcuts.

</td></tr>
<tr><td valign="top">

**Iterators, not pagination loops**

`bot.iter_updates()` and `client.iter_messages()` own the cursor and stop
when it stops advancing.

</td><td valign="top">

**Testing toolkit**

`darkob.testing` ships `FakeBot`, `FakeEvent` and `make_message`, so a
handler test needs no token and no network.

</td></tr>
</table>

## Reliability

Six primitives that most bot libraries leave to the user:

| Primitive | What it buys you |
| --- | --- |
| `Retry(attempts=, backoff=, jitter=)` | A policy you can reason about, honoured by both surfaces |
| `RateLimiter(rate=, per_chat_rate=)` | Token buckets globally and per chat, applied to every attempt |
| `CircuitBreaker` | A dead data centre stops burning your retry budget |
| `SendQueue(path=)` | Messages survive a dropped connection and flush on reconnect |
| `ProtocolTracker` | Reports when Rubika reshuffles its endpoints |
| Resumable downloads | Byte-range resume that survives an interrupted file |

```python
from darkob import Bot, RateLimiter, Retry, SendQueue

bot = Bot(
    token="...",
    retry=Retry(attempts=4, backoff=0.5),
    rate_limiter=RateLimiter(rate=20, per_chat_rate=3),
)

outbox = SendQueue(bot, path="outbox.json")
outbox.start()
```

## Performance

Measured with `benchmarks/benchmark_suite.py` against maxrubika 1.17.0 on the
same machine, each case in a fresh process so neither library inherits the
other's warm state:

| Benchmark | darkob | maxrubika | Result |
| --- | --- | --- | --- |
| Read `event.text` ×20,000 | 13.5 ms | 20.9 ms | **1.5× faster** |
| Nested key lookup ×20,000 | 3.0 ms | 16.8 ms | **5.7× faster** |
| Filter evaluation ×5,000 | 5.1 ms | 10.5 ms | **1.4× faster** |
| Route 5,000 updates, 50 handlers | 160 ms | 344 ms | **2.2× faster** |
| Route 5,000 updates, 500 handlers | 1.50 s | 3.33 s | **2.2× faster** |

Under realistic load (`benchmarks/scenarios.py`, same machine): **17,500
updates/s** routing 1,000 updates against 100 registered handlers, and a 4 MiB
download resumed from 50% completes in **1.9 ms** of library overhead.

Three things carry the difference:

1. **Lookups are indexed.** Every payload builds a key index on first
   access, so `event.text` — which searches `text` then `caption` — no
   longer walks the structure on every read.
2. **Dispatch is an index, not a scan.** Handlers are grouped by update
   name once, so routing cost scales with the handlers that match, not with
   the handlers that exist.
3. **The update name and waiter list are cheap.** `capitalize()` is
   memoised and a pending `ask()` costs one integer check per update.

### Read this before quoting those numbers

The benchmark used to be wrong, and in our favour, which is the worst kind of
wrong. Its dispatch cases registered handlers as
`{handler: MessageUpdates() for _ in range(count)}` — a dict keyed by the
function object, so 500 identical entries collapsed into **one key**. Both
"50 handlers" and "500 handlers" were measuring a single handler, which is why
the two rows previously reported nearly identical times.

With distinct handlers the gap widened rather than narrowed: 1.5× became 2.2×,
because an index only helps once there is something to index. `README` numbers
before 0.18.0 should be discarded.

Two more caveats, stated plainly:

- **Nothing here measures the network.** In a running bot, network latency
  dominates every row. These numbers describe CPU work per update.
- **The dispatch rows measure the client dispatch path** — the one both
  libraries expose identically, which is what makes the comparison fair.
  `darkob.Bot` routes through its own handler registry, which is a linear
  scan rather than an index; it is a different code path and is not what these
  rows time.
- **The micro-benchmarks isolate one code path each.** The 5.7× nested lookup
  is real but applies to a payload shape those properties actually walk; the
  end-to-end gain is smaller. The dispatch rows are the ones you will notice,
  because routing runs on every single update.

CI enforces this: `benchmarks/check_regression.py` fails the build when a
head-to-head factor drops by more than 25%, or a calibration-normalised
scenario ratio rises by more than 75% (wider, because the committed baseline
was recorded on a different platform). See
[`benchmarks/README.md`](benchmarks/README.md) for the methodology, the
recording hardware and the exact commands.

## Verified against the real API

The Bot API documents **19 endpoints**. All are implemented, and **18 were
exercised against a live server** — including the full file round-trip
(`requestSendFile → uploadFile → getFile → sendFile → download`) and
byte-range resume.

That testing caught three things static reading could not:

1. `editInlineKeypad` — the docs' own cURL — answers `INVALID_INPUT: Invalid Method`. The working endpoint is `editMessageKeypad`.
2. A bare `Payment` button is rejected; `Button.payment()` now demands its fields instead of failing at send time.
3. `Bot.download_file` was opening its own HTTP session, paying a fresh TLS handshake per file.

The remaining two gaps are documented rather than guessed: `getChatMember`
needs a group chat to verify, and `setCommands` has no read-back, so
testing it would destroy your command list.

## Documentation

Full site: **[manitheferfri.github.io/darkob](https://manitheferfri.github.io/darkob/)**

| | |
| --- | --- |
| [Quickstart](https://manitheferfri.github.io/darkob/get-started/quickstart/) | Install to running bot in five minutes |
| [Handlers](https://manitheferfri.github.io/darkob/guides/handlers/) · [Filters](https://manitheferfri.github.io/darkob/guides/filters/) | Every decorator and all 42 constraints |
| [Routers](https://manitheferfri.github.io/darkob/guides/routers/) | Split a bot into modules, with scoped middleware |
| [Conversations](https://manitheferfri.github.io/darkob/guides/fsm/) | State, storage backends, `StateFilter` |
| [Keyboards](https://manitheferfri.github.io/darkob/guides/keyboards/) | All button types and formatting |
| [Composing messages](https://manitheferfri.github.io/darkob/guides/composing-messages/) | `MessageBuilder` and formatting together |
| [Errors](https://manitheferfri.github.io/darkob/guides/errors/) | Retries, breaker, rate limiting, queue |
| [Bot API](https://manitheferfri.github.io/darkob/api/bot/) · [Messenger API](https://manitheferfri.github.io/darkob/api/messenger/) | Generated from the package |

## Built for AI-assisted development

Most darkob bots are written by an assistant, so the docs are built to be
read by a model.

```text
https://manitheferfri.github.io/darkob/llms-full.txt
```

One file, one fetch: hard rules, every guide, and the complete API with
full docstrings for all 688 methods.

- [`llms.txt`](https://manitheferfri.github.io/darkob/llms.txt) — curated map
- [`api.json`](https://manitheferfri.github.io/darkob/api.json) — every method as JSON
- Every page is also served as raw Markdown: append `.md` to any URL
- The API reference is generated from the installed package, so it cannot drift

## Development

```bash
git clone https://github.com/ManiTheFerfri/darkob.git
cd darkob
pip install -e ".[dev]"

pytest --cov=darkob     # 463 tests, no network required
ruff check .            # lint
mypy darkob/router.py darkob/retry.py darkob/builders.py \
     darkob/keyboards.py darkob/formatting.py darkob/testing.py
```

The suite never opens a socket: HTTP goes through fake transports, and a
subprocess test asserts that importing `darkob` cannot reach the network.

Two extra tools live in `scripts/`:

- `benchmark.py` — micro-benchmarks for the hot paths, no network.
- `conformance.py` — exercises every Bot API method against a real token,
  cleans up after itself, and exits non-zero on failure.

## Roadmap

See [docs/roadmap.md](docs/roadmap.md) — milestones 1–3 and P0–P2 are
closed. It records what is proven, what is impossible, and why.

## License

MIT. Derived from [maxrubika](https://github.com/MEH2RAB/maxrubika),
copyright MEHRAB Farahmand; the original MIT notice is preserved in
[LICENSE](LICENSE).

Maintained by [Mani Keikhosravi](https://github.com/ManiTheFerfri).

> Not affiliated with Rubika or Shad. Use responsibly and in line with the
> platforms' terms of service.

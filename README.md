<p align="center">
  <img src="assets/darkob-logo.png" alt="darkob" width="180"/>
</p>

<h1 align="center">darkob</h1>

<p align="center">
  <strong>Fast, stable async Python for the Rubika &amp; Shad platforms.</strong><br/>
  Build bots and userbots that stay up, without the boilerplate.
</p>

<p align="center">
  <a href="https://github.com/ManiTheFerfri/darkob/actions/workflows/ci.yml"><img src="https://github.com/ManiTheFerfri/darkob/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/darkob/"><img src="https://img.shields.io/pypi/v/darkob?color=blue" alt="PyPI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT"></a>
  <img src="https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue.svg" alt="Python 3.9-3.14">
  <img src="https://img.shields.io/badge/tests-121%20passing-brightgreen.svg" alt="Tests">
</p>

---

**darkob** (دارکوب, *woodpecker*) is a fork of
[maxrubika](https://github.com/MEH2RAB/maxrubika) by
[MEHRAB Farahmand](https://github.com/MEH2RAB), rebuilt around
foundations you can trust. Same protocol, same power, far less
guesswork when something goes wrong.

```python
from darkob import Bot

bot = Bot(token="YOUR_BOT_TOKEN")

@bot.on_command("start")
async def start(bot, event):
    await event.reply("Welcome 👋")

bot.run()
```

---

## ✨ Why darkob

The upstream library is feature-complete, but its foundations were never
hardened. Speed and new features are only worth having on a base that
does not quietly fail, so darkob starts there.

| Inherited problem | What darkob does instead |
| --- | --- |
| Contacted PyPI at startup (`urlopen` inside the package init) | Importing darkob performs **no network I/O**. The update check is opt-in via `darkob.check_for_updates()`. |
| TLS verification disabled on every connector | Verification is **on by default**; opt out explicitly with `verify_ssl=False`. |
| Bare `except:` swallowed `KeyboardInterrupt` and `SystemExit` | Narrowed to `except Exception:`; session-loading failures are logged rather than silently returning `None`. |
| `Data` used without being imported in the request path | Fixed — that branch would have raised `NameError` at runtime. |
| Every update scanned **all** handlers, rebuilt the update name per handler, and spawned an OS thread per synchronous handler | **Indexed dispatch**: handlers grouped by update name once; blocking handlers run in the loop's bounded executor. |
| Retries were `endpoints × max_retries` — 3 endpoints meant 9 attempts with exponential backoff | **Bounded budget** per request, endpoint rotation, jitter, and explicit `429` / `TOO_REQUESTS` backoff. |
| A fresh `ClientSession` (and TLS handshake) per file download | **Pooled sessions** per file server, reused across downloads. |
| No tests, no CI, no `pyproject.toml` | 121 tests, GitHub Actions across 3.9–3.14 plus Windows, modern packaging. |

## 🚀 Install

```bash
pip install darkob
```

Latest development version:

```bash
pip install git+https://github.com/ManiTheFerfri/darkob.git
```

## 📦 What's inside

- **Two surfaces, one library.** `Bot` talks to the official Bot API;
  `Messenger` drives a real user account, including channels, groups,
  voice chats and stickers. `Shad` is the same Messenger protocol against
  the Shad platform.
- **Async first, sync friendly.** Every method works with `await` or
  without it — darkob runs one background loop and hops onto it for you.
- **Decorator handlers.** `on_message`, `on_command`, `on_callback`,
  `on_edit_message`, and friends, with a composable filter system
  (`&`, `|`, `~`).
- **Routers.** Split a bot into feature modules and include them in one line.
- **Finite state machines.** Multi-step conversations with pluggable
  storage that can survive a restart.
- **Polling or webhook.** `bot.run()` polls; `bot.run(webhook_url=...)`
  serves a webhook instead.

## 🔀 Routers

Handlers can live in their own modules and be registered from one place:

```python
from darkob import Bot, Router

bot = Bot(token="YOUR_BOT_TOKEN")
admin = Router("admin")

@admin.command("ban")
async def ban(bot, event):
    await bot.ban_member(event.chat_id, event.author_id)
    await event.reply("Banned.")

bot.include_router(admin)
bot.run()
```

Routers nest, so a larger bot can keep one root router per feature area.

## 🧠 Conversations (FSM)

Track which step a user is on and remember what they told you:

```python
from darkob import Bot, FSMContext, JsonFileStorage, StateFilter

bot = Bot(token="YOUR_BOT_TOKEN")
storage = JsonFileStorage("fsm.json")   # survives restarts

@bot.on_command("order")
async def order(bot, event):
    ctx = FSMContext(storage, key=event.chat_id)
    await ctx.set_state("address")
    await event.reply("What is your delivery address?")

@bot.on_new_message(StateFilter(storage, "address"))
async def address(bot, event):
    ctx = FSMContext(storage, key=event.chat_id)
    await ctx.update_data(address=event.text)
    await ctx.clear()
    await event.reply("Order received ✅")
```

Swap `JsonFileStorage` for `MemoryStorage` in tests, or implement the
`Storage` interface to back it with Redis or SQL.

## 👤 Userbots

```python
from darkob import Messenger

app = Messenger(auth="...", private_key="...")
```

Authentication, session strings, platforms (`web`, `pwa`, `android`,
`rubx`, `rubino`, …) and the full method surface are covered in the
documentation.

## 📚 Documentation

The exhaustive, method-by-method reference lives in [`docs/`](docs/):

| Area | Start here |
| --- | --- |
| Getting started with bots | [bot-guide](docs/bot-guide.md) |
| Bot methods | [bot-methods](docs/bot-methods.md) |
| Bot filters | [bot-filters](docs/bot-filters.md) |
| Userbot guide | [client-guide](docs/client-guide.md) |
| Userbot methods | [client-methods](docs/client-methods.md) |
| Shad platform | [shad-guide](docs/shad-guide.md) |

Every public method also ships a full docstring:

```python
from darkob import Bot
import inspect

for name in dir(Bot):
    if not name.startswith("_"):
        print(f"{name}: {inspect.getdoc(getattr(Bot, name))}\n")
```

## 🗂 Project layout

```
darkob/
├── bot/          # Bot API surface: endpoint mixins, filters, registry, plugins
├── client/       # Messenger API: chats, groups, channels, messages, settings
├── types/        # Event and update models
├── router.py     # Composable routers
├── fsm.py        # Conversation state + pluggable storage
├── hybrid.py     # Sync/async bridge
└── data.py       # Attribute/item-accessible response wrapper
```

## 🛠 Development

```bash
git clone https://github.com/ManiTheFerfri/darkob.git
cd darkob
pip install -e ".[dev]"

pytest                    # 121 tests, no network required
ruff check .              # lint
pytest --cov=darkob       # coverage
```

The suite never opens a socket: HTTP goes through fake transports, and a
subprocess test asserts that importing `darkob` cannot reach the network.

## 🗺 Roadmap

- [x] Foundation: packaging, TLS, logging, test suite, CI
- [x] Performance: indexed dispatch, bounded retries, pooled sessions
- [x] Routers and FSM
- [ ] Middleware chain on routers
- [ ] Pagination helpers (`async for` over messages and members)
- [ ] Redis storage backend
- [ ] CLI (`darkob new`, `darkob run`)
- [ ] Type-complete public API and `mypy` in CI

## 🤝 Contributing

Issues and pull requests are welcome. Please run `pytest` and
`ruff check .` before opening a PR; CI runs both on every push.

## 📄 License & credits

MIT. darkob is derived from
[maxrubika](https://github.com/MEH2RAB/maxrubika), copyright
MEHRAB Farahmand, and keeps the original MIT notice. See [LICENSE](LICENSE).

Maintained by [Mani Keikhosravi](https://github.com/ManiTheFerfri).

> Not affiliated with Rubika or Shad. Use responsibly and in line with
> the platforms' terms of service.

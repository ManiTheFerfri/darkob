<p align="center">
  <img src="https://manitheferfri.github.io/darkob/assets/darkob-logo.png" alt="darkob" width="140"/>
</p>

<h1 align="center">darkob</h1>

<p align="center">
  <b>Fast, stable async Python for the Rubika & Shad platforms.</b><br/>
  Build bots and userbots that stay up.
</p>

<p align="center">
  <a href="https://pypi.org/project/darkob/"><img src="https://shieldcn.dev/pypi/darkob.svg" alt="PyPI"></a>
  <img src="https://shieldcn.dev/badge/python-3.9--3.14-4f46e5.svg" alt="Python 3.9-3.14">
  <a href="https://github.com/ManiTheFerfri/darkob/actions/workflows/ci.yml"><img src="https://shieldcn.dev/github/ci/ManiTheFerfri/darkob.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://shieldcn.dev/github/license/ManiTheFerfri/darkob.svg" alt="License"></a>
  <a href="https://github.com/ManiTheFerfri/darkob/stargazers"><img src="https://shieldcn.dev/github/stars/ManiTheFerfri/darkob.svg" alt="Stars"></a>
</p>

<p align="center">
  <a href="https://manitheferfri.github.io/darkob/"><b>Documentation</b></a> ·
  <a href="https://manitheferfri.github.io/darkob/llms-full.txt">AI context</a> ·
  <a href="https://pypi.org/project/darkob/">PyPI</a> ·
  <a href="https://github.com/ManiTheFerfri/darkob/issues">Issues</a>
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
    await event.reply("Welcome 👋")

@bot.on_new_message()
async def echo(bot, event):
    await event.reply(event.text, inline_keypad=Keyboard().row("Yes", "No"))

bot.run()
```

---

## Why darkob

A fork of [maxrubika](https://github.com/MEH2RAB/maxrubika), rebuilt so
failures are visible and the fast paths are actually fast.

| Inherited problem | What darkob does |
| --- | --- |
| Contacted PyPI at import time | Importing performs **no network I/O** |
| TLS verification disabled everywhere | Verification **on by default**, opt out explicitly |
| Bare `except:` swallowed `KeyboardInterrupt` | Narrowed to `Exception` and logged |
| Background handler crashes vanished at GC | Logged the moment they happen |
| Every event scanned all handlers | **Indexed dispatch**, built once |
| Retries were `endpoints × max_retries` | **Bounded budget** with jitter and `429` handling |
| A new TLS handshake per file download | **Pooled sessions** per host |
| Saved sessions were opened but never read back | Credentials **restored**; sessions survive restarts |
| A corrupt session file was deleted | **Quarantined**, never destroyed |

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

**Composable handlers**

Decorators, 42 filters with `&`, `|`, `~`, middleware, routers, and a
global `on_error` handler.

</td><td valign="top">

**Conversations that survive restarts**

`FSMContext` with memory or JSON storage, and `StateFilter` to route by
step.

</td></tr>
<tr><td valign="top">

**Shortcuts that save lines**

`event.reply(...)`, `bot.reply(event, text)`, `bot.edit(event, text)`,
`bot.iter_updates()`.

</td><td valign="top">

**Keyboards and formatting**

`Keyboard().row("Yes", "No")` instead of nested dicts. `bold()`,
`italic()`, `link()`, `spoiler()` and friends.

</td></tr>
</table>

## Documentation

Full site: **[manitheferfri.github.io/darkob](https://manitheferfri.github.io/darkob/)**

| | |
| --- | --- |
| [Quickstart](https://manitheferfri.github.io/darkob/get-started/quickstart/) | Install to running bot in five minutes |
| [Handlers](https://manitheferfri.github.io/darkob/guides/handlers/) | Every decorator and what triggers it |
| [Filters](https://manitheferfri.github.io/darkob/guides/filters/) | All 42 constraints and how to compose them |
| [Routers](https://manitheferfri.github.io/darkob/guides/routers/) | Split a bot into modules |
| [Conversations](https://manitheferfri.github.io/darkob/guides/fsm/) | Multi-step flows |
| [Keyboards](https://manitheferfri.github.io/darkob/guides/keyboards/) | Keypads and text formatting |
| [Errors](https://manitheferfri.github.io/darkob/guides/errors/) | Exception hierarchy and retries |
| [Bot API](https://manitheferfri.github.io/darkob/api/bot/) · [Messenger API](https://manitheferfri.github.io/darkob/api/messenger/) | Generated from the package |
| [Roadmap](https://manitheferfri.github.io/darkob/roadmap/) | What ships next, and what will not |

## Built for AI-assisted development

Most darkob bots are written by an assistant, so the docs are built to be
read by a model.

```text
https://manitheferfri.github.io/darkob/llms-full.txt
```

That single file is the whole thing: hard rules, every guide, and the full
API with complete docstrings for all 688 methods — **318 KB**, one fetch,
no follow-up links.

- [`llms.txt`](https://manitheferfri.github.io/darkob/llms.txt) — curated map
- [`api.json`](https://manitheferfri.github.io/darkob/api.json) — every method as JSON
- Every page is also served as raw Markdown: append `.md` to any URL
- The API reference is generated from the installed package, so it cannot
  drift from the code

## Development

```bash
git clone https://github.com/ManiTheFerfri/darkob.git
cd darkob
pip install -e ".[dev]"

pytest --cov=darkob    # 290 tests, no network required
ruff check .           # lint
```

The suite never opens a socket: HTTP goes through fake transports, and a
subprocess test asserts that importing `darkob` cannot reach the network.

## License

MIT. Derived from [maxrubika](https://github.com/MEH2RAB/maxrubika),
copyright MEHRAB Farahmand; the original MIT notice is preserved in
[LICENSE](LICENSE).

Maintained by [Mani Keikhosravi](https://github.com/ManiTheFerfri).

> Not affiliated with Rubika or Shad. Use responsibly and in line with the
> platforms' terms of service.

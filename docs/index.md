# darkob

**Fast, stable async Python for the Rubika & Shad platforms.**
Build bots and userbots that stay up — without the boilerplate.

!!! tip "Writing a bot with an AI assistant? Give it one URL"
    **[https://manitheferfri.github.io/Darkob/llms-full.txt](llms-full.txt)** — this
    single file contains the complete public API with real signatures, the
    full filter catalogue, working patterns and the mistakes to avoid. Tell
    the model: *"read this URL fully, then build me a bot that does X."*
    Nothing else is required.

    Prefer structured data? [`api.json`](api.json) has every method as JSON.

```bash
pip install darkob
```

## 30 seconds to a working bot

```python
from darkob import Bot

bot = Bot(token="YOUR_BOT_TOKEN")

@bot.on_command("start")
async def start(bot, event):
    await event.reply("Welcome 👋")

bot.run()
```

## Start here

| If you want to… | Read |
| --- | --- |
| Install and run something in 5 minutes | [Quickstart](get-started/quickstart.md) |
| Understand handlers, filters and decorators | [Handlers](guides/handlers.md) · [Filters](guides/filters.md) |
| Split a bot into modules | [Routers](guides/routers.md) |
| Build a multi-step conversation | [Conversations (FSM)](guides/fsm.md) |
| Handle failures properly | [Errors](guides/errors.md) |
| Drive a real user account | [API: Messenger](api/messenger.md) |
| Write bots with an AI assistant | [AI workflow](ai/index.md) |
| Look up a method signature | [API: Bot](api/bot.md) · [API: Messenger](api/messenger.md) |

## Built for AI-assisted development

Most darkob bots are written by an AI assistant, so the documentation is
designed to be *read by a model*, not just by a human:

- **[`llms.txt`](llms.txt)** — a curated map of the docs, in the
  [`llms.txt`](https://llmstxt.org/) format.
- **[`llms-full.txt`](llms-full.txt)** — the entire documentation in one
  file, ready to paste into a context window.
- **[`api.json`](api.json)** — every public method as structured JSON:
  name, signature, module, docstring. Machine-readable, no parsing.
- **Every page is also served as raw Markdown** — append `.md` to any
  page URL instead of `.html`.
- **The API reference is generated from the installed package**, so a
  signature in the docs cannot disagree with the signature at runtime.

See [AI workflow](ai/index.md) for the recommended prompts, and
[Recipes](ai/recipes.md) for task-shaped examples you can hand to a model.

## Why darkob

darkob is a fork of [maxrubika](https://github.com/MEH2RAB/maxrubika),
rebuilt around foundations that do not quietly fail.

| Inherited problem | What darkob does |
| --- | --- |
| Contacted PyPI at import time | Importing performs **no network I/O** |
| TLS verification disabled | Verification is **on by default** |
| Bare `except:` swallowed `KeyboardInterrupt` | Narrowed and logged |
| Every event scanned all handlers | **Indexed dispatch** |
| Retries multiplied per endpoint | **Bounded attempt budget** |
| A new TLS handshake per file download | **Pooled sessions** |

See [Migrating from maxrubika](get-started/migrating-from-maxrubika.md) for
the complete list of behavioural differences.

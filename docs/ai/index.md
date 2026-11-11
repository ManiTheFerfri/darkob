# AI-assisted development

Most darkob bots are written by an AI assistant. These docs are built for
that: machine-readable, deterministic, and complete.

## Feed the model context

Pick the smallest input that answers your question:

| Asset | Size | Use it when |
| --- | --- | --- |
| [`api.json`](../api.json) | ~1 MB | You need exact signatures. Structured, greppable |
| [`llms.txt`](../llms.txt) | small | The model needs to know *what exists* and where |
| [`llms-full.txt`](../llms-full.txt) | large | The model must answer anything; paste wholesale |
| `api/bot.md`, `api/messenger.md` | medium | You are working on one surface |

Every page on this site is also available as raw Markdown: replace a pretty
URL's trailing `/` with `.md` (for example `/guides/routers/` →
`/guides/routers.md`). That gives an assistant clean text without navigation.

## The minimum viable prompt

```text
You are writing a chatbot with the Python library `darkob` (v0.19+),
for the Rubika messaging platform.

Rules:
- Import from `darkob`: `from darkob import Bot, Router, FSMContext`.
- Handlers are `async def name(bot, event)` and are registered with
  decorators on a Bot instance.
- Filters come from `darkob.bot.filters`.
- Do not invent methods. If you are unsure of a signature, say so.
- async and sync both work; use `await` consistently.
```

A longer, tested version is in the [prompt pack](prompt-pack.md).

## Rules that prevent most AI mistakes

Models trained on Telegram/Pyrogram confuse the two ecosystems. darkob's
API is different in specific ways, so state them explicitly:

1. **`event`, not `message`.** Handlers receive `(bot, event)`.
2. **`event.chat_id`, not `event.chat.id`.**
3. **Reply with `await event.reply(text)`**, not `message.reply(...)`.
4. **Decorators are bot methods**: `@bot.on_new_message()`, never
   `@dp.message_handler`.
5. **Filters are classes you instantiate**: `IsGroup()`, not `IsGroup`.
6. **There is no `Dispatcher`.** A `Bot` registers and dispatches.
7. **There is no `aiogram`-style `types.Message` class.** Use the `event`
   object you are given.

## Validate what the model writes

```python
import darkob, inspect

# Does the method exist?
assert hasattr(darkob.Bot, "send_message"), "hallucinated method"

# Does the signature match?
print(inspect.signature(darkob.Bot.send_message))
```

Or check `api.json` mechanically:

```python
import json, darkob

api = json.load(open("api.json"))
names = {m["name"] for m in api["classes"]["Bot"]["methods"]}

for method in proposed_methods:
    assert method in names, f"not a real Bot method: {method}"
```

## Generate rather than recall

A workflow that reliably produces working bots:

1. Ask the model to list the handlers it plans to write, with triggers.
2. Paste `llms.txt` so it knows the real surface.
3. Ask for one handler at a time, then run it.
4. On failure, paste the traceback **and** the relevant `api/bot.md`
   section back into the conversation.

## What the model will get wrong without help

| Symptom | Cause | Fix in your prompt |
| --- | --- | --- |
| A hybrid call never executes | The coroutine was created inside async code but never awaited | "Inside async code, hybrid methods return coroutines and must be awaited" |
| `ModuleNotFoundError: maxrubika` | Model defaulted to the upstream package | "The package is darkob; maxrubika is deprecated" |
| Handler never fires | Wrong decorator for the update type | Point it at [Handlers](../guides/handlers.md) |
| Filters never match | Passing the class instead of an instance | "Filters are instantiated: `IsGroup()`" |
| Bot replies to itself or loops | No guard on own messages | Add `FromUser(...)` or an ownership check |

# Handlers

A handler is an async (or plain) function registered on the bot. darkob
calls it as `handler(bot, event)` when a matching update arrives.

## Decorators

All decorators are available on a `Bot` instance.

| Decorator | Fires on |
| --- | --- |
| `@bot.on_new_message()` | Brand-new messages |
| `@bot.on_edit_message()` | Edited messages |
| `@bot.on_delete_message()` | Deleted messages |
| `@bot.on_message()` | Any of new / edit / delete / inline |
| `@bot.on_callback()` | Inline keyboard clicks |
| `@bot.on_command("start")` | Messages that start with a command |
| `@bot.on_update()` | **Any** update the server sends |
| `@bot.on_event_data()` | System events (joins, leaves, pins, …) |
| `@bot.on_bot_joined()` | Bot added to a chat |
| `@bot.on_bot_removed()` | Bot removed from a chat |
| `@bot.on_bot_permissions_changed()` | Bot rights changed |
| `@bot.on_started_bot()` / `@bot.on_stopped_bot()` | Bot lifecycle on the server |
| `@bot.on_start()` / `@bot.on_shutdown()` | Your process starting / stopping |

## Basic handler

```python
@bot.on_new_message()
async def echo(bot, event):
    await event.reply(event.text)
```

## Adding constraints

Every decorator accepts constraints, which decide whether the handler
runs. They compose with `&`, `|` and `~`.

```python
from darkob.bot.filters import IsGroup, IsImage

@bot.on_new_message(IsGroup(), IsImage())
async def group_photo(bot, event):
    await event.reply("Nice picture")
```

See [Filters](filters.md) for the full list.

## Commands

```python
@bot.on_command("start")
@bot.on_command(["start", "begin", "شروع"])
@bot.on_command()                       # any command
@bot.on_command("help", prefixes=["/", "!"])
```

## Editing a message

```python
await bot.edit_message(
    event.chat_id,
    event.message_id,
    "Updated text",
    inline_keypad=Keyboard().row("Done"),
)
```

The inline keypad is optional; omit it to leave the existing buttons
alone.

## Middleware

A middleware wraps dispatch. Call `call_next()` to continue, or return
without calling it to stop the chain.

```python
@bot.middleware()
async def log_everything(bot, event, call_next):
    print("incoming:", getattr(event, "text", ""))
    await call_next()
```

Middlewares run in registration order, outermost first.

## Ordering and stopping

By default every matching handler runs, in registration order. Set
`run_all_handlers=False` on the bot to run only the first match:

```python
bot = Bot(token="...", run_all_handlers=False)
```

A handler that raises does not stop the others; the exception is logged.

## Lifecycle hooks

```python
@bot.on_start()
async def warm_up(bot):
    print("bot is starting")

@bot.on_shutdown()
async def clean_up(bot):
    print("bot is stopping")
```

## Sync handlers

A plain function works too — it is executed in a bounded thread pool so
it cannot block the event loop:

```python
@bot.on_command("ping")
def ping(bot, event):
    bot.send_message(event.chat_id, "pong")
```

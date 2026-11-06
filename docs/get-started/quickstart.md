# Quickstart

## 1. Get a bot token

Create a bot with Rubika's official bot creator and copy the token it
gives you. A valid token looks like 64 uppercase alphanumeric
characters.

## 2. Your first bot

```python
from darkob import Bot

bot = Bot(token="YOUR_BOT_TOKEN")

@bot.on_command("start")
async def start(bot, event):
    await event.reply("Welcome 👋")

@bot.on_new_message()
async def echo(bot, event):
    await event.reply(event.text)

bot.run()
```

`bot.run()` starts long polling and blocks until you stop it with Ctrl+C.

## 3. Send messages from a handler

```python
@bot.on_command("hello")
async def hello(bot, event):
    await bot.send_message(event.chat_id, "Hello!")
```

`event` carries the incoming update:

| Attribute | Meaning |
| --- | --- |
| `event.chat_id` | Conversation to reply in |
| `event.author_id` | User who sent it |
| `event.text` | Message text (`""` when there is none) |
| `event.reply(text)` | Shortcut: send into the same chat |
| `event.forward()`, `event.delete()` | Act on the message |

## 4. Run as a webhook instead

Polling needs no public address; webhooks need one.

```python
bot.run(
    webhook_url="https://example.com/wk",
    host="0.0.0.0",
    port=8080,
)
```

Turbo mode is `bot.run()` with no arguments — it polls every 5 ms by
default, tunable with `poll_interval`.

!!! warning "Always set a webhook secret"
    A webhook URL that leaks lets anyone inject fake updates into
    your bot — a fake `/start`, a fake admin command. darkob cannot
    verify who posted, so agree on a shared secret:

    ```python
    bot = Bot(token="...", webhook_secret="long-random-string")
    bot.run(webhook_url="https://example.com/wk?secret=long-random-string")
    ```

    Requests without a matching `?secret=` or `X-Webhook-Secret`
    header are rejected with `401`. With no secret configured, a
    warning is logged on the first webhook request.

## 5. Tell users what the bot can do

```python
bot.set_commands({
    "start": "Start the bot",
    "help": "Show help",
})
```

## 6. Grow the bot

Once one file stops being enough:

- [Handlers](handlers.md) — every decorator and what triggers it
- [Filters](filters.md) — narrow down which events a handler sees
- [Routers](routers.md) — split handlers into modules
- [Conversations](fsm.md) — multi-step flows
- [Errors](errors.md) — stop silent failures

## Async or not?

Every method works both ways. Without `await`, darkob runs the call on a
background loop and returns the result:

```python
bot = Bot(token="YOUR_TOKEN")
me = bot.get_me()          # blocking, returns the result
me = await bot.get_me()    # async, same result
```

Mixing is safe, but pick one style per codebase. See
[Sync and async](../guides/sync-and-async.md).

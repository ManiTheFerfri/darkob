# Build your first Rubika bot in 10 minutes

A hands-on walkthrough that ends with a bot which echoes, answers one command, and puts a working button under a message.

## 1. Install

```bash
pip install darkob
```

darkob needs Python 3.9 or newer. Confirm the install:

```bash
python -c "import darkob; print(darkob.__version__)"
```

Importing darkob performs no network I/O, so this works offline.

## 2. Get a bot token

Create a bot with Rubika's official bot creator and copy the token it
shows you. A token is 64 characters: five uppercase letters, then 59
characters that are digits or uppercase letters.

!!! warning "The token is a password"
    Anyone holding it can send messages as your bot. Keep it out of the
    repository and read it from the environment instead:

    ```python
    import os
    token = os.environ["RUBIKA_BOT_TOKEN"]
    ```

## 3. A bot that echoes messages

Create `bot.py`:

```python title="bot.py"
from darkob import Bot

bot = Bot(token="YOUR_BOT_TOKEN")

@bot.on_new_message()
async def echo(bot, event):
    await event.reply(event.text)

bot.run()
```

`Bot(...)` validates the token and creates its handler registry; the HTTP
session is opened on first use. `bot.run()` then starts long polling and
blocks until you stop it.

Run it and send the bot any message:

```bash
python bot.py
```

A one-time banner appears, then `Bot started in polling mode...`. The bot
answers with the same text you sent. Stop it with Ctrl+C.

A handler is a plain async function taking two arguments: the bot, and the
event. `event.text` holds the message text, or `None` when the update
carries none, and `event.reply(text)` sends into the same chat as a
threaded reply.

!!! note "A mistyped token does not raise"
    If the token does not match the expected shape, `Bot(...)` asks for
    one interactively in the terminal. A prompt in the middle of a
    deployment log means the token was wrong, not missing.

## 4. Only answer commands

Echoing everything is rarely useful. A filter decides whether a handler
runs, so add one:

```python title="bot.py"
from darkob import Bot
from darkob.bot.filters import Command

bot = Bot(token="YOUR_BOT_TOKEN")

@bot.on_new_message(Command("echo"))
async def echo(bot, event):
    await event.reply(event.command_args or "nothing to echo")

bot.run()
```

Now `/echo hello` replies `hello`, while a plain `hello` is ignored. The
filter matches `/echo` and `/echo@your_bot`, and lets every other command
fall through to other handlers.

`event.command_args` is everything after the command, or `""`.

!!! tip "One decorator instead of two filters"
    `@bot.on_command("echo")` applies the message and command filters for
    you, and takes a list: `@bot.on_command(["echo", "بازگو"])`. Once your
    bot has several commands, that shortcut keeps the code shorter.

## 5. Add an inline keyboard button

Buttons live under the message, so they need an inline keypad. Give each
button an `id`; that id is what comes back when somebody presses it.

```python title="bot.py"
from darkob import Bot, Button, Keyboard

bot = Bot(token="YOUR_BOT_TOKEN")

@bot.on_command("menu")
async def menu(bot, event):
    keypad = Keyboard().row(
        Button("Say hi", id="hi"),
        Button("Docs", id="docs"),
    )
    await bot.send_message(event.chat_id, "Pick one:", inline_keypad=keypad)

@bot.on_callback()
async def on_button(bot, event):
    if event.button_id == "hi":
        await event.reply("Hi there 👋")
    else:
        await event.reply("Docs: https://github.com/ManiTheFerfri/darkob")

bot.run()
```

A press arrives as an `InlineMessage` update, and `@bot.on_callback()`
fires on exactly that. `event.button_id` holds the `id` you set, and
`event.reply(...)` still works because the payload carries the chat and
message it belongs to.

Buttons without an explicit `id` get a numeric one assigned for you
(`"100"`, `"101"`, …). That is fine for a static menu, but an explicit id
is what makes the handler readable.

## 6. Run it

The finished file:

```python title="bot.py"
import os

from darkob import Bot, Button, Keyboard
from darkob.bot.filters import Command

bot = Bot(token=os.environ["RUBIKA_BOT_TOKEN"])

@bot.on_new_message(Command("echo"))
async def echo(bot, event):
    await event.reply(event.command_args or "nothing to echo")

@bot.on_command("menu")
async def menu(bot, event):
    keypad = Keyboard().row(
        Button("Say hi", id="hi"),
        Button("Docs", id="docs"),
    )
    await bot.send_message(event.chat_id, "Pick one:", inline_keypad=keypad)

@bot.on_callback()
async def on_button(bot, event):
    if event.button_id == "hi":
        await event.reply("Hi there 👋")
    else:
        await event.reply("Docs: https://github.com/ManiTheFerfri/darkob")

bot.run()
```

```bash
python bot.py
```

Send `/echo hi`, then `/menu` and press a button. Both handlers fire, in
that order of registration, for events that match them.

## Where to go next

- More decorators and middleware: [Handlers](../guides/handlers.md)
- Narrow handlers by chat, media or text: [Filters](../guides/filters.md)
- Every button type the API accepts: [Keyboards and formatting](../guides/keyboards.md)
- Multi-step conversations: [Conversations (FSM)](../guides/fsm.md)
- Test all of this without a token: [Testing without a token](testing-without-a-token.md)

## See also

- [Quickstart](../get-started/quickstart.md)
- [Installation](../get-started/installation.md)
- [Errors](../guides/errors.md)
- [Testing bots](../guides/testing.md)
- [Architecture](../explanation/architecture.md)

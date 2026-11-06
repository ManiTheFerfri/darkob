# Testing without a token

Write a pytest suite for your handlers with `darkob.testing`: no token, no network and no hand-written stubs.

## 1. Install the test tools

```bash
pip install pytest pytest-asyncio
```

## 2. Turn on auto mode

```ini title="pyproject.toml"
[tool.pytest.ini_options]
asyncio_mode = "auto"
pythonpath = ["."]
```

With `auto`, every `async def test_...` is collected as a coroutine test —
no `@pytest.mark.asyncio` on each function. `pythonpath` puts the project
root on `sys.path`, so a test can `from bot import echo` without
installing your project.

!!! tip "`pytest` versus `python -m pytest`"
    Only `python -m pytest` adds the current directory to `sys.path` by
    itself. Keep `pythonpath = ["."]` in the config and both commands
    behave the same.

## 3. Meet the two fakes

`darkob.testing` ships the two objects a handler test needs:

| Object | What it does |
| --- | --- |
| `FakeBot()` | Records every method call; any method returns `{"status": "OK", "method": name}` |
| `make_message(text=..., chat_id=...)` | Builds a `FakeEvent` that records `reply`, `edit` and `delete` |

`FakeBot` answers to *any* attribute, so you never have to stub the one
method your handler happens to call.

## 4. A complete test file

Handlers are plain async functions, so a test needs a bot to register them
and an event to pass in. Both are cheap to build:

```python title="tests/test_echo.py"
from darkob import Bot
from darkob.bot.filters import Command
from darkob.testing import FakeBot, make_message

# Valid token *shape* only. Nothing connects, so no real token is needed.
TOKEN = "ABCDE" + "0" * 59


def build_echo_handler():
    bot = Bot(token=TOKEN, show_welcome=False)

    @bot.on_new_message(Command("echo"))
    async def echo(bot, event):
        await event.reply(event.command_args or "nothing to echo")

    return echo


async def test_echo_replies_with_the_arguments():
    echo = build_echo_handler()
    event = make_message(text="/echo hi", command_args="hi")

    await echo(FakeBot(), event)

    assert event.replies == ["hi"]


async def test_echo_falls_back_when_there_are_no_arguments():
    echo = build_echo_handler()
    event = make_message(text="/echo", command_args="")

    await echo(FakeBot(), event)

    assert event.replies == ["nothing to echo"]


async def test_the_command_filter_rejects_plain_text():
    # The filter is a plain object: evaluate it directly.
    event = make_message(text="hello")

    assert await Command("echo").evaluate(event) is False
```

Run it:

```bash
pytest -q
```

```text
...                                                              [100%]
3 passed
```

!!! note "Why `command_args` has to be passed in"
    `FakeEvent` is event-*shaped*, not a full `Events` envelope: it carries
    `text`, `chat_id`, `message_id`, `author_id`, plus whatever keyword
    arguments you give it. Real events compute `command_args`,
    `pattern_match` and the file helpers from the payload, so a fake that
    needs one of them should be handed the value explicitly. Anything you
    pass as a keyword becomes an attribute — that is also how you satisfy
    filters such as `IsGroup()`.

## 5. Assert on what the bot was asked to do

When a handler calls the bot instead of the event, inspect `FakeBot`:

```python
from darkob.testing import FakeBot

fake = FakeBot()
await fake.send_message("chat", "hi")

fake.called("send_message")      # True
fake.calls_to("send_message")    # [(("chat", "hi"), {})]
fake.last_call()[0]              # "send_message"
fake.reset()                     # forget every recorded call
```

A test that asserts on the outgoing call from the `menu` handler built in
[First bot](first-bot.md):

```python
from bot import menu
from darkob.testing import FakeBot, make_message


async def test_menu_sends_an_inline_keypad():
    fake = FakeBot()
    event = make_message(text="/menu")

    await menu(fake, event)

    method, args, kwargs = fake.last_call()
    assert method == "send_message"
    assert kwargs["inline_keypad"]["rows"][0]["buttons"][0]["id"] == "hi"
```

## 6. Test the module you already have

The test above rebuilds the handler, which is fine for a snippet but not
for a real bot. Import the handler from your own module instead — and keep
`bot.run()` behind a `__main__` guard so the import does not start polling:

```python title="bot.py"
import os

from darkob import Bot
from darkob.bot.filters import Command

bot = Bot(token=os.environ["RUBIKA_BOT_TOKEN"])

@bot.on_new_message(Command("echo"))
async def echo(bot, event):
    await event.reply(event.command_args or "nothing to echo")

if __name__ == "__main__":
    bot.run()
```

```python title="tests/test_bot.py"
from bot import echo
from darkob.testing import FakeBot, make_message


async def test_echo():
    event = make_message(text="/echo hi", command_args="hi")

    await echo(FakeBot(), event)

    assert event.replies == ["hi"]
```

Set the environment variable for the test run (a pattern-valid fake is
enough — nothing connects), then run the suite:

```bash
export RUBIKA_BOT_TOKEN="ABCDE000000000000000000000000000000000000000000000000000000000000"
# PowerShell: $env:RUBIKA_BOT_TOKEN = "ABCDE..."
pytest -q
```

!!! warning "A missing token blocks collection"
    `Bot(...)` falls back to an interactive prompt when the token does not
    match the expected shape, so importing `bot.py` with no token hangs CI
    instead of failing. Keep the token in the environment, and let the
    placeholder live only in tests you build yourself.

## See also

- [Testing bots](../guides/testing.md)
- [Handlers](../guides/handlers.md)
- [Filters](../guides/filters.md)
- [First bot](first-bot.md)
- [Errors](../guides/errors.md)


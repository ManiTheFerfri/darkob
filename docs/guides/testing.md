# Testing bots

darkob's own suite runs entirely offline — no sockets, no tokens. You can
do the same for your bot.

## Install the test extras

```bash
pip install pytest pytest-asyncio
```

```ini
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

## Test a handler without a bot

Handlers are plain functions. Call them with a stand-in event:

```python
from types import SimpleNamespace

async def _noop():
    pass

async def test_echo_replies(monkeypatch):
    replies = []

    fake_event = SimpleNamespace(
        text="hello",
        chat_id="g0test",
        reply=lambda text: replies.append(text) or _noop(),
    )

    await echo(bot=object(), event=fake_event)

    assert replies == ["hello"]
```

For `async def reply(...)` handlers, make the stub awaitable:

```python
from types import SimpleNamespace

class FakeEvent:
    def __init__(self, text, chat_id="g0test"):
        self.text = text
        self.chat_id = chat_id
        self.replies = []

    async def reply(self, text):
        self.replies.append(text)
```

## Test routers without a token

```python
from darkob import Router

def test_routes_are_registered():
    router = Router()

    @router.command("start")
    async def start(bot, event): ...

    assert len(router) == 1
    assert router.routes[0].kind == "on_command"
```

## Test conversations

`MemoryStorage` makes FSM tests trivial and isolated:

```python
from darkob import FSMContext, MemoryStorage, StateFilter

async def test_address_flow():
    storage = MemoryStorage()
    ctx = FSMContext(storage, key="chat")

    await ctx.set_state("address")
    assert await StateFilter(storage, "address").evaluate(
        SimpleNamespace(chat_id="chat")
    )

    await ctx.update_data(address="Main St")
    assert await ctx.get_data() == {"address": "Main St"}
```

## Assert that nothing hits the network

Guard the socket layer in a test:

```python
import socket

def test_import_is_offline(monkeypatch):
    def boom(*args, **kwargs):
        raise AssertionError("network access")

    monkeypatch.setattr(socket.socket, "connect", boom)

    import darkob  # already imported in practice; use a subprocess for a real check
```

darkob itself checks this in a subprocess, which is the only reliable way
to catch import-time I/O.

## Testing filters

Filters are async predicates over an event-shaped object:

```python
from types import SimpleNamespace
from darkob.bot.filters import Text, IsGroup

async def test_text_filter():
    event = SimpleNamespace(original_data={"message": {"text": "hi there"}})
    assert await Text("hi").evaluate(event) is True
```

## Golden rules

1. Never let a test hit a real API.
2. Freeze time and randomness when asserting on retries.
3. Test the failure path as often as the happy path — that is where
   darkob's own bugs were found.


## `darkob.testing`

Ship-ready fakes, so a handler test needs no token, no network and no
hand-written stubs:

```python
from darkob.testing import FakeBot, make_message

async def test_echo(bot=None):
    bot = FakeBot()
    event = make_message(text="hi")

    await echo(bot, event)

    assert event.replies == ["hi"]
```

`FakeBot` records every call and returns an `{"status": "OK"}` payload:

```python
await bot.send_message("chat", "hi")

bot.called("send_message")          # True
bot.calls_to("send_message")        # [(("chat", "hi"), {})]
bot.last_call()[0]                  # "send_message"
bot.reset()                         # forget everything
```

`FakeEvent` records what a handler does to it:

```python
event = make_message(text="hello", chat_id="g0abc")
await event.reply("thanks")

event.replies    # ["thanks"]
event.edits      # []
event.deleted    # False
```

Both accept extra keyword attributes, so you can shape the event to match
your filters:

```python
event = make_message(text="hi", is_group=True)
```

# Inline conversations

Two ways to ask a user something without writing a state machine.

## `ask()` — wait for the next reply

```python
from darkob import Bot, NoReply

bot = Bot(token="...")

@bot.on_command("signup")
async def signup(bot, event):
    await event.reply("What is your name?")

    try:
        reply = await bot.ask(event.chat_id, timeout=60)
    except NoReply:
        await event.reply("Never mind.")
        return

    await event.reply(f"Nice to meet you, {reply.text}")
```

While the prompt is pending, the next message in that chat is handed to
**you** instead of being dispatched to handlers, so no `waiting_for = True`
flag is needed.

### With a prompt and filters

```python
reply = await bot.ask(
    event.chat_id,
    "Send me a photo",
    filters=[lambda ev: ev.text and ev.text.startswith("/")],
    timeout=30,
)
```

The `text` argument is optional — pass it to send the question for you:

```python
reply = await bot.ask(event.chat_id, "Pick one", inline_keypad=Keyboard().row("A", "B"))
```

Both surfaces support it: `bot.ask(...)` and `client.ask(...)`.

| Behaviour | Detail |
| --- | --- |
| Timeout | Raises `darkob.NoReply` (a `TimeoutError` subclass) |
| Queueing | Two pending asks in one chat are served oldest-first |
| Filters | Each is called with the event; sync or async, exceptions count as "no match" |
| Cleanup | The waiter is removed on success, timeout or cancellation |

## `StatesGroup` — named states

Plain strings work, but a class keeps them together and typo-free:

```python
from darkob import FSMContext, JsonFileStorage, State, StateFilter, StatesGroup

storage = JsonFileStorage("fsm.json")

class Form(StatesGroup):
    name = State()
    email = State()

@bot.on_command("register")
async def register(bot, event):
    ctx = FSMContext(storage, key=event.chat_id)
    await ctx.set_state(Form.name)
    await event.reply("Name?")

@bot.on_new_message(StateFilter(storage, Form.name))
async def got_name(bot, event):
    ctx = FSMContext(storage, key=event.chat_id)
    await ctx.update_data(name=event.text)
    await ctx.set_state(Form.email)
    await event.reply("Email?")
```

`State` is a `str` subclass ordered by its group, so it flows through
every existing helper — storage backends, `StateFilter`, and comparisons —
with no changes:

```python
Form.name == "Form.name"      # True
Form.states()                 # {"name": State('Form.name'), ...}
list(Form.values())           # ["Form.name", "Form.other"]
```

Two groups cannot collide: `Form.name` and `Survey.name` are different
state strings.

## Which to use

| Need | Use |
| --- | --- |
| One question, then continue | `ask()` |
| Several steps, resumable after a restart | `StatesGroup` + `FSMContext` |
| Steps that must survive the process | FSM with `JsonFileStorage` or `SQLiteStorage` |

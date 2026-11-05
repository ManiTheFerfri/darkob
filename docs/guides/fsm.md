# Conversations (FSM)

A finite state machine tracks which step a user is on, and what they have
already told you.

## The idea

Two pieces of data per conversation:

- **state** — a string like `"waiting_for_address"`, or `None`
- **data** — a free-form dict

Both live in a `Storage`, keyed by chat (or user) id.

## Complete example

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

The second handler only runs while the conversation is in the `address`
state, so it will not hijack unrelated messages.

## Storage backends

| Storage | Survives restart | Use for |
| --- | --- | --- |
| `MemoryStorage()` | No | Tests, ephemeral bots |
| `JsonFileStorage("fsm.json")` | Yes | Single-process bots |
| `TTLMemoryStorage(ttl=3600)` | No | State that should expire |
| `SQLiteStorage("fsm.db")` | Yes | Durable and concurrency-safe |

`JsonFileStorage` writes atomically, tolerates a corrupt file (it starts
empty rather than crashing), and is safe to call from concurrent tasks.

`JsonFileStorage` writes atomically and tolerates a corrupt file.
`SQLiteStorage` runs in WAL mode, so it survives a hard kill mid-write
and is safe for several tasks writing at once.

```python
from darkob import SQLiteStorage, TTLMemoryStorage

storage = SQLiteStorage("darkob_fsm.db")   # durable
storage = TTLMemoryStorage(ttl=1800)         # forgets after 30 min
```

## FSMContext

```python
ctx = FSMContext(storage, key="g0abc")          # explicit key
ctx = FSMContext.from_event(storage, event)     # key from the event

await ctx.get_state()                # str | None
await ctx.set_state("waiting")
await ctx.set_state(None)            # clear the state

await ctx.get_data()                 # dict
await ctx.set_data({"a": 1})         # replace
await ctx.update_data(a=2, b=3)      # merge, returns the new dict
await ctx.clear()                    # state + data
```

## StateFilter

```python
StateFilter(storage, "address")
StateFilter(storage, "address", key_func=lambda e: e.author_id)
```

It is a normal filter, so it composes:

```python
from darkob.bot.filters import IsGroup

@bot.on_new_message(IsGroup() & StateFilter(storage, "address"))
async def group_address(bot, event):
    ...
```

## Choosing a key

`default_storage_key` prefers `chat_id`, then `object_guid`, then
`author_object_guid`, falling back to `"default"`.

Use a custom key to scope a conversation per user instead of per chat:

```python
ctx = FSMContext(storage, key=f"order:{event.author_id}")
```

## Custom storage

Implement `Storage` to back it with Redis or SQL:

```python
from darkob import Storage

class RedisStorage(Storage):
    async def get_state(self, key): ...
    async def set_state(self, key, state): ...
    async def get_data(self, key): ...
    async def set_data(self, key, data): ...
```

The four methods are all you need; `clear()` and `close()` have default
implementations.

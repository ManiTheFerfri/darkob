# Recipes

Task-shaped examples. Each one is a complete, runnable pattern you can
paste to an assistant as a starting point.

## Echo bot

```python
@bot.on_new_message()
async def echo(bot, event):
    if not event.text:
        return
    await event.reply(event.text)
```

## Command menu with a description

```python
bot.set_commands({
    "start": "Start the bot",
    "help": "Show help",
    "settings": "Change settings",
})
```

## Admin-only command

```python
from darkob.bot.filters import IsGroup

@bot.on_command("ban", IsGroup())
async def ban(bot, event):
    if not await bot.member_is_admin(event.chat_id, event.author_id):
        await event.reply("Admins only.")
        return
    ...
```

## Paginated list

Ask for the first page, then keep the cursor you were given:

```python
@bot.on_command("chats")
async def chats(bot, event):
    page = await bot.get_chats()          # first page
    names = [c.get("title", "?") for c in page]
    await event.reply("\n".join(names))
```

For large result sets, handle one page per command invocation and store
the cursor in FSM data rather than blocking the handler.

## Multi-step form

```python
from darkob import FSMContext, JsonFileStorage, StateFilter

storage = JsonFileStorage("fsm.json")

@bot.on_command("signup")
async def signup(bot, event):
    ctx = FSMContext(storage, key=event.chat_id)
    await ctx.set_state("name")
    await event.reply("Your name?")

@bot.on_new_message(StateFilter(storage, "name"))
async def got_name(bot, event):
    ctx = FSMContext(storage, key=event.chat_id)
    await ctx.update_data(name=event.text)
    await ctx.set_state("email")
    await event.reply("Your email?")

@bot.on_new_message(StateFilter(storage, "email"))
async def got_email(bot, event):
    ctx = FSMContext(storage, key=event.chat_id)
    data = await ctx.update_data(email=event.text)
    await ctx.clear()
    await event.reply(f"Thanks {data['name']}, saved {data['email']}.")
```

## Cancel any conversation

```python
@bot.on_command(["cancel", "cancel"], prefixes=["/", "!"] )
async def cancel(bot, event):
    await FSMContext(storage, key=event.chat_id).clear()
    await event.reply("Cancelled.")
```

Order matters: register the cancel handler **before** the state handlers if
you use `run_all_handlers=False`.

## Send a file from disk

```python
@bot.on_command("report")
async def report(bot, event):
    await bot.send_file(
        event.chat_id,
        file="report.pdf",
        file_type="File",
        text="Here is the report",
    )
```

`send_file` also accepts `bytes` and `base64`, and a `file_type` of
`File`, `Image`, `Voice`, `Video`, `Music` or `Gif`.

## Log every update

```python
@bot.middleware()
async def log_all(bot, event, call_next):
    print(getattr(event, "update_type", "?"), getattr(event, "chat_id", "-"))
    await call_next()
```

## Fail loudly, but survive

```python
import logging
from darkob.bot.exceptions import APIException

log = logging.getLogger(__name__)

@bot.on_command("send")
async def send(bot, event):
    try:
        await bot.send_message(event.chat_id, "done")
    except APIException as exc:
        log.warning("send failed: %s", exc)
        await event.reply("Could not send that right now.")
```

## Guard against self-replies

```python
@bot.on_new_message()
async def reply(bot, event):
    me = await bot.get_me()
    if event.author_id == me.get("user", {}).get("user_guid"):
        return
    await event.reply("got it")
```

## Keep state across restarts

```python
from darkob import JsonFileStorage

storage = JsonFileStorage("fsm.json")   # written atomically, one file
```

For multi-process deployments, implement `Storage` against Redis instead
of sharing the JSON file.

## Split into modules

```python
# main.py
from darkob import Bot
from routers import admin, users

bot = Bot(token="...")
bot.include_router(admin.router)
bot.include_router(users.router)
bot.run()
```

```python
# routers/admin.py
from darkob import Router

router = Router("admin")

@router.command("stats")
async def stats(bot, event):
    await event.reply("…")
```

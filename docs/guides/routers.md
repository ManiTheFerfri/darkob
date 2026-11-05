# Routers

A `Router` collects handlers without needing a bot instance, then
registers them all at once. Use it to split a bot into feature modules.

## Basic use

```python
from darkob import Bot, Router

bot = Bot(token="YOUR_BOT_TOKEN")
admin = Router("admin")

@admin.command("ban")
async def ban(bot, event):
    await bot.ban_member(event.chat_id, event.author_id)
    await event.reply("Banned.")

bot.include_router(admin)
bot.run()
```

## Why bother

- Handlers live next to the feature they implement, in their own file.
- A module can be tested without a token.
- Nested routers let one root assemble the whole bot.

## Nesting

```python
root = Router("root")
admin = Router("admin")
moderation = Router("moderation")

admin.include_router(moderation)
root.include_router(admin)

bot.include_router(root)     # registers everything, recursively
```

`len(router)` counts all routes including children.

## Router decorators

Mirror the bot decorators exactly:

`update()`, `message()`, `new_message()`, `edit_message()`,
`delete_message()`, `callback()`, `command()`, `event_data()`.

```python
@router.command("start")
@router.command(["help", "?", "راهنما"])
@router.message(IsGroup())
```

Constraints are passed through unchanged, so a router route behaves
identically to the same decorator written on the bot.

## Router middleware

A middleware declared on a router wraps **only** that router's
handlers, including routers nested inside it.

```python
@router.middleware()
async def log(bot, event, call_next):
    print("before")
    await call_next()
    print("after")
```

Call `await call_next()` to continue; return without calling it to
stop the handler. Multiple middlewares run outermost-first.

## Inspecting a router

```python
router.routes      # routes declared directly on this router
router.children    # nested routers
len(router)        # total routes, recursively
router.apply(bot)  # register manually; returns the number registered
```

## Registration rules

- `include_router` returns the router, so calls chain.
- Including the same child twice is a no-op.
- A router cannot include itself (`ValueError`).
- `bot.include_router(obj)` raises `TypeError` if `obj` is not a `Router`.
- Handlers register in declaration order; middleware, if any, is bot-level.

## Testing a router without a token

```python
router = Router()

@router.command("ping")
async def ping(bot, event):
    ...

assert len(router) == 1
assert router.routes[0].kind == "on_command"
```

# Bot vs Messenger vs Shad

Three clients in one package: a bot account on the Bot API, a real user account on Rubika, and that same user account on Shad.

## Which one do you need?

- **`Bot`** — people talk to *your bot*. You want commands, inline
  keyboards, a public webhook or long polling, and no phone number
  involved. This is the right default for automation.
- **`Messenger`** — *you* are the account: read and send in existing chats,
  manage groups and channels, react, search history, automate your own
  profile. It is a userbot, and it signs in as you.
- **`Shad`** — identical to `Messenger`, on the Shad platform instead of
  Rubika.

Nothing stops you from running a `Bot` and a `Messenger` in one process:
different classes, different credentials, independent state.

## The class hierarchy

```python
from darkob import Bot, Client, Messenger, Shad

Bot                     # standalone
Client                  # base class — deprecated, do not use
Messenger(Client)       # the supported user client
Shad(Messenger)         # same API, Shad platforms only
```

`Client` still works, but instantiating it prints a deprecation notice and
you should write `Messenger` instead. `Shad` accepts only
`shad_web`, `shad_pwa` and `shad_android`, and defaults to `shad_web`;
anything else raises `PlatformError`.

## Bot: the Bot API

```python
bot = Bot(token="ABCDE...")     # 64 chars: five uppercase letters, then 59
bot.run()                        # long polling, blocking
```

| Aspect | Detail |
| --- | --- |
| Transport | Plain HTTP to `https://botapi.rubika.ir/v3/<token>` |
| Endpoints | One base URL; no discovery, no circuit breaker |
| Updates | Long polling (`getUpdates`) or a webhook receiver |
| Auth | A bot token, or an encrypted `token_string` plus its password |
| Handlers | `bot.on_command`, `bot.on_new_message`, `bot.on_callback`, … |
| Concurrency | Polling awaits each update; webhook updates run under a semaphore |
| Stopping | `run_all_handlers=False` keeps only the first match |
| Downloads | `download_file(..., save_as=True, resume=True)` |
| Plugins | `bot.plugin_manager` exists for lifecycle management |

A token is visible to whoever reads the process environment; a leaked bot
token can send as your bot. Treat it as a password.

## Messenger: a real account

```python
from darkob import Messenger

async with Messenger(string_session="1BVts...") as client:
    me = await client.get_me()
```

| Aspect | Detail |
| --- | --- |
| Transport | Encrypted, signed HTTP to discovered data centres, plus a WebSocket |
| Endpoints | Discovered with `get_dcs`, ranked, rotated, one breaker each |
| Updates | Pushed over the WebSocket |
| Auth | Session file, `string_session`, or `auth` + `private_key` |
| Handlers | `client.on_new_message`, `client.on_chat_updates`, `client.on_add_reaction`, … |
| Concurrency | Handlers are spawned as tasks |
| Stopping | `stop_on_first_match=True` keeps only the first match |
| Throttling | `flood_sleep_threshold` bounds how long a rate-limit wait may last |

The method surface is the whole user account, not just messaging: `chats`,
`groups`, `channels`, `messages`, `users`, `settings`, `bots` and `extras`
(stickers, live comments, wallet, wallpapers). `messages/chats/users`
cover reading history, editing, reacting, polls, folders and privacy
settings.

## Auth models compared

| Credential | Used by | Notes |
| --- | --- | --- |
| Bot token | `Bot` | 64 characters; validated at construction |
| Encrypted `token_string` + `password` | `Bot` | Takes priority over `token` |
| Session file (`session="my.session"`) | `Messenger`, `Shad` | Restores `auth`, guid and key from disk on start |
| String session (`string_session=...`) | `Messenger`, `Shad` | Takes priority over the file; `password` if it was encrypted |
| `auth` + `private_key` | `Messenger`, `Shad` | API v6. `auth` must be 32 lowercase letters |

Two more rules are enforced at construction, before anything touches the
network:

- **API v6** needs `session`, `string_session`, *or* both `auth` and
  `private_key`. One without the other raises `AuthError`.
- **API v5** needs only `auth`, and rejects `private_key` with `AuthError`.
  It also ignores `session` and `string_session`.

## What is identical

The parts you write are the same on both surfaces: filters and their
`&`/`|`/`~` composition, `Keyboard`/`Button`, the formatting helpers, FSM
storage and `FSMContext`, routers, `darkob.testing`, metrics, health
checks, `RateLimiter`/`AdaptiveRateLimiter`, `SendQueue` and the `Retry`
policy. The differences are in transport, authentication and how handlers
are scheduled.

## The differences that bite

| Symptom | Bot | Messenger / Shad |
| --- | --- | --- |
| A send silently does nothing | `send_message` returned a response; check the log | `_send_request` returns `None` when every endpoint is circuit-open |
| `TooRequests` | Raised to your code | Retried with backoff, fed to the limiter |
| Handler ordering | Strictly sequential | Spawned tasks, may interleave |
| File attachments | `event.file_id` + `download_file` | `event.file_inline` + `download_file(file_inline=...)` |
| Resumable downloads | Yes | No — every call restarts |
| `bot.run()` vs `client.start()` | Blocking polling loop | Async connect; use `async with` |

## See also

- [Architecture](architecture.md)
- [Reliability](reliability.md)
- [Concurrency](concurrency.md)
- [API: Bot](../api/bot.md)
- [API: Messenger](../api/messenger.md)
- [API: Shad](../api/shad.md)
- [Migrating from maxrubika](../get-started/migrating-from-maxrubika.md)

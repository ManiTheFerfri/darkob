# Project layout

```
darkob/
├── __init__.py        Public exports, version, opt-in update check
├── TheBot.py          Bot class: composes the bot/ mixins
├── TheClient.py       Client / Messenger classes
├── shad.py            Shad facade
├── router.py          Composable routers
├── fsm.py             Conversation state and storage backends
├── hybrid.py          Sync/async bridge (one shared loop thread)
├── data.py            Response wrapper: attribute + item access
├── types/             Event and update models
├── bot/               Bot API surface
│   ├── session.py       Pooled HTTP session
│   ├── request.py       Request + retry + error mapping
│   ├── registry.py      Handler registry and dispatch
│   ├── bridge.py        Decorator families
│   ├── filters.py       42 event constraints
│   ├── plugin.py        Plugin manager
│   └── send_*.py        One module per endpoint family
└── client/            Messenger API surface
    ├── core/            api (transport, dispatch), cipher, session, media
    ├── base/            start, connect, request, upload, download
    ├── chats/           Chats, groups, channels, voice chats
    ├── messages/        Send, fetch, edit, react, polls
    ├── users/           Contacts, profiles, calls
    ├── settings/        Account settings, folders, two-step
    ├── decorators/      on_new_message, on_callback, …
    └── filters.py       Client-side filter classes
```

## Where to look for what

| You want… | Open |
| --- | --- |
| To add a bot endpoint | `bot/send_*.py` or `bot/get_*.py`, then register it |
| To change retry behaviour | `bot/request.py`, `client/core/api.py` |
| To change dispatch | `bot/registry.py`, `client/core/api.py` |
| To add a filter | `bot/filters.py` (Bot) or `client/filters.py` (Messenger) |
| To add a public export | `darkob/__init__.py` |
| To change packaging | `pyproject.toml` |

## Design rules

1. **One shared HTTP session per client.** Never create a session inside
   a request method.
2. **No network at import time.** Import must stay side-effect free.
3. **Typed errors over `None`.** If something failed, raise.
4. **Bounded concurrency.** No unbounded thread or task creation.
5. **Tests never touch the network.**

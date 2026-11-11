# Upstream v1.18.0 merge

darkob 0.19 merges the feature surface of maxrubika **v1.18.0** while keeping
darkob's transport, dispatch, compatibility and session-safety work.

This is an additive merge. No method that existed in `Bot`, `Messenger` or
`Shad` before it was removed, and every method exposed by the relocated
upstream commit is present. The merged `Messenger` and `Shad` also keep
darkob's `ask()` and `iter_messages()` helpers.

## New surfaces

Three clients can now be imported from `darkob`:

```python
from darkob import RubiAI, RubikaTV, Rubino

ai = RubiAI(auth="...")
posts = Rubino(auth="...")
tv = RubikaTV(auth="...")
```

All of these are optional to import: the root package loads them lazily, so a
bot that only uses `Bot` or `Messenger` does not import the additional
endpoint modules. These aliases also work for compatibility:

- `rubino`
- `RubiAi`, `rubiai`, `RubikaAI`, `RubikaAi`
- `rubikatv`

Each accepts a `Messenger` via `client=`, or creates one from
`session=`/`string_session=`. `auth=` is also supported for the upstream
API-only mode. Wrapper-created clients forward `timeout`, `proxy`,
`max_retries` and TLS settings. A connected client's HTTP pool is reused.

## New Messenger and Shad APIs

Examples of new upstream methods now available:

- `delete_message` and `forward_message`
- `save_message_draft`
- `send_live_location`
- `get_abs_chats`
- `delete_no_access_group_chat`
- `get_wallet_transfer_message` and `send_wallet_transfer_message`
- `on_scheduled_message`

The endpoint directory reorganisation upstream (grouped messages, chats and
settings) is included. See the generated [Rubino](api/rubino.md),
[RubiAI](api/rubiai.md), [RubikaTV](api/rubikatv.md), and
[Messenger](api/messenger.md) references for the actual current signatures.

## Compatibility rules

- The old Bot call style and the new upstream style both work:

  ```python
  await bot.request("POST", "getMe", json={})
  await bot.request(method="getMe", input={})
  await bot.request("getMe", {})
  ```

  All of them share darkob's retries, rate-limiter feedback, metrics and
  plugin hooks. `Bot(as_dict=True)` returns plain dictionaries.

- `Bot.download_file` still returns raw bytes, or base64 when requested.
  Its resumable `Range` behaviour and documented return types did not change
  to match upstream's new `Data` wrapper.

- `Messenger.send_message` accepts its earlier file, base64 and sticker
  parameters. Those calls are routed to `send_file` or the raw sticker path;
  their arguments are not accepted then silently discarded.

- `get_chat_messages` accepts its historic `(chat, max_id, ...)` form, as well
  as the newer direction-first call shape and keyword parameters.

- Live helpers accept either positional order `(access_token, live_id)` or
  `(live_id, access_token)` only when the argument shapes make that
  unambiguous. **Use keywords** for arbitrary strings; tokens beginning with
  nothing recognizable are deliberately left in the legacy order.

- Voice-chat arguments such as `voice_chat_id` are optional for existing
  calls. When absent, the library resolves the current chat's active voice
  chat, or raises `VoiceChatNotActive` rather than inventing one.

## Sessions are not reset by the merge

Existing darkob sessions remain `.max` files at their stable paths. The
primary database key and the current `StringSession` secret are unchanged.
Migration is read-compatible:

- older maxrubika database encryption keys are accepted while reading;
- upstream `StringSession` secrets are accepted when no explicit password is
  supplied;
- supplied passwords are never bypassed by fallback secrets;
- source session files are **not deleted** after migration;
- unreadable files are still quarantined rather than destroyed.

Use your usual `session=` or `string_session=` value. There is no mandatory
re-login step.

## Transport and async changes retained or added

- Rubino uses one retry budget for a whole request instead of allowing
  `max_retries` attempts for every one of 85 candidate URLs.
- The new surfaces reuse connected sessions when available and verify TLS by
  default. `verify_ssl=False` is still available explicitly; it is not forced.
- `proxy` and `timeout` are forwarded by Rubino, RubiAI and RubikaTV.
- Media thumbnail and audio parsing is moved off the event loop in the new
  send paths, and rubino disk reads/writes use `aiofiles`.
- Timestamp defaults such as `round(time()) - 150` are evaluated per request,
  not frozen when Python imports the module.

## Verification

The merge includes coverage for both historical call shapes and the new
surfaces: import and API retention checks, session key compatibility,
`Data` indexing with nested `Data` objects, mock HTTP transport and TLS
settings, bounded retries, raw sticker payloads, voice/live compatibility and
update-timestamp behaviour. No live endpoint was needed for these tests; the
new APIs' presence and signatures are additionally checked against the
relocated upstream source.

See also:

- [Migrating from maxrubika](get-started/migrating-from-maxrubika.md)
- [Bot vs Messenger vs Shad](explanation/bot-vs-messenger-vs-shad.md)
- [Reliability](explanation/reliability.md)

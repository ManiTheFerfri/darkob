# Filters

Filters decide whether a handler runs. Import them from
`darkob.bot.filters`.

```python
from darkob.bot.filters import IsGroup, Text, IsImage
```

## Composing

Filters combine with Python operators: `&` (both), `|` (either), `~` (not).

```python
@bot.on_new_message(IsGroup() & ~IsImage())
async def text_in_group(bot, event):
    ...
```

Precedence follows Python: `~` binds tighter than `&`, which binds
tighter than `|`.

## Message shape

| Filter | Matches |
| --- | --- |
| `IsMessage()` | A new message |
| `IsEdited()` | An edit |
| `IsDeleted()` | A deletion |
| `IsCallback()` | An inline keyboard callback |
| `IsStartedBot()` / `IsStoppedBot()` | Bot lifecycle updates |
| `IsEventData()` | System event payloads |

## Text

| Filter | Matches |
| --- | --- |
| `Text("hello")` | Text containing the pattern (regex) |
| `TextMatch(r"name: (\w+)")` | Same, and stores the match on `event.pattern_match` |
| `Command("start")` | A command, optionally with a bot suffix |
| `IsText()` | Any text message |

```python
@bot.on_new_message(TextMatch(r"order\s+(\d+)"))
async def order(bot, event):
    number = event.pattern_match.group(1)
    await event.reply(f"Order #{number}")
```

## Chat kind

| Filter | Matches |
| --- | --- |
| `IsUser()` | A direct chat |
| `IsGroup()` | A group |
| `IsChannel()` | A channel |
| `ChatType("Group")` | By explicit type name |
| `FromChat("g0…")` | A specific chat |
| `FromUser("u0…")` | A specific user |

## Media

`IsFile()`, `IsImage()`, `IsVideo()`, `IsVoice()`, `IsMusic()`,
`IsSticker()`, `IsPoll()`, `IsLocation()`, `IsReply()`,
`IsForwarded()`.

Forward details: `ForwardedFromUser()`, `ForwardedFromChannel()`,
`ForwardedFromBot()`, `ForwardedNoLink()`.

## Formatting metadata

| Filter | Matches |
| --- | --- |
| `HasMetadata()` | Text carrying bold/italic/link formatting |
| `MetadataType("Bold")` | A specific metadata type |

## Membership and rights

| Filter | Matches |
| --- | --- |
| `IsJoined()` | The bot/user is a member |
| `IsAdmin()` | Admin rights |
| `IsOwner()` | Ownership |

## Events

```python
from darkob.bot.filters import EventType

@bot.on_event_data(EventType("AddedGroupMembers"))
async def someone_joined(bot, event):
    await event.reply("Welcome to the group!")
```

## Writing your own

Subclass `EventConstraint` and implement `evaluate`:

```python
from darkob.bot.filters import EventConstraint

class IsLongMessage(EventConstraint):
    def __init__(self, minimum: int = 500):
        self.minimum = minimum

    async def evaluate(self, event) -> bool:
        return len(getattr(event, "text", "") or "") >= self.minimum
```

`evaluate` may be async and may do I/O. A filter that raises is treated
as "no match" and the error is logged.

# Models and enums

Every type the Bot API documents, as Python `str` enums. They compare
equal to their wire value and serialise to it, so they are safe to pass
anywhere the API expects a string.

```python
from darkob import ButtonType, ChatType, FileType
from darkob.bot.models import (
    ButtonCalendarType, ButtonLocationType, ButtonSelectionType,
    ButtonTextboxLine, ChatKeypadType, EventJoinType, EventType,
    ForwardedFrom, MessageSender, PaymentStatus, PollStatus,
)
```

## Buttons

`ButtonType` — the 19 button kinds, each with a builder in
[Keyboards](../guides/keyboards.md):

`Simple` · `Selection` · `Calendar` · `NumberPicker` · `StringPicker` ·
`Location` · `Payment` · `CameraImage` · `CameraVideo` · `GalleryImage` ·
`GalleryVideo` · `File` · `Audio` · `RecordAudio` · `Textbox` · `Link` ·
`AskMyPhoneNumber` · `AskMyLocation` · `Barcode`

```python
from darkob import ButtonType

ButtonType.Selection == "Selection"   # True
```

| Enum | Values |
| --- | --- |
| `ButtonSelectionType` | `TextOnly`, `TextImgThu`, `TextImgBig` |
| `ButtonSelectionGet` | `Local`, `Api` |
| `ButtonSelectionSearch` | `None_`, `Local`, `Api` |
| `ButtonCalendarType` | `DatePersian`, `DateGregorian` |
| `ButtonLocationType` | `Picker`, `View` |
| `ButtonTextboxKeypad` | `String`, `Number` |
| `ButtonTextboxLine` | `SingleLine`, `MultiLine` |

## Chats and files

| Enum | Values |
| --- | --- |
| `ChatType` | `User`, `Bot`, `Group`, `Channel` |
| `ChatKeypadType` | `None_`, `New`, `Remove` |
| `FileType` | `File`, `Image`, `Voice`, `Video`, `Music`, `Gif` |
| `MessageSender` | `User`, `Bot` |
| `ForwardedFrom` | `User`, `Channel`, `Bot` |

## Polls, payments and events

| Enum | Values |
| --- | --- |
| `PollStatus` | `Open`, `Closed` |
| `PaymentStatus` | `Paid`, `NotPaid` |
| `EventType` | `BotJoined`, `BotRemoved`, `BotPermissionsChanged` |
| `EventJoinType` | `Member`, `Admin` |

## Why `None_`

`None` is a reserved word in Python, so the enum member is `None_` while
the value sent over the wire is still `"None"`:

```python
ChatKeypadType.None_ == "None"   # True
```

## Limits worth knowing

The reference documents these enums but not every field that carries them
— the calendar's Persian/Gregorian selector, the textbox variants and the
location mode have no documented field name. darkob does **not** invent
them; pass the field yourself through the builder's `**fields`.

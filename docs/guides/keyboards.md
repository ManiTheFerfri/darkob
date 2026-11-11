# Keyboards and formatting

Two helpers remove most of the boilerplate from bot code: keypad
builders, and text formatting.

## Keypads

A :class:`Keyboard` **is** a dict (`{"rows": [...]}`), so it can be passed
anywhere the API accepts a raw keypad. Ids and button types are filled in
automatically.

```python
from darkob import Keyboard

keypad = Keyboard().row("Yes", "No").row("Cancel")

await bot.send_message(chat_id, "Continue?", inline_keypad=keypad)
```

Chat keyboards (the persistent bottom keyboard) use the same builder:

```python
await bot.send_message(chat_id, "Menu", chat_keypad=Keyboard().row("Help", "Settings"))
```

### Chaining

```python
(
    Keyboard()                # empty
    .row("A", "B")            # one row, two buttons
    .row("C")                 # second row
    .button("Alone")          # a row with a single button
    .clear()                  # remove all rows
)
```

Inspect before sending:

```python
keyboard.row_count        # number of rows
keyboard.button_count     # total buttons
keyboard.to_dict()        # plain-dict copy
Keyboard.from_rows([["A", "B"], ["C"]])
```

### Explicit buttons

```python
from darkob import Button

Button("Delete", id=42, type="Selection")

Keyboard().row(
    Button("Delete", id=42, type="Selection"),
    "Plain string button",
    {"button_text": "Raw dict", "type": "Simple"},
)
```

`Button` accepts `text`, `id`, `type` and any extra keyword fields, which
are forwarded to the API verbatim:

```python
Button("Open", url="https://example.com")
```

An empty button label raises `ValueError` immediately instead of failing
server-side.

### With the Messenger surface

The userbot `send_message` takes `inline_keypad` and `chat_keypad` too,
and accepts the same `Keyboard`.

## Text formatting

Rubika renders a small Markdown dialect. These helpers produce it exactly:

| Helper | Output |
| --- | --- |
| `bold("x")` | `**x**` |
| `italic("x")` | `__x__` |
| `strike("x")` | `~~x~~` |
| `underline("x")` | `--x--` |
| `spoiler("x")` | `\|\|x\|\|` |
| `code("x")` | `` `x` `` |
| `pre("x", "python")` | fenced block |
| `link("text", url)` | `[text](url)` |
| `join([...])` | skips empty fragments |

```python
from darkob import bold, code, link

await event.reply(
    f"{bold('Deployed')} {code('v0.2.1')} — {link('logs', 'https://example.com')}"
)
```

They return plain strings, so they compose inside f-strings and nest:

```python
bold(f"{italic('nested')} works")
```

`link()` raises `ValueError` on an empty URL rather than sending a
malformed message.

## Button types

The Bot API documents 19 button types. Every one has a builder, and the
fields each builder sends are the ones the reference lists — nothing is
invented.

```python
from darkob import Button, Keyboard

keypad = (
    Keyboard()
    .row(Button.simple("Plain"), Button.link("Docs", "https://rubika.ir"))
    .row(Button.selection("Pick", title="Choose", items=[{"text": "A"}]))
    .row(Button.calendar("Date", min_year=2024, max_year=2030))
)
```

| Builder | `type` sent | Notes |
| --- | --- | --- |
| `Button.simple(text)` | `Simple` | |
| `Button.link(text, url)` | `Link` | |
| `Button.selection(text, title=, items=, columns_count=, is_multi_selection=)` | `Selection` | |
| `Button.calendar(text, title=, min_year=, max_year=)` | `Calendar` | Persian/Gregorian field is not named in the reference |
| `Button.number_picker(text, title=, min_value=, max_value=)` | `NumberPicker` | |
| `Button.string_picker(text, title=, items=)` | `StringPicker` | |
| `Button.location(text, image_url=)` | `Location` | |
| `Button.text_box(text)` | `Textbox` | |
| `Button.ask_my_phone(text)` / `Button.ask_my_location(text)` | `AskMyPhoneNumber` / `AskMyLocation` | |
| `Button.barcode(text)` | `Barcode` | |
| `Button.payment(text, **fields)` | `Payment` | **Requires** extra fields; a bare one is rejected by the API |
| `Button.of("CameraImage", text)` | any | Escape hatch for the remaining types |

All 19 documented types have builders. `Button.payment` raises `ValueError`
locally when required fields are missing, so that malformed request fails
before any network call. Server acceptance still requires a live check.

## Enums

The documented enums live in `darkob.bot.models`, and the common ones are
also exported from the package root:

```python
from darkob import ButtonType, ChatType, FileType
from darkob.bot.models import ChatKeypadType, PollStatus, EventType

FileType.Voice          # "Voice"
ButtonType.Selection    # "Selection"
```

They subclass `str`, so they serialise to the exact wire value and compare
equal to plain strings.

## Putting them together

```python
from darkob import Bot, Keyboard, bold

bot = Bot(token="...")

@bot.on_command("order")
async def order(bot, event):
    keypad = Keyboard().row("Confirm", "Cancel")
    await bot.send_message(
        event.chat_id,
        f"{bold('Order #42')}\nShall I confirm?",
        inline_keypad=keypad,
    )
```

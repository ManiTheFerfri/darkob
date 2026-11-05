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
Keyboard()                    # empty
    .row("A", "B")            # one row, two buttons
    .row("C")                 # second row
    .button("Alone")          # a row with a single button
    .clear()                  # remove all rows
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

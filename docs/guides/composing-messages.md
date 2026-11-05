# Composing messages

Two helpers keep message code short: a builder for the message itself, and
formatting helpers for the text.

## MessageBuilder

Handlers often assemble the same pieces — text, a keypad, a reply target,
a silent flag. The builder keeps them in one place and emits only the
options you actually set.

```python
from darkob import Keyboard, MessageBuilder

message = (
    MessageBuilder("Order #42 confirmed")
    .append("Delivery tomorrow between 9 and 12")
    .inline(Keyboard().row("Track", "Cancel"))
    .silent()
)

await message.send(bot, event.chat_id)
```

### Building text

```python
builder = MessageBuilder("Line one")
builder.append("Line two")        # newline separated
builder.line()                    # blank line
builder.line("After the gap")
builder.set_text("Start over")    # replace everything

builder.text                      # the string so far
len(builder)                      # character count
```

`append` takes any separator:

```python
MessageBuilder("a").append("b", separator=" ·  ").text   # "a · b"
```

### Options

| Method | Sets |
| --- | --- |
| `.keypad(kb)` | `chat_keypad` — the persistent bottom keyboard |
| `.inline(kb)` | `inline_keypad` — buttons attached to the message |
| `.reply_to(message_id)` | `reply_to_message_id` |
| `.silent()` | `disable_notification` |
| `.metadata(meta)` | Rubika text metadata |
| `.option(name, value)` | Any other `send_message` keyword |
| `.clear_options()` | Drops every option, keeps the text |

### Sending or inspecting

```python
message.build()          # {"text": ..., **options}
await message.send(bot, chat_id)
```

`build()` is plain data, so it is easy to assert on in tests:

```python
assert MessageBuilder("hi").silent().build() == {
    "text": "hi",
    "disable_notification": True,
}
```

## Formatting

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

await event.reply(f"{bold('Done')} in {code('1.2s')} — {link('logs', url)}")
```

## Both together

```python
from darkob import Keyboard, MessageBuilder, bold

message = (
    MessageBuilder(bold("Deployment finished"))
    .append("All checks passed")
    .inline(Keyboard().row("View logs", "Roll back"))
    .reply_to(event.message_id)
)

await message.send(bot, event.chat_id)
```

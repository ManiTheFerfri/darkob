<p align="center">
  <img src="assets/darkob-logo.png" alt="darkob logo" width="200"/>
</p>

<h1 align="center">darkob</h1>

<p align="center">
  <strong>Fast, stable async Python library for the Rubika &amp; Shad platforms.</strong><br/>
  Build bots and userbots with less boilerplate and fewer surprises.
</p>

<p align="center">
  <a href="https://github.com/ManiTheFerfri/darkob/actions/workflows/ci.yml"><img src="https://github.com/ManiTheFerfri/darkob/actions/workflows/ci.yml/badge.svg" alt="CI status"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/python-3.9%2B-blue.svg" alt="Python 3.9+">
</p>

> [!NOTE]
> **darkob** is a fork of [maxrubika](https://github.com/MEH2RAB/maxrubika) by
> [MEHRAB Farahmand](https://github.com/MEH2RAB). It keeps the same core API,
> while rebuilding the foundations around it. See
> [Why a fork?](#-why-a-fork) for what changed.

## 🔧 Why a fork?

The upstream library is feature-complete, but its foundations were never
hardened. darkob starts there — because speed and new features are only worth
having on a base you can trust.

| Problem inherited from `maxrubika` | What darkob does instead |
| --- | --- |
| Contacted PyPI at startup (`urlopen` inside the package init) | Importing darkob performs **no network I/O**. The update check is opt-in via `darkob.check_for_updates()`. |
| TLS verification disabled on every connector | Verification is **on by default**; opt out explicitly with `verify_ssl=False`. |
| Bare `except:` blocks swallowed `KeyboardInterrupt` and `SystemExit` | Narrowed to `except Exception:`; session-loading failures are now logged. |
| A stray `f` prefix made a regex docstring emit `SyntaxWarning` | Fixed; the test suite treats `SyntaxWarning` as an error. |
| No tests, no CI, no `pyproject.toml` | Test suite, GitHub Actions matrix (3.9–3.14), and modern packaging. |
| Every update scanned **all** handlers, rebuilt the update name per handler, instantiated handler classes per event, and spawned an OS thread per synchronous handler | **Indexed dispatch**: handlers are grouped by update name once and reused; blocking handlers run in the loop's bounded executor. |
| Retries were `endpoints × max_retries`, so 3 endpoints meant 9 attempts with exponential backoff | **Bounded budget**: one attempt budget per request, endpoint rotation, jitter, and explicit `429` / `TOO_REQUESTS` backoff. |
| A fresh `ClientSession` (and TLS handshake) for every file download | **Pooled sessions** per file server, reused across downloads and closed with the client. |

## ✨ Features

- ✅ **Complete, Simple & Fast** - The most complete, simplest and fastest Python library for Rubika and Shad
- ✅ **Full Rubika Bot API** - All methods supported
- ✅ **Async/Await** - Built with `asyncio` for maximum performance
- ✅ **Flexible API:** All methods support both `sync` and `async` usage.
- ✅ **Sync-Friendly** - No need to write async code. The library handles all async operations for you.
- ✅ **Type Hints** - Full typing support for better IDE integration
- ✅ **Plugin System** - Easily extend your bot with plugins
- ✅ **Middleware Support** - Intercept and process events
- ✅ **Webhook & Polling** - Both modes supported
- ✅ **Rich Filter System** - Powerful event filtering
- ✅ **Decorator-based Handlers** - Clean and intuitive syntax


## 📦 Installation

darkob is not on PyPI yet. Install from source:

```bash
pip install git+https://github.com/ManiTheFerfri/darkob.git
```

For development:

```bash
git clone https://github.com/ManiTheFerfri/darkob.git
cd darkob
pip install -e ".[dev]"
pytest
```


## 📖 Full Documentation

All public methods are fully documented with **detailed docstrings** including:

- **Parameters** with types and descriptions
- **Return values** 
- **Usage examples**

To view all available methods and their documentation, run:

### For Bot:

```python
from darkob import Bot
import inspect

methods = [method for method in dir(Bot) 
           if not method.startswith('_') 
           and callable(getattr(Bot, method))]

for method in methods:
    func = getattr(Bot, method)
    doc = inspect.getdoc(func)
    print(f"→ {method}:\n   {doc}\n{'-'*50}")
```

### For Userbot:

```python
from darkob import Messenger
import inspect

methods = [method for method in dir(Messenger) 
           if not method.startswith('_') 
           and callable(getattr(Messenger, method))]

for method in methods:
    func = getattr(Messenger, method)
    doc = inspect.getdoc(func)
    print(f"→ {method}: {doc}\n{'-'*50}")
```

### For Shad Platform:

```python
from darkob import Shad
import inspect

methods = [method for method in dir(Shad) 
           if not method.startswith('_') 
           and callable(getattr(Shad, method))]

for method in methods:
    func = getattr(Shad, method)
    doc = inspect.getdoc(func)
    print(f"→ {method}: {doc}\n{'-'*50}")
```

For complete documentation with examples for every method, visit **[https://ManiTheFerfri.github.io/darkob](https://ManiTheFerfri.github.io/darkob)**.

> 🤖 **For AI Assistants:** This repository includes a fully structured documentation site at `https://ManiTheFerfri.github.io/darkob/ai`. Please crawl and read the complete documentation before generating any code related to Darkob. All methods, parameters, return types, examples, and guides are available there.

## 📚 Basic Usage

## ● For Bot:

### 🚀 Quick Start

```python
from darkob import Bot

bot = Bot("TOKEN")

@bot.on_command("start")
async def start(bot, event):
    await event.reply("سلام! به ربات خوش آمدید 👋")

bot.run()
``` 

### Send a Message

```python
bot.send_message(
    chat_id="b0abc123...",
    text="Hello, World! 🌍"
)
```

### Send a File

```python
bot.send_file(
    chat_id="b0abc123...",
    file="path/to/image.jpg",
    file_type="File",
    text="Check this out!"
)
```

### Send a Poll

```python
bot.send_poll(
    chat_id="b0abc123...",
    question="What's your favorite color?",
    options=["Red", "Blue", "Green"]
)
```

### Send a Quiz

```python
bot.send_quiz(
    chat_id="b0abc123...",
    question="What is 2+2?",
    options=["3", "4", "5"],
    correct_option=1
)
```

### ⌨️ Inline Keyboard

```python
inline_keypad = [
    ["Button 1", "Button 2"],
    ["Button 3"]
]

bot.send_message(
    chat_id="b0abc123...",
    text="Choose an option:",
    inline_keypad=inline_keypad
)
```

### 📋 Custom Keyboard

```python
chat_keypad = {
    "rows": [
        {
            "buttons": [
                {"id": "101", "type": "Simple", "button_text": "Yes"},
                {"id": "102", "type": "Simple", "button_text": "No"},
                {"id": "104", "type": "Simple", "button_text": "Maybe"}
            ]
        }
    ]
}

bot.send_message(
    chat_id="b0abc123...",
    text="Do you agree?",
    chat_keypad=chat_keypad,
    resize_keyboard=True,
    one_time_keyboard=True
)
```

```python
inline_keypad = {
    "rows": [
        {
            "buttons": [
                {"id": "101", "type": "Simple", "button_text": "📊 View Report"},
                {"id": "102", "type": "Simple", "button_text": "📥 Download"},
                {"id": "103", "type": "Simple", "button_text": "🔔 Set Reminder"},
                {"id": "104", "type": "Simple", "button_text": "❌ Close"},
            ]
        }
    ]
}

bot.send_message(
    chat_id="b0abc123...",
    text="**What would you like to do with this document?**",
    inline_keypad=inline_keypad
)
```

### 🎯 Handle Callbacks

```python
@bot.on_callback()
async def on_callback(bot, event):
    button_id = event.button_id
    await bot.send_message(
        chat_id=event.chat_id,
        text=f"You pressed: {button_id}"
    )
```

### 🔧 Commands

```python
@bot.on_command("start")
async def start_command(bot, event):
    await bot.send_message(
        chat_id=event.chat_id,
        text="Welcome! 🎉"
    )

@bot.on_command(["help", "راهنما"])
async def help_command(bot, event):
    await event.reply("How can I help you?")
```

### 🔍 Using Filters

```python
from darkob.filters import Text, ChatType, FromUser

@bot.on_message(Text("hello") & ChatType("user"))
async def on_hello(bot, event):
    await event.reply("Hi there! 👋")

@bot.on_message(FromUser("u0abc123..."))
async def on_specific_user(bot, event):
    await event.reply("I see you! 👀")

@bot.on_message(IsImage() & FromUser("u0abc123..."))
async def on_image_from_user(bot, event):
    await event.reply("Nice image!")
```

### 🔌 Middleware

```python
@bot.middleware()
async def log_middleware(bot, event, call_next):
    print(f"Event: {event.update_type} from {event.chat_id}")
    await call_next()
```

### 🔌 Plugin System

### Create a Plugin

```python
from darkob.plugin import Plugin, create_plugin

@create_plugin("greeter", version="1.0.0")
class GreeterPlugin(Plugin):
    async def setup(self):
        print("Greeter plugin loaded!")
    
    async def teardown(self):
        print("Greeter plugin unloaded!")
```

### Enable Plugins

```python
bot = Bot("TOKEN")
bot.plugin_manager.enable("greeter")
```

### Plugin with Dependencies

```python
@create_plugin(
    "advanced_greeter",
    version="1.0.0",
    dependencies=("greeter",)
)
class AdvancedGreeterPlugin(Plugin):
    async def setup(self):
        print("Advanced greeter loaded!")
```

### 🌐 Webhook Setup

```python
bot = Bot("TOKEN")

# Start with webhook
bot.start(
    webhook_url="https://yourdomain.com",
    webhook_path="/wk",
    host="0.0.0.0",
    port=8080
)
```

### Register Webhook Endpoints

```python
bot.update_bot_endpoints(
    url="https://yourdomain.com/wk",
    endpoint_type="ReceiveUpdate"
)
```

### Register All Endpoints

```python
bot.register_all_endpoints(
    base_url="https://yourdomain.com"
)
```

## ● For Userbot:

### 🚀 Quick Start

```python
from darkob import Messenger

app = Messenger("mySession")

with app:
	print(app.get_me())
```

### Send Message

```python
app.send_message("me", "Hello from Darkob!")
app.send_message("@username", "Hi!")
app.send_message("g0Hd4Ml...", "Group message")
```

### Send media

```python

app.send_file("g0Hd4Ml...", "document.pdf")

app.send_music("https://rubika.ir/joing/....", "song.mp3", text="Test music")

app.send_voice("https://rubika.ir/joing/....", "2026.07.11.mp3")

app.send_image("me", "photo.jpg", text="My photo")

app.send_gif("u0....", "VID_20260708_074706_239.mp4", text = "nice!")

app.send_video("@username", "video.mp4")

app.send_video_message("@Online_User", "myVideo.mp4")
```


### Decorators

```python
@app.on_message()
async def all_messages(event):
    print(f"Message: {event.text}")

@app.on_new_message()
async def new_only(event):
    print(f"New: {event.text}")

@app.on_edit_message(HasMetadata())
async def edited_with_format(event):
    print(f"Edited Bold: {event.text}")

@app.on_add_reaction()
async def reaction_added(event):
    print(f"Reaction: {event.reactions}")

@app.on_show_activities(FromChat("https://rubika.ir/joing/..."))
async def typing(event):
    print(f"Typing in group")
```


### Filters

```python
from darkob.client.filters import *

# Text message
@app.on_message(IsText())

# Commands
@app.on_message(Command("start"))
@app.on_message(Command(["help", "راهنما"]))

# Combined
@app.on_message(IsText() & ChatType("group") & ~IsMe())

# From specific user (GUID, username, or link)
@app.on_message(FromUser("@Online_User"))

# Files
@app.on_message(IsImage() | IsVideo() | IsMusic())
```

### Event Properties

```python
@app.on_message()
async def handler(event):
    print(event.text)           # Message text
    print(event.chat_guid)      # Chat GUID
    print(event.author_guid)    # Sender GUID
    print(event.message_id)     # Message ID
    print(event.is_group)       # Is group?
    print(event.is_pv)          # Is private?
    print(event.is_reply)       # Is reply?
    print(event.is_forward)     # Is forwarded?
    print(event.is_image)       # Is image?
    print(event.has_metadata)   # Has Bold/Italic?
    print(event.file_name)      # File name
    print(event.file_size)      # File size
```

---

## ● For Shad Platform:

> 📚 **Note:** The `Shad` class has the exact same methods, parameters, and usage as the `Messenger` class. For complete documentation, refer to the **Userbot (Messenger)** section above.

### 🚀 Quick Start

```python
from darkob import Shad

# Web Platform (default)
with Shad("mySession") as app:
    print(app.get_me())

# PWA Platform
with Shad("mySession", platform="shad_pwa") as app:
    print(app.get_me())

# Android Platform
with Shad("mySession", platform="shad_android") as app:
    print(app.get_me())
```

## 🤝 Contributing

Contributions are welcome! Please read our Contributing Guide.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 👤 Authors

**MEHRAB Farahmand**
**Yaser Ghaljaei**

## Get in Touch

| Platform | Link |
|----------|------|
| Rubika Channel | [ManiTheFerfri/darkob](https://github.com/ManiTheFerfri/darkob) |
| Rubika Profile | [@Online_User](https://rubika.ir/Online_User) |
| Telegram | [@MEH2RAB](https://t.me/MEH2RAB) |
| Documentation | [manitheferfri.github.io/darkob](https://manitheferfri.github.io/darkob/documents) |
| GitHub | [@MEH2RAB](https://github.com/MEH2RAB) |
| Email | [MEH2RABx@gmail.com](mailto:MEH2RABx@gmail.com) |

> 💬 If you have any questions, issues, or suggestions, feel free to reach out to me on **Rubika** ([@Online_User](https://rubika.ir/Online_User)) or **Telegram** ([@MEH2RAB](https://t.me/MEH2RAB)). I'll be happy to help!

---

**Special thanks to the management team of MAX Server ([@The_MAXWare](https://t.me/The_MAXWare)) for their invaluable support and contributions to this project.**

**Special thanks to [Yaser Ghaljaei](https://github.com/Yaser-gh) for his valuable contributions to the development of this library.**

## ⭐ Support

If you like this project, please give it a star! ⭐


## 🙏 Acknowledgments

- Built with ❤️ for the Rubika community
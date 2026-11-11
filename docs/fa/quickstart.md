<div dir="rtl" lang="fa" markdown="1">

# راهنمای شروع سریع

**darkob** کتابخانه‌ای سریع و پایدار برای ساخت ربات و یوزربات در
پیام‌رسان‌های **روبیکا** و **شاد** است.

## نصب

```bash
pip install darkob
```

## اولین ربات

```python
from darkob import Bot

bot = Bot(token="توکن_ربات_شما")

@bot.on_command("start")
async def start(bot, event):
    await event.reply("خوش آمدید 👋")

@bot.on_new_message()
async def echo(bot, event):
    if not event.text:
        return
    await event.reply(event.text)

bot.run()
```

تابع `bot.run()` ربات را با روش Polling اجرا می‌کند و تا زمان توقف
(Ctrl+C) فعال می‌ماند.

## دسترسی به اطلاعات رویداد

| ویژگی | معنی |
| --- | --- |
| `event.chat_id` | شناسه‌ی گفتگو |
| `event.author_id` | فرستنده‌ی پیام |
| `event.text` | متن پیام |
| `event.reply(text)` | پاسخ در همان گفتگو |

## اجرا با وبهوک

```python
bot.run(webhook_url="https://example.com/wk", port=8080)
```

## مراحل بعدی

- [مدیریت‌کننده‌ها (Handlers)](../guides/handlers.md)
- [فیلترها (Filters)](../guides/filters.md)
- [روترها (Routers)](../guides/routers.md)
- [مکالمه‌های چندمرحله‌ای (FSM)](../guides/fsm.md)
- [خطاها (Errors)](../guides/errors.md)

</div>

---

!!! tip "Documentation is in English"
    The full documentation is written in English because it doubles as
    the context for AI assistants. Every page is also available as raw
    Markdown — good for pasting into a model.

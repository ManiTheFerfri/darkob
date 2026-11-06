"""Tests for Bot shortcuts and the global error handler."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from darkob import Bot

from conftest import VALID_TOKEN


def make_bot(**kwargs) -> Bot:
    return Bot(token=VALID_TOKEN, show_welcome=False, **kwargs)


EVENT = SimpleNamespace(chat_id="g0chat", message_id="42", text="hi")


# ---------------------------------------------------------------------------
# reply / edit / delete
# ---------------------------------------------------------------------------


async def test_reply_targets_the_event_chat_and_message():
    bot = make_bot()
    calls = []

    async def fake_send(chat_id, text, **kwargs):
        calls.append((chat_id, text, kwargs))
        return "sent"

    bot.send_message = fake_send

    result = await bot.reply(EVENT, "hello")

    assert result == "sent"
    assert calls == [
        ("g0chat", "hello", {"reply_to_message_id": "42"}),
    ]


async def test_reply_forwards_extra_arguments():
    bot = make_bot()
    captured = {}

    async def fake_send(chat_id, text, **kwargs):
        captured.update(kwargs)

    bot.send_message = fake_send

    await bot.reply(EVENT, "x", disable_notification=True)

    assert captured["disable_notification"] is True


async def test_edit_passes_the_message_id():
    bot = make_bot()
    calls = []

    async def fake_edit(chat_id, message_id, text, **kwargs):
        calls.append((chat_id, message_id, text))

    bot.edit_message = fake_edit

    await bot.edit(EVENT, "updated")

    assert calls == [("g0chat", "42", "updated")]


async def test_delete_passes_the_message_id():
    bot = make_bot()
    calls = []

    async def fake_delete(chat_id, message_id):
        calls.append((chat_id, message_id))

    bot.delete_message = fake_delete

    await bot.delete(EVENT)

    assert calls == [("g0chat", "42")]


def test_reply_requires_a_chat_identifier():
    bot = make_bot()

    with pytest.raises(ValueError):
        bot._chat_id(SimpleNamespace())


def test_message_id_falls_back_to_id():
    bot = make_bot()

    assert bot._message_id(SimpleNamespace(id=7)) == 7


def test_message_id_missing_raises():
    bot = make_bot()

    with pytest.raises(ValueError):
        bot._message_id(SimpleNamespace())


# ---------------------------------------------------------------------------
# iter_updates
# ---------------------------------------------------------------------------


class FakeResponse(dict):
    pass


async def test_iter_updates_pages_until_the_cursor_stops():
    bot = make_bot()
    pages = [
        {"data": {"updates": [{"n": 1}, {"n": 2}], "next_offset_id": "b"}},
        {"data": {"updates": [{"n": 3}], "next_offset_id": None}},
    ]
    seen_offsets = []

    async def fake_get_updates(offset_id=None, limit=100):
        seen_offsets.append(offset_id)
        return FakeResponse(pages.pop(0))

    bot.get_updates = fake_get_updates

    updates = [update async for update in bot.iter_updates(limit=2)]

    assert [u["n"] for u in updates] == [1, 2, 3]
    assert seen_offsets == [None, "b"]


async def test_iter_updates_honours_max_pages():
    bot = make_bot()
    counter = {"n": 0}

    async def fake_get_updates(offset_id=None, limit=100):
        counter["n"] += 1
        page = counter["n"]
        return FakeResponse(
            {"data": {"updates": [{"n": page}], "next_offset_id": f"p{page}"}}
        )

    bot.get_updates = fake_get_updates

    updates = [u async for u in bot.iter_updates(max_pages=3)]

    assert len(updates) == 3


async def test_iter_updates_stops_when_the_cursor_does_not_advance():
    """A server that repeats its cursor must not loop forever."""
    bot = make_bot()
    calls = {"n": 0}

    async def fake_get_updates(offset_id=None, limit=100):
        calls["n"] += 1
        return FakeResponse(
            {"data": {"updates": [{"n": 1}], "next_offset_id": "stuck"}}
        )

    bot.get_updates = fake_get_updates

    updates = [u async for u in bot.iter_updates()]

    assert len(updates) == 2, "two pages, then the cursor stops advancing"
    assert calls["n"] == 2


async def test_iter_updates_stops_on_empty_page():
    bot = make_bot()

    async def fake_get_updates(offset_id=None, limit=100):
        return FakeResponse({"data": {"updates": [], "next_offset_id": "x"}})

    bot.get_updates = fake_get_updates

    assert [u async for u in bot.iter_updates()] == []


# ---------------------------------------------------------------------------
# on_error
# ---------------------------------------------------------------------------


def test_on_error_is_exposed_on_the_bot_instance():
    bot = make_bot()

    assert callable(bot.on_error)


async def test_report_error_calls_registered_handlers():
    bot = make_bot()
    seen = []

    @bot.on_error()
    async def handler(bot, exc, event):
        seen.append((type(exc).__name__, event))

    error = RuntimeError("boom")
    await bot._registry.report_error(error, EVENT)

    assert seen == [("RuntimeError", EVENT)]


async def test_report_error_without_handlers_is_safe():
    bot = make_bot()

    await bot._registry.report_error(RuntimeError("nobody listening"))


async def test_sync_error_handler_is_supported():
    bot = make_bot()
    seen = []

    @bot.on_error()
    def handler(bot, exc, event):
        seen.append(str(exc))

    await bot._registry.report_error(ValueError("sync"), None)

    assert seen == ["sync"]


async def test_failing_error_handler_does_not_propagate():
    bot = make_bot()

    @bot.on_error()
    async def broken(bot, exc, event):
        raise RuntimeError("handler failure")

    # Must not raise.
    await bot._registry.report_error(RuntimeError("original"), None)

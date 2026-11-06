"""Tests for darkob.testing and Event.when."""

from __future__ import annotations

from datetime import datetime, timezone


from darkob.testing import FakeBot, make_message
from darkob.types.event import Event


# ---------------------------------------------------------------------------
# FakeBot
# ---------------------------------------------------------------------------


async def test_fake_bot_records_calls():
    bot = FakeBot()

    await bot.send_message("g0chat", "hi", disable_notification=True)

    assert bot.called("send_message")
    assert bot.calls_to("send_message")[0][0] == ("g0chat", "hi")
    assert bot.calls_to("send_message")[0][1]["disable_notification"] is True


async def test_fake_bot_returns_an_ok_payload():
    bot = FakeBot()

    result = await bot.ban_member("g0chat", "u0user")

    assert result["status"] == "OK"
    assert result["method"] == "ban_member"


async def test_fake_bot_last_call_and_reset():
    bot = FakeBot()
    await bot.send_message("a", "1")
    await bot.edit_message("a", "2", "x")

    assert bot.last_call()[0] == "edit_message"

    bot.reset()

    assert bot.calls == []
    assert bot.last_call() is None


async def test_fake_bot_accepts_preset_attributes():
    bot = FakeBot(token="secret")

    assert bot.token == "secret"


def test_fake_bot_repr_shows_call_count():
    bot = FakeBot()

    assert "calls=0" in repr(bot)


# ---------------------------------------------------------------------------
# FakeEvent
# ---------------------------------------------------------------------------


async def test_fake_event_records_replies_and_edits():
    event = make_message(text="hello")

    await event.reply("a")
    await event.edit("b")
    await event.delete()

    assert event.replies == ["a"]
    assert event.edits == ["b"]
    assert event.deleted is True


def test_fake_event_has_default_identifiers():
    event = make_message()

    assert event.chat_id == "g0test"
    assert event.message_id == "1"
    assert event.author_id == "u0test"


def test_fake_event_accepts_extra_attributes():
    event = make_message(is_group=True)

    assert event.is_group is True


def test_fake_event_has_a_memo_dict():
    event = make_message()

    assert event._memo == {}


# ---------------------------------------------------------------------------
# Event.when
# ---------------------------------------------------------------------------


def test_when_parses_a_unix_timestamp():
    event = Event({"message": {"time": 1700000000}})

    assert event.when == datetime.fromtimestamp(1700000000, tz=timezone.utc)


def test_when_is_none_when_absent():
    assert Event({"message": {}}).when is None


def test_when_is_none_for_garbage():
    assert Event({"message": {"time": "not-a-number"}}).when is None


def test_when_accepts_a_numeric_string():
    event = Event({"message": {"time": "1700000000"}})

    assert event.when == datetime.fromtimestamp(1700000000, tz=timezone.utc)

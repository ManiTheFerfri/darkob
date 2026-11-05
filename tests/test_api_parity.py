"""Docs-backed additions: edit_message inline_keypad, remove_commands."""

from __future__ import annotations

from darkob import Bot, Keyboard

from conftest import VALID_TOKEN

CHAT = "g0" + "a" * 30


def make_bot() -> Bot:
    return Bot(token=VALID_TOKEN, show_welcome=False)


async def test_edit_message_sends_an_inline_keypad():
    bot = make_bot()
    captured = {}

    async def fake_request(method, endpoint, **kwargs):
        captured["endpoint"] = endpoint
        captured["payload"] = kwargs.get("json")
        return {"status": "OK"}

    bot.request = fake_request

    await bot.edit_message(
        CHAT, 42, "updated", inline_keypad=Keyboard().row("Yes", "No")
    )

    assert captured["endpoint"] == "editMessageText"
    keypad = captured["payload"]["inline_keypad"]
    assert keypad["rows"][0]["buttons"][0]["button_text"] == "Yes"
    assert all(button["id"] for button in keypad["rows"][0]["buttons"])


async def test_edit_message_without_a_keypad_omits_the_field():
    bot = make_bot()
    captured = {}

    async def fake_request(method, endpoint, **kwargs):
        captured["payload"] = kwargs.get("json")
        return {"status": "OK"}

    bot.request = fake_request

    await bot.edit_message(CHAT, 42, "plain")

    assert "inline_keypad" not in captured["payload"]


async def test_edit_message_accepts_a_raw_row_list():
    bot = make_bot()
    captured = {}

    async def fake_request(method, endpoint, **kwargs):
        captured["payload"] = kwargs.get("json")
        return {"status": "OK"}

    bot.request = fake_request

    await bot.edit_message(CHAT, 42, "x", inline_keypad=[["A", "B"]])

    buttons = captured["payload"]["inline_keypad"]["rows"][0]["buttons"]
    assert [b["button_text"] for b in buttons] == ["A", "B"]


async def test_remove_commands_calls_set_commands_with_an_empty_list():
    bot = make_bot()
    captured = {}

    async def fake_request(method, endpoint, **kwargs):
        captured["endpoint"] = endpoint
        captured["payload"] = kwargs.get("json")
        return {"status": "OK"}

    bot.request = fake_request

    await bot.remove_commands()

    assert captured["endpoint"] == "setCommands"
    assert captured["payload"] == {"bot_commands": []}


async def test_set_commands_with_an_empty_list_also_removes():
    bot = make_bot()
    captured = {}

    async def fake_request(method, endpoint, **kwargs):
        captured["payload"] = kwargs.get("json")
        return {"status": "OK"}

    bot.request = fake_request

    await bot.set_commands([])

    assert captured["payload"] == {"bot_commands": []}

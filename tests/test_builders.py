"""Tests for MessageBuilder."""

from __future__ import annotations

import pytest

from darkob.builders import MessageBuilder


def test_build_returns_text_only_by_default():
    assert MessageBuilder("hello").build() == {"text": "hello"}


def test_append_adds_a_new_line():
    assert MessageBuilder("a").append("b").text == "a\nb"


def test_append_uses_a_custom_separator():
    assert MessageBuilder("a").append("b", separator=" ").text == "a b"


def test_append_to_empty_starts_without_a_separator():
    assert MessageBuilder("").append("a").text == "a"


def test_line_with_no_argument_adds_a_blank_line():
    assert MessageBuilder("a").line().text == "a\n"


def test_set_text_replaces_everything():
    assert MessageBuilder("a").append("b").set_text("c").text == "c"


def test_options_are_only_emitted_when_set():
    builder = MessageBuilder("hi")

    assert builder.build() == {"text": "hi"}

    builder.silent()

    assert builder.build()["disable_notification"] is True


def test_keypad_and_inline_are_separate_options():
    payload = MessageBuilder("x").keypad("chat-kb").inline("inline-kb").build()

    assert payload["chat_keypad"] == "chat-kb"
    assert payload["inline_keypad"] == "inline-kb"


def test_reply_to_and_metadata():
    payload = (
        MessageBuilder("x").reply_to("42").metadata({"bold": []}).build()
    )

    assert payload["reply_to_message_id"] == "42"
    assert payload["metadata"] == {"bold": []}


def test_option_accepts_any_send_message_keyword():
    assert MessageBuilder("x").option("resize_keyboard", False).build()[
        "resize_keyboard"
    ] is False


def test_clear_options_keeps_the_text():
    builder = MessageBuilder("keep").silent().reply_to(1)
    builder.clear_options()

    assert builder.build() == {"text": "keep"}


def test_silent_can_be_disabled():
    assert MessageBuilder("x").silent(False).build()["disable_notification"] is False


def test_len_counts_text_characters():
    assert len(MessageBuilder("abc")) == 3


def test_repr_is_informative():
    assert "MessageBuilder" in repr(MessageBuilder("hi").silent())


def test_non_string_text_is_rejected():
    with pytest.raises(TypeError):
        MessageBuilder(123)

    with pytest.raises(TypeError):
        MessageBuilder("x").append(None)

    with pytest.raises(TypeError):
        MessageBuilder("x").set_text(5)


async def test_send_calls_the_bot():
    class FakeBot:
        def __init__(self):
            self.calls = []

        async def send_message(self, chat_id, **kwargs):
            self.calls.append((chat_id, kwargs))
            return "sent"

    bot = FakeBot()

    result = await MessageBuilder("hi").silent().send(bot, "g0chat")

    assert result == "sent"
    assert bot.calls == [("g0chat", {"text": "hi", "disable_notification": True})]

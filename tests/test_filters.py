"""Tests for the filter layer, including the TextMatch docstring regression."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from darkob.client.filters import (
    Command,
    HasMetadata,
    MetadataType,
    Text,
    TextMatch,
)


def make_event(text: str | None = None, message: dict | None = None) -> SimpleNamespace:
    """Build a minimal event shaped like the real one filters receive."""
    msg = message if message is not None else {}
    if text is not None:
        msg = {**msg, "text": text}
    return SimpleNamespace(original_data={"message": msg}, _memo={})


async def test_text_matches_substring():
    assert await Text("hello").evaluate(make_event("well hello there")) is True


async def test_text_does_not_match_other_text():
    assert await Text("hello").evaluate(make_event("goodbye")) is False


async def test_text_does_not_match_empty_message():
    assert await Text("hello").evaluate(make_event("")) is False


async def test_text_match_stores_the_match_on_the_event():
    """Regression: TextMatch used to raise SyntaxWarning on its own docstring."""
    event = make_event("my name is Ada")

    assert await TextMatch(r"name is (\w+)").evaluate(event) is True
    assert event._memo["_regex_match"].group(1) == "Ada"


async def test_text_match_false_when_no_match():
    event = make_event("nothing here")

    assert await TextMatch(r"(\d+)").evaluate(event) is False
    assert "_regex_match" not in event._memo


@pytest.mark.parametrize(
    "text,command,expected",
    [
        ("/start", "start", True),
        ("/start payload", "start", True),
        ("/start@my_bot", "start", True),
        ("/start", "help", False),
        ("start", "start", False),
        ("", "start", False),
    ],
)
async def test_command_matching(text, command, expected):
    assert await Command(command).evaluate(make_event(text)) is expected


async def test_command_without_a_name_matches_any_command():
    assert await Command().evaluate(make_event("/anything")) is True
    assert await Command().evaluate(make_event("not a command")) is False


async def test_filters_compose_with_boolean_operators():
    event = make_event("/start")

    assert await (Command("start") & Text("start")).evaluate(event) is True
    assert await (Command("help") | Text("start")).evaluate(event) is True
    assert await (~Command("start")).evaluate(event) is False


async def test_has_metadata():
    assert await HasMetadata().evaluate(
        make_event(message={"metadata": {"meta_data_parts": []}})
    ) is True
    assert await HasMetadata().evaluate(make_event("plain")) is False


async def test_metadata_type():
    event = make_event(
        message={"metadata": {"meta_data_parts": [{"type": "Bold"}]}}
    )

    assert await MetadataType("Bold").evaluate(event) is True
    assert await MetadataType("Italic").evaluate(event) is False

"""Tests for the documented Bot API enums and button builders."""

from __future__ import annotations

import json

import pytest

from darkob.bot.models import (
    ButtonCalendarType,
    ButtonLocationType,
    ButtonSelectionType,
    ButtonTextboxLine,
    ButtonType,
    ChatKeypadType,
    ChatType,
    EventType,
    FileType,
    ForwardedFrom,
    MessageSender,
    PaymentStatus,
    PollStatus,
)
from darkob.keyboards import Button, Keyboard


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "enum_member,wire_value",
    [
        (ButtonType.Simple, "Simple"),
        (ButtonType.Selection, "Selection"),
        (ButtonType.NumberPicker, "NumberPicker"),
        (ButtonType.AskMyPhoneNumber, "AskMyPhoneNumber"),
        (FileType.Voice, "Voice"),
        (ChatType.Channel, "Channel"),
        (ChatKeypadType.New, "New"),
        (ForwardedFrom.Bot, "Bot"),
        (PaymentStatus.NotPaid, "NotPaid"),
        (PollStatus.Closed, "Closed"),
        (MessageSender.User, "User"),
        (EventType.BotJoined, "BotJoined"),
        (ButtonCalendarType.DateGregorian, "DateGregorian"),
        (ButtonLocationType.Picker, "Picker"),
        (ButtonSelectionType.TextImgBig, "TextImgBig"),
        (ButtonTextboxLine.MultiLine, "MultiLine"),
    ],
)
def test_enum_values_match_the_wire_format(enum_member, wire_value):
    assert enum_member == wire_value
    assert json.dumps({"type": enum_member}) == json.dumps({"type": wire_value})


def test_none_valued_enums_use_the_wire_spelling():
    assert ChatKeypadType.None_ == "None"
    assert ButtonSelectionType.TextOnly == "TextOnly"


def test_every_button_type_is_covered():
    # The reference lists 19 button types.
    assert len(ButtonType) == 19


# ---------------------------------------------------------------------------
# Button builders
# ---------------------------------------------------------------------------


def test_simple_button():
    assert Button.simple("A").to_dict() == {"button_text": "A", "type": "Simple"}


def test_link_button():
    payload = Button.link("Site", "https://rubika.ir").to_dict()

    assert payload["type"] == "Link"
    assert payload["url"] == "https://rubika.ir"


def test_selection_button_keeps_documented_fields():
    payload = Button.selection(
        "Pick", title="Choose", items=[{"text": "A"}], columns_count=2
    ).to_dict()

    assert payload["type"] == "Selection"
    assert payload["title"] == "Choose"
    assert payload["columns_count"] == 2
    assert payload["items"] == [{"text": "A"}]


def test_calendar_button_only_sends_documented_fields():
    payload = Button.calendar("Date", min_year=2024, max_year=2030).to_dict()

    assert payload["type"] == "Calendar"
    assert payload["min_year"] == 2024
    assert payload["max_year"] == 2030
    # The reference does not name the Persian/Gregorian field, so we must
    # not invent one.
    assert "type_calendar" not in payload
    assert "calendar_type" not in payload


def test_location_button_uses_the_documented_image_field():
    payload = Button.location("Where", image_url="https://x/y.png").to_dict()

    assert payload["type"] == "Location"
    assert payload["location_image_url"] == "https://x/y.png"
    assert "location_type" not in payload


def test_textbox_does_not_invent_fields():
    payload = Button.text_box("Type").to_dict()

    assert payload["type"] == "Textbox"
    assert set(payload) == {"button_text", "type"}


def test_unknown_fields_pass_through():
    payload = Button.of("Barcode", "Scan", level=3).to_dict()

    assert payload["type"] == "Barcode"
    assert payload["level"] == 3


def test_none_fields_are_dropped():
    payload = Button.selection("Pick", title=None, columns_count=None).to_dict()

    assert "title" not in payload
    assert "columns_count" not in payload


def test_ask_helpers():
    assert Button.ask_my_phone("P").to_dict()["type"] == "AskMyPhoneNumber"
    assert Button.ask_my_location("L").to_dict()["type"] == "AskMyLocation"


def test_payment_requires_fields_because_the_api_rejects_a_bare_one():
    with pytest.raises(ValueError):
        Button.payment("Pay")

    payload = Button.payment("Pay", amount=1000).to_dict()

    assert payload["type"] == "Payment"
    assert payload["amount"] == 1000


def test_builders_compose_into_a_keyboard():
    keypad = Keyboard().row(
        Button.simple("Yes"),
        Button.link("Docs", "https://example.com"),
    )

    rows = keypad.to_dict()["rows"]

    assert [b["button_text"] for b in rows[0]["buttons"]] == ["Yes", "Docs"]
    assert rows[0]["buttons"][1]["type"] == "Link"

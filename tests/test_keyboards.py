"""Tests for the keyboard builders."""

from __future__ import annotations

import pytest

from darkob.bot.keypad_mixin import KeypadMixin
from darkob.keyboards import Button, ChatKeyboard, InlineKeyboard, Keyboard


def normalizer():
    class _M(KeypadMixin):
        pass

    return _M()


def test_keyboard_is_a_dict_with_rows():
    keyboard = Keyboard()

    assert isinstance(keyboard, dict)
    assert keyboard["rows"] == []


def test_row_chaining_appends_rows():
    keyboard = Keyboard().row("Yes", "No").row("Cancel")

    assert keyboard.row_count == 2
    assert keyboard.button_count == 3
    assert keyboard.rows[0]["buttons"] == ["Yes", "No"]
    assert keyboard.rows[1]["buttons"] == ["Cancel"]


def test_button_helper_adds_a_single_button_row():
    keyboard = Keyboard().button("Only")

    assert keyboard.row_count == 1
    assert keyboard.rows[0]["buttons"] == ["Only"]


def test_empty_row_is_rejected():
    with pytest.raises(ValueError):
        Keyboard().row()


def test_button_object_is_serialised():
    keyboard = Keyboard().row(Button("Go", id=7, type="Selection"))

    payload = keyboard.to_dict()["rows"][0]["buttons"][0]

    assert payload == {"button_text": "Go", "type": "Selection", "id": "7"}


def test_button_rejects_empty_text():
    with pytest.raises(ValueError):
        Button("")


def test_button_forwards_extra_fields():
    button = Button("Docs", url="https://example.com")

    assert button.to_dict()["url"] == "https://example.com"


def test_dict_buttons_pass_through():
    keyboard = Keyboard().row({"button_text": "X", "type": "Simple"})

    assert keyboard.rows[0]["buttons"][0] == {"button_text": "X", "type": "Simple"}


def test_unsupported_button_type_raises():
    with pytest.raises(TypeError):
        Keyboard().row(object())


def test_from_rows_builds_nested_mapping():
    keyboard = Keyboard.from_rows([["A", "B"], ["C"]])

    assert keyboard.row_count == 2
    assert keyboard.button_count == 3


def test_clear_and_reuse():
    keyboard = Keyboard().row("A")
    keyboard.clear()

    assert keyboard.row_count == 0
    assert keyboard.row("B").row_count == 1


def test_to_dict_is_a_copy():
    keyboard = Keyboard().row("A")
    snapshot = keyboard.to_dict()

    snapshot["rows"].append({"buttons": ["X"]})

    assert keyboard.row_count == 1


def test_aliases_point_at_the_same_class():
    assert InlineKeyboard is Keyboard
    assert ChatKeyboard is Keyboard


def test_normalizer_accepts_a_keyboard_and_fills_ids():
    keyboard = Keyboard().row("Yes", "No")

    normalized = normalizer()._normalize_keypad(keyboard, is_inline=True)

    assert normalized is not None
    buttons = normalized["rows"][0]["buttons"]
    assert [b["button_text"] for b in buttons] == ["Yes", "No"]
    assert all(b["id"] for b in buttons)
    assert all(b["type"] == "Simple" for b in buttons)


def test_normalizer_preserves_explicit_ids():
    keyboard = Keyboard().row(Button("Yes", id=5), "No")

    normalized = normalizer()._normalize_keypad(keyboard, is_inline=False)

    ids = [b["id"] for b in normalized["rows"][0]["buttons"]]
    assert "5" in ids


def test_inline_normalization_drops_keyboard_only_options():
    keyboard = Keyboard().row("A")

    normalized = normalizer()._normalize_keypad(keyboard, is_inline=True)

    assert "resize_keyboard" not in normalized
    assert "one_time_keyboard" not in normalized


def test_repr_is_informative():
    assert "rows=1" in repr(Keyboard().row("A"))

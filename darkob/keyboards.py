"""Keyboard and button builders.

Building a Rubika keypad by hand means nested ``rows`` / ``buttons``
dictionaries and manual button ids. These builders produce the exact
shape the API expects, so you can write::

    from darkob import Keyboard

    keypad = Keyboard().row("Yes", "No").row("Cancel")

    await bot.send_message(chat_id, "Continue?", inline_keypad=keypad)

A :class:`Keyboard` **is** a dict (``{"rows": [...]}``), so it can be
passed anywhere a raw keypad dict is accepted. The bot's normalizer fills
in ids and button types for anything left out.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Union, cast

__all__ = ["Button", "Keyboard", "InlineKeyboard", "ChatKeyboard"]

ButtonLike = Union[str, "Button", Dict[str, Any], Iterable[Any]]


class Button:
    """A single keypad button.

    Args:
        text: Label shown on the button.
        id: Explicit button id. Omit to let the API assign one.
        type: Button type passed through to the API (default ``"Simple"``).
        **extra: Any additional API fields, forwarded verbatim.
    """

    __slots__ = ("text", "id", "type", "extra")

    def __init__(
        self,
        text: str,
        *,
        id: Optional[Union[str, int]] = None,
        type: str = "Simple",
        **extra: Any,
    ) -> None:
        if not isinstance(text, str) or not text:
            raise ValueError("Button text must be a non-empty string.")
        self.text = text
        self.id = id
        self.type = type
        self.extra = {k: v for k, v in extra.items() if v is not None}

    # -- documented button types -----------------------------------------
    # Field names follow the models page of the Bot API reference. Values
    # the API does not need are omitted rather than sent as null.

    @classmethod
    def of(cls, button_type: str, text: str, **fields: Any) -> "Button":
        """Build any button type by name, forwarding documented fields."""
        return cls(
            text,
            type=button_type,
            **{k: v for k, v in fields.items() if v is not None},
        )

    @classmethod
    def simple(cls, text: str, **fields: Any) -> "Button":
        """A plain button (``Simple``)."""
        return cls(text, type="Simple", **fields)

    @classmethod
    def link(cls, text: str, url: str, **fields: Any) -> "Button":
        """A button that opens a URL (``Link``)."""
        return cls(text, type="Link", url=url, **fields)

    @classmethod
    def selection(
        cls,
        text: str,
        title: Optional[str] = None,
        items: Optional[List[Dict[str, Any]]] = None,
        columns_count: Optional[int] = None,
        is_multi_selection: Optional[bool] = None,
        selection_id: Optional[str] = None,
        get: Optional[str] = None,
        search: Optional[str] = None,
        **fields: Any,
    ) -> "Button":
        """A list picker (``Selection``)."""
        return cls(
            text,
            type="Selection",
            title=title,
            items=items,
            columns_count=columns_count,
            is_multi_selection=is_multi_selection,
            selection_id=selection_id,
            get=get,
            search=search,
            **fields,
        )

    @classmethod
    def calendar(
        cls,
        text: str,
        title: Optional[str] = None,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
        **fields: Any,
    ) -> "Button":
        """A date picker; ``calendar_type`` is DatePersian or DateGregorian."""
        return cls(
            text,
            type="Calendar",
            title=title,
            min_year=min_year,
            max_year=max_year,
            **fields,
        )

    @classmethod
    def number_picker(
        cls,
        text: str,
        title: Optional[str] = None,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
        **fields: Any,
    ) -> "Button":
        """A numeric range picker (``NumberPicker``)."""
        return cls(
            text,
            type="NumberPicker",
            title=title,
            min_value=min_value,
            max_value=max_value,
            **fields,
        )

    @classmethod
    def string_picker(
        cls,
        text: str,
        title: Optional[str] = None,
        items: Optional[List[str]] = None,
        **fields: Any,
    ) -> "Button":
        """A picker over a fixed list of strings (``StringPicker``)."""
        return cls(text, type="StringPicker", title=title, items=items, **fields)

    @classmethod
    def location(
        cls,
        text: str,
        image_url: Optional[str] = None,
        **fields: Any,
    ) -> "Button":
        """A location button; ``location_type`` is Picker or View."""
        return cls(
            text,
            type="Location",
            location_image_url=image_url,
            **fields,
        )

    @classmethod
    def text_box(
        cls,
        text: str,
        **fields: Any,
    ) -> "Button":
        """Opens a text input. keypad_type: String|Number; line_type: SingleLine|MultiLine."""
        return cls(
            text,
            type="Textbox",
            **fields,
        )

    @classmethod
    def ask_my_phone(cls, text: str, **fields: Any) -> "Button":
        """Asks the user to share their phone number."""
        return cls(text, type="AskMyPhoneNumber", **fields)

    @classmethod
    def ask_my_location(cls, text: str, **fields: Any) -> "Button":
        """Asks the user to share their location."""
        return cls(text, type="AskMyLocation", **fields)

    @classmethod
    def barcode(cls, text: str, **fields: Any) -> "Button":
        """Opens the barcode scanner."""
        return cls(text, type="Barcode", **fields)

    @classmethod
    def payment(cls, text: str, **fields: Any) -> "Button":
        """A payment button.

        Unlike the other types, a bare `Payment` button is rejected by
        the live API with `INVALID_INPUT`: it needs its own fields
        (amount, currency and so on), which the reference does not
        document here. Pass them through `**fields`; this helper refuses
        to build one without them rather than fail at send time.
        """
        if not fields:
            raise ValueError(
                "A Payment button needs additional API fields; the API "
                "rejects a bare one with INVALID_INPUT. Pass them as "
                "keyword arguments."
            )
        return cls(text, type="Payment", **fields)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"button_text": self.text, "type": self.type}
        if self.id is not None:
            payload["id"] = str(self.id)
        payload.update(self.extra)
        return payload

    def __repr__(self) -> str:
        return f"Button({self.text!r})"


def _as_button(value: ButtonLike) -> Any:
    if isinstance(value, Button):
        return value.to_dict()
    if isinstance(value, (str, dict)):
        return value
    if isinstance(value, (tuple, list)):
        return list(value)
    raise TypeError(
        f"Unsupported button type {type(value).__name__}: "
        "use a string, Button, dict or tuple."
    )


class Keyboard(Dict[str, Any]):
    """An API-ready keypad: ``{"rows": [{"buttons": [...]}, ...]}``."""

    def __init__(self, *rows: Iterable[ButtonLike]) -> None:
        super().__init__(rows=[])
        for row in rows:
            if isinstance(row, (list, tuple)):
                self.row(*row)
            else:
                self.row(row)

    @property
    def rows(self) -> List[Dict[str, Any]]:
        """The mutable row list (each row is ``{"buttons": [...]}``)."""
        return cast(List[Dict[str, Any]], self["rows"])

    def row(self, *buttons: ButtonLike) -> "Keyboard":
        """Append one row of buttons. Returns the keyboard for chaining."""
        if not buttons:
            raise ValueError("A keyboard row needs at least one button.")
        self.rows.append({"buttons": [_as_button(b) for b in buttons]})
        return self

    def button(self, button: ButtonLike) -> "Keyboard":
        """Append a single button as its own row."""
        return self.row(button)

    def clear(self) -> "Keyboard":  # type: ignore[override]
        """Remove every row. Returns the keyboard for chaining."""
        self.rows.clear()
        return self

    @property
    def row_count(self) -> int:
        return len(self.rows)

    @property
    def button_count(self) -> int:
        return sum(len(row.get("buttons", [])) for row in self.rows)

    def to_dict(self) -> Dict[str, Any]:
        """Return a deep-ish copy as a plain dict."""
        return {
            "rows": [
                {"buttons": [dict(b) if isinstance(b, dict) else b for b in row["buttons"]]}
                for row in self.rows
            ]
        }

    @classmethod
    def from_rows(cls, rows: Iterable[Iterable[ButtonLike]]) -> "Keyboard":
        """Build a keyboard from a list of rows."""
        keyboard = cls()
        for row in rows:
            keyboard.row(*row)
        return keyboard

    def __repr__(self) -> str:
        return f"Keyboard(rows={self.row_count}, buttons={self.button_count})"


#: Inline keypads and chat keypads share one representation.
InlineKeyboard = Keyboard
ChatKeyboard = Keyboard

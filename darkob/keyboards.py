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

from typing import Any, Dict, Iterable, List, Optional, Union

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
        self.extra = extra

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


class Keyboard(dict):
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
        return self["rows"]

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

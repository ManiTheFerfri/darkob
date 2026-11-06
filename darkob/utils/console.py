"""Minimal console output that upgrades to rich when it is installed.

`rich` used to be a mandatory dependency purely for a banner and a few
prompts. It is now optional: when present this delegates to it, otherwise a
tiny stand-in keeps the same tiny API surface the library actually uses.
"""

from __future__ import annotations

import sys
from typing import Any, Optional, TextIO

__all__ = ["Console", "Text", "HAS_RICH"]

HAS_RICH = False

try:  # pragma: no cover - depends on the environment
    from rich.console import Console as _RichConsole
    from rich.text import Text as _RichText

    HAS_RICH = True
    Console = _RichConsole  # type: ignore[assignment,misc]
    Text = _RichText  # type: ignore[assignment,misc]

except ImportError:  # pragma: no cover

    class Text:  # type: ignore[no-redef]
        """Plain-text stand-in for ``rich.text.Text``."""

        __slots__ = ("_parts",)

        def __init__(self, text: str = "") -> None:
            self._parts: list[str] = [text] if text else []

        def append(self, text: str, style: Optional[str] = None) -> "Text":
            self._parts.append(text)
            return self

        def __str__(self) -> str:
            return "".join(self._parts)

        def __repr__(self) -> str:
            return f"Text({str(self)!r})"

    class Console:  # type: ignore[no-redef]
        """Plain-output stand-in for ``rich.console.Console``."""

        def __init__(self, *, stderr: bool = False, highlight: bool = False, **_: Any) -> None:
            self._stream: TextIO = sys.stderr if stderr else sys.stdout

        def print(self, *objects: Any, end: str = "\n", **_: Any) -> None:
            text = " ".join(str(item) for item in objects)
            self._stream.write(text + end)
            self._stream.flush()

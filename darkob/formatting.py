"""Text formatting helpers for Rubika's metadata markdown.

Rubika renders a small Markdown-like dialect. Building these strings by
hand is error-prone and easy to get subtly wrong, so use the helpers::

    from darkob import bold, link, code

    await event.reply(f"{bold('Deployed')} — see {link('logs', url)}")

Every helper accepts ``str`` and returns ``str``, so they compose
freely inside f-strings.
"""

from __future__ import annotations

from typing import Iterable, Optional

__all__ = [
    "bold",
    "italic",
    "strike",
    "underline",
    "spoiler",
    "code",
    "pre",
    "link",
    "join",
]


def bold(text: str) -> str:
    """``**text**``"""
    return f"**{text}**"


def italic(text: str) -> str:
    """``__text__``"""
    return f"__{text}__"


def strike(text: str) -> str:
    """``~~text~~``"""
    return f"~~{text}~~"


def underline(text: str) -> str:
    """``--text--``"""
    return f"--{text}--"


def spoiler(text: str) -> str:
    """``||text||`` — hidden until the user taps it."""
    return f"||{text}||"


def code(text: str) -> str:
    """``\\`text\\`` — inline monospace."""
    return f"`{text}`"


def pre(text: str, language: Optional[str] = None) -> str:
    """A fenced code block, optionally with a language hint."""
    fence = f"```{language}" if language else "```"
    return f"{fence}\n{text}\n```"


def link(text: str, url: str) -> str:
    """``[text](url)``"""
    if not url:
        raise ValueError("link() needs a non-empty url.")
    return f"[{text}]({url})"


def join(parts: Iterable[str], separator: str = " ") -> str:
    """Join already-formatted fragments, skipping empty ones."""
    return separator.join(part for part in parts if part)

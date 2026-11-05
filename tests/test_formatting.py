"""Tests for the text formatting helpers."""

from __future__ import annotations

import pytest

from darkob.formatting import (
    bold,
    code,
    italic,
    join,
    link,
    pre,
    spoiler,
    strike,
    underline,
)


@pytest.mark.parametrize(
    "func,expected",
    [
        (bold, "**hi**"),
        (italic, "__hi__"),
        (strike, "~~hi~~"),
        (underline, "--hi--"),
        (spoiler, "||hi||"),
        (code, "`hi`"),
    ],
)
def test_wrappers(func, expected):
    assert func("hi") == expected


def test_pre_without_language():
    assert pre("x = 1") == "```\nx = 1\n```"


def test_pre_with_language():
    assert pre("x = 1", "python") == "```python\nx = 1\n```"


def test_link():
    assert link("docs", "https://e.com") == "[docs](https://e.com)"


def test_link_requires_url():
    with pytest.raises(ValueError):
        link("docs", "")


def test_join_skips_empty_fragments():
    assert join(["a", "", "b"]) == "a b"


def test_join_uses_separator():
    assert join(["a", "b"], separator="\n") == "a\nb"


def test_helpers_compose_in_an_fstring():
    message = f"{bold('Deployed')} {link('logs', 'https://e.com')}"

    assert message == "**Deployed** [logs](https://e.com)"


def test_formatting_does_not_mutate_input():
    text = "hello"
    bold(text)

    assert text == "hello"

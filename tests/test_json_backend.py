"""Tests for the JSON backend and the optional-dependency diet."""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

from darkob.utils import json_backend as jb

REPO_ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# JSON backend
# ---------------------------------------------------------------------------


def test_backend_is_reported():
    assert jb.BACKEND in {"msgspec", "stdlib"}


def test_roundtrip_dict():
    payload = {"status": "OK", "data": {"nested": [1, 2, 3]}}

    assert jb.loads(jb.dumps(payload)) == payload


def test_roundtrip_unicode():
    payload = {"text": "سلام دنیا"}

    assert jb.loads(jb.dumps_bytes(payload)) == payload


def test_dumps_is_compact():
    text = jb.dumps({"a": 1, "b": 2})

    assert " " not in text


def test_loads_accepts_bytes_and_str():
    raw = jb.dumps({"a": 1})

    assert jb.loads(raw) == jb.loads(raw.encode("utf-8")) == {"a": 1}


def test_loads_matches_stdlib_on_typical_payloads():
    sample = '{"method":"sendMessage","input":{"text":"hi","n":3},"ok":true}'

    assert jb.loads(sample) == json.loads(sample)


@dataclass
class Point:
    x: int
    y: int


def test_convert_builds_a_typed_object():
    result = jb.convert({"x": 1, "y": 2, "ignored": 3}, Point)

    assert (result.x, result.y) == (1, 2)


def test_dumps_handles_nested_lists():
    payload = [{"a": [1, 2]}, {"b": None}]

    assert jb.loads(jb.dumps(payload)) == payload


@pytest.mark.parametrize("bad", ["{not json", "", "'"])
def test_loads_raises_on_invalid_input(bad):
    with pytest.raises(Exception):
        jb.loads(bad)


# ---------------------------------------------------------------------------
# Optional dependency diet
# ---------------------------------------------------------------------------


BLOCKED_SCRIPT = '''
import sys
import importlib.abc


class Blocker(importlib.abc.MetaPathFinder):
    def find_spec(self, name, path=None, target=None):
        root = name.split(".")[0]
        if root in {"mutagen", "rich"}:
            raise ImportError(f"{root} is blocked for this test")
        return None


sys.meta_path.insert(0, Blocker())

import darkob
from darkob import Bot
from darkob.client.core.media import Audio
from darkob.utils import HAS_RICH

print("HAS_RICH:", HAS_RICH)
print("audio:", Audio.get_audio_info(b"\\x00" * 64))
darkob.show_welcome_message(True)
print("IMPORT-OK")
'''


def test_package_imports_without_mutagen_or_rich():
    """Neither mutagen nor rich may be required at import time."""
    result = subprocess.run(
        [sys.executable, "-c", BLOCKED_SCRIPT],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=180,
    )

    assert result.returncode == 0, result.stderr
    assert "IMPORT-OK" in result.stdout
    assert "HAS_RICH: False" in result.stdout, "the console shim should be active"


def test_media_module_is_free_of_mutagen():
    source = (
        REPO_ROOT / "darkob" / "client" / "core" / "media.py"
    ).read_text(encoding="utf-8")

    assert "import mutagen" not in source
    assert "mutagen.File" not in source


def test_no_module_imports_rich_directly():
    offenders = []
    for path in (REPO_ROOT / "darkob").rglob("*.py"):
        if path.name == "console.py":
            continue  # the shim itself is allowed to probe for rich
        text = path.read_text(encoding="utf-8")
        if "from rich" in text or "import rich" in text:
            offenders.append(path.name)

    assert offenders == [], f"use darkob.utils.console instead: {offenders}"

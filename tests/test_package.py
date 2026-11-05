"""Package-level guarantees: version, upstream attribution, update-check safety."""

from __future__ import annotations

import urllib.error
import urllib.request

import pytest

import darkob
from darkob import _parse_version


def test_version_matches_pyproject():
    """Guards against the packaged metadata drifting from __version__."""
    import pathlib
    import re

    pyproject = pathlib.Path(__file__).resolve().parents[1] / "pyproject.toml"
    match = re.search(
        r'^version\s*=\s*"([^"]+)"', pyproject.read_text(encoding="utf-8"), re.M
    )

    assert match is not None, "pyproject.toml has no version"
    assert darkob.__version__ == match.group(1)


def test_upstream_attribution_is_preserved():
    """MIT requires keeping the original author's notice."""
    assert darkob.__author__ == "MEHRAB Farahmand"


def test_check_for_updates_returns_none_when_offline(monkeypatch):
    def _offline(*args, **kwargs):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(urllib.request, "urlopen", _offline)

    assert darkob.check_for_updates("0.1.0") is None


def test_check_for_updates_returns_none_when_already_latest(monkeypatch):
    import json

    class _Response:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self):
            return json.dumps({"info": {"version": "0.1.0"}}).encode()

    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **k: _Response())

    assert darkob.check_for_updates("0.1.0") is None


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("1.2.3", (1, 2, 3)),
        ("0.1.0", (0, 1, 0)),
        ("1.2.0rc1", (1, 2, 1)),
        ("2", (2,)),
    ],
)
def test_parse_version_is_tolerant(raw, expected):
    assert _parse_version(raw) == expected


def test_client_request_module_imports_data():
    """Regression: ``client/base/request.py`` used ``Data`` without importing it.

    That branch returned ``Data({})`` and would have raised ``NameError`` at
    runtime instead of returning an empty response.
    """
    from darkob.client.base import request as request_module
    from darkob.data import Data

    assert request_module.Data is Data

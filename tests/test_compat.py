"""Tests for the maxrubika compatibility shim."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import darkob
import darkob.compat.maxrubika as shim

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_shim_reexports_everything_darkob_exports():
    missing = [name for name in darkob.__all__ if not hasattr(shim, name)]

    assert missing == [], f"not re-exported: {missing}"


def test_core_classes_are_the_same_objects():
    assert shim.Messenger is darkob.Messenger
    assert shim.Bot is darkob.Bot
    assert shim.Client is darkob.Client
    assert shim.Shad is darkob.Shad


def test_darkob_only_names_are_reachable():
    """A half-migrated file may have started using new APIs already."""
    assert shim.Router is darkob.Router
    assert shim.FSMContext is darkob.FSMContext
    assert shim.MessageBuilder is darkob.MessageBuilder


def test_version_reports_the_installed_package():
    assert shim.__version__ == darkob.__version__
    assert shim.__maxrubika_version__ == "1.18.0"


def test_unknown_name_raises_a_clear_error():
    try:
        shim.does_not_exist
    except AttributeError as exc:
        assert "does_not_exist" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected AttributeError")


def test_importing_the_shim_warns_once():
    code = """
import warnings
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    import darkob.compat.maxrubika  # noqa: F401
print(len([w for w in caught if w.category is DeprecationWarning]))
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "1"


def test_a_maxrubika_style_script_imports_cleanly():
    script = """
import warnings
warnings.simplefilter("ignore", DeprecationWarning)
from darkob.compat.maxrubika import Messenger, Bot, bot, messenger
print("IMPORTED")
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )

    assert result.returncode == 0, result.stderr
    assert "IMPORTED" in result.stdout

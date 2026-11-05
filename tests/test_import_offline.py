"""Importing darkob, and showing its banner, must never touch the network.

These run in a subprocess so the network guard is actually in place before
``darkob`` is imported.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

_GUARD = """
import socket

def _blocked(*args, **kwargs):
    raise AssertionError("network access attempted during import")

socket.socket.connect = _blocked
socket.create_connection = _blocked

{body}
print("GUARD-OK")
"""


def _run(body: str) -> subprocess.CompletedProcess:
    code = _GUARD.format(body=body)
    return subprocess.run(
        [sys.executable, "-c", code],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=180,
    )


def test_import_does_not_touch_network():
    result = _run("import darkob")
    assert result.returncode == 0, result.stderr
    assert "GUARD-OK" in result.stdout


def test_welcome_banner_does_not_touch_network():
    result = _run("import darkob\ndarkob.show_welcome_message(True)")
    assert result.returncode == 0, result.stderr
    assert "GUARD-OK" in result.stdout


def test_check_for_updates_is_not_called_automatically():
    """The update check is opt-in: importing and constructing must stay silent."""
    body = (
        "import darkob\n"
        "calls = []\n"
        "darkob.check_for_updates = lambda *a, **k: calls.append(1)\n"
        "darkob.show_welcome_message(True)\n"
        "assert not calls, 'check_for_updates must not run automatically'\n"
    )
    result = _run(body)
    assert result.returncode == 0, result.stderr

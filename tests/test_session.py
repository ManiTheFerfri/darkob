"""Regression tests for session persistence.

These cover the "my login disappeared" failures: sessions stored relative
to the cwd, and session files being deleted when they could not be read.
"""

from __future__ import annotations

import os

import pytest

from darkob.client.core.session import (
    SESSION_DIR_ENV,
    Session,
    default_session_dir,
    resolve_session_path,
)

CREDENTIALS = dict(
    phone_number="+989000000000",
    auth="a" * 32,
    guid="u0abc",
    user_agent="darkob-tests",
    private_key="key",
)


@pytest.fixture(autouse=True)
def isolated_session_dir(tmp_path, monkeypatch):
    """Redirect the default session directory into a temp folder."""
    target = tmp_path / "sessions"
    monkeypatch.setenv(SESSION_DIR_ENV, str(target))
    return target


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------


def test_default_dir_honours_the_override(isolated_session_dir):
    assert default_session_dir() == str(isolated_session_dir)


def test_bare_name_resolves_into_the_session_dir(isolated_session_dir):
    resolved = resolve_session_path("darkob_abc")

    assert os.path.dirname(resolved) == str(isolated_session_dir)
    assert resolved.endswith("darkob_abc")


def test_absolute_path_is_used_verbatim(tmp_path):
    target = str(tmp_path / "explicit.max")

    assert resolve_session_path(target) == target


def test_relative_path_with_directory_is_used_verbatim():
    assert resolve_session_path(os.path.join("sub", "x.max")) == os.path.join(
        "sub", "x.max"
    )


def test_legacy_file_in_cwd_wins(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    legacy = tmp_path / "darkob_legacy"
    legacy.write_bytes(b"anything")

    assert resolve_session_path("darkob_legacy") == "darkob_legacy"


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------


def test_session_roundtrip_persists_credentials():
    session = Session("roundtrip", create_file=True)
    session.insert(**CREDENTIALS)
    session.close()

    reopened = Session("roundtrip")
    info = reopened.information()

    assert reopened.is_logged_in is True
    assert info[0] == CREDENTIALS["phone_number"]
    assert info[1] == CREDENTIALS["auth"]
    assert info[2] == CREDENTIALS["guid"]
    reopened.close()


def test_session_survives_a_directory_change(tmp_path, monkeypatch):
    """The cwd must not decide where a session lives."""
    first = Session("stable", create_file=True)
    first.insert(**CREDENTIALS)
    first.close()

    other = tmp_path / "elsewhere"
    other.mkdir()
    monkeypatch.chdir(other)

    reopened = Session("stable")

    assert reopened.is_logged_in is True
    assert reopened.information()[1] == CREDENTIALS["auth"]
    reopened.close()


def test_missing_session_is_not_logged_in(isolated_session_dir):
    session = Session("does-not-exist")

    assert session.is_logged_in is False
    session.close()


# ---------------------------------------------------------------------------
# Corruption handling
# ---------------------------------------------------------------------------


def test_unreadable_session_is_quarantined_not_deleted(isolated_session_dir):
    path = isolated_session_dir / "broken.max"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"not a sqlite database")

    session = Session("broken")

    assert session.is_logged_in is False
    assert not path.exists(), "the unreadable file must be moved aside"

    quarantined = list(isolated_session_dir.glob("broken.max.corrupt-*"))
    assert quarantined, "the original bytes must be preserved for recovery"
    assert quarantined[0].read_bytes() == b"not a sqlite database"

    session.close()


def test_corruption_does_not_destroy_a_later_login(isolated_session_dir):
    path = isolated_session_dir / "recover.max"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"garbage")

    Session("recover").close()

    fresh = Session("recover", create_file=True)
    fresh.insert(**CREDENTIALS)
    fresh.close()

    reopened = Session("recover")

    assert reopened.is_logged_in is True
    assert reopened.information()[0] == CREDENTIALS["phone_number"]
    reopened.close()

"""Tests for the CLI: scaffolding, session listing, diagnostics, parsing."""

from __future__ import annotations

import argparse
from pathlib import Path

import pytest

from darkob import cli
from darkob.client.core.session import SESSION_DIR_ENV


@pytest.fixture(autouse=True)
def isolated_session_dir(tmp_path, monkeypatch):
    target = tmp_path / "sessions"
    monkeypatch.setenv(SESSION_DIR_ENV, str(target))
    return target


def test_parser_exposes_every_command():
    parser = cli.build_parser()
    args = parser.parse_args([])

    assert args.command is None

    for command in ("login", "sessions", "new", "run", "doctor", "version"):
        parsed = parser.parse_args([command] + (["x"] if command in {"new", "run"} else []))
        assert parsed.command == command


def test_version_command_prints_version(capsys):
    assert cli.main(["version"]) == 0

    out = capsys.readouterr().out
    import darkob

    assert darkob.__version__ in out


def test_sessions_is_empty_initially(capsys):
    assert cli.main(["sessions"]) == 0

    out = capsys.readouterr().out
    assert "No sessions yet" in out or "sessions" in out.lower()


def test_sessions_lists_saved_files(isolated_session_dir, capsys):
    isolated_session_dir.mkdir(parents=True, exist_ok=True)
    (isolated_session_dir / "alpha.max").write_bytes(b"x" * 10)

    assert cli.main(["sessions"]) == 0

    assert "alpha" in capsys.readouterr().out


def test_new_scaffolds_a_project(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    assert cli.main(["new", "mybot"]) == 0

    project = tmp_path / "mybot"
    assert (project / "main.py").exists()
    assert (project / "routers" / "general.py").exists()
    assert (project / "routers" / "__init__.py").exists()
    assert (project / "config.py").exists()
    assert (project / ".env.example").exists()
    assert "Router" in (project / "routers" / "general.py").read_text()


def test_new_refuses_to_overwrite(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    project = tmp_path / "mybot"
    project.mkdir()
    (project / "existing.txt").write_text("keep me")

    assert cli.main(["new", "mybot"]) == 1

    assert (project / "existing.txt").read_text() == "keep me"


def test_run_missing_file_fails(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    assert cli.main(["run", "nope.py"]) == 1


def test_run_executes_a_script(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    script = tmp_path / "job.py"
    marker = tmp_path / "ran.txt"
    script.write_text(
        f"from pathlib import Path\nPath({str(marker)!r}).write_text('yes')\n",
        encoding="utf-8",
    )

    assert cli.main(["run", str(script)]) == 0
    assert marker.read_text() == "yes"


def test_run_sets_main_name(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    script = tmp_path / "name.py"
    marker = tmp_path / "name.txt"
    script.write_text(
        f"from pathlib import Path\nPath({str(marker)!r}).write_text(__name__)\n",
        encoding="utf-8",
    )

    cli.main(["run", str(script)])

    assert marker.read_text() == "__main__"


def test_doctor_runs_and_reports(capsys):
    assert cli.main(["doctor"]) == 0

    out = capsys.readouterr().out
    assert "Python" in out
    assert "darkob" in out


def test_main_without_command_prints_help(capsys):
    assert cli.main([]) == 0

    out = capsys.readouterr().out
    assert "usage" in out.lower()


def test_format_age_units():
    import time as time_module

    now = time_module.time()

    assert cli._format_age(now - 5).endswith("s ago")
    assert cli._format_age(now - 120).endswith("m ago")
    assert cli._format_age(now - 7200).endswith("h ago")
    assert cli._format_age(now - 172800).endswith("d ago")


def test_login_parser_defaults():
    parser = cli.build_parser()
    args = parser.parse_args(["login"])

    assert args.func is cli.cmd_login
    assert args.session is None


def test_new_parser_requires_a_name():
    parser = cli.build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(["new"])

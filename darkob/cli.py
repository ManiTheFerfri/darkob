"""The `darkob` command line interface.

Designed so the first thing a new user runs is a guided login, and
everything after that is one word::

    darkob login          # interactive: phone, code, session saved
    darkob sessions       # what logins do I have?
    darkob doctor         # is my environment sane?
    darkob new mybot      # scaffold a project
    darkob run bot.py     # run it

No secret flags are required to get started.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
import time
from pathlib import Path
from typing import List, Optional

try:  # rich is a hard dependency, but keep the CLI usable without it
    from rich.console import Console

    console: Optional[Console] = Console()
except ImportError:  # pragma: no cover
    console = None


# ---------------------------------------------------------------------------
# output helpers
# ---------------------------------------------------------------------------


def _print(message: str = "") -> None:
    if console is not None:
        console.print(message)
    else:  # pragma: no cover
        print(message)


def _ok(message: str) -> None:
    _print(f"[bold green]✓[/] {message}")


def _warn(message: str) -> None:
    _print(f"[bold yellow]![/] {message}")


def _fail(message: str) -> None:
    _print(f"[bold red]✗[/] {message}")


def _heading(message: str) -> None:
    _print(f"\n[bold cyan]{message}[/]")


# ---------------------------------------------------------------------------
# sessions
# ---------------------------------------------------------------------------


def _session_dir() -> Path:
    from darkob.client.core.session import default_session_dir

    return Path(default_session_dir())


def _list_sessions() -> List[Path]:
    directory = _session_dir()
    if not directory.exists():
        return []
    return sorted(
        (path for path in directory.glob("*.max") if path.is_file()),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )


def _format_age(timestamp: float) -> str:
    delta = max(0, int(time.time() - timestamp))
    if delta < 60:
        return f"{delta}s ago"
    if delta < 3600:
        return f"{delta // 60}m ago"
    if delta < 86400:
        return f"{delta // 3600}h ago"
    return f"{delta // 86400}d ago"


def cmd_sessions(args: argparse.Namespace) -> int:
    directory = _session_dir()
    sessions = _list_sessions()

    _heading("Sessions")
    _print(f"[dim]directory: {directory}[/]")

    if not sessions:
        _warn("No sessions yet. Run [bold]darkob login[/] to create one.")
        return 0

    for path in sessions:
        stat = path.stat()
        _print(
            f"  [bold]{path.stem}[/]  "
            f"[dim]{stat.st_size} bytes · {_format_age(stat.st_mtime)}[/]"
        )

    return 0


def cmd_login(args: argparse.Namespace) -> int:
    from darkob import Messenger
    from darkob.client.core.cipher import Cipher

    name = args.session or "darkob_default"

    _heading("Login")
    _print(f"[dim]session: {name}[/]")

    existing = None
    candidate = _session_dir() / f"{name}.max"
    if candidate.exists():
        existing = candidate

    async def _run() -> None:
        if existing is not None:
            client = Messenger(session=name, show_welcome=False)
            if client.auth:
                _ok("Existing session restored — no login needed.")
                _print(f"[dim]{existing}[/]")
                return
            _warn("Existing session could not be reused; starting a fresh login.")

        # Fresh registration: a throwaway request secret plus real RSA keys.
        _, private_key = Cipher.create_keys()
        client = Messenger(
            auth=Cipher.secret(32),
            private_key=private_key,
            session=name,
            show_welcome=False,
        )
        await client.start()

        saved = getattr(getattr(client, "session", None), "filename", None)
        if saved:
            _ok(f"Login complete. Session saved to {os.path.abspath(saved)}")
        else:
            _ok("Login complete.")
        await client.close()

    try:
        asyncio.run(_run())
    except KeyboardInterrupt:
        _warn("Cancelled.")
        return 130

    return 0


# ---------------------------------------------------------------------------
# project scaffolding
# ---------------------------------------------------------------------------

MAIN_TEMPLATE = '''"""Entry point for {name}."""

from darkob import Bot

from routers import general

bot = Bot(token="YOUR_BOT_TOKEN")

bot.include_router(general.router)

if __name__ == "__main__":
    bot.run()
'''

ROUTER_TEMPLATE = '''"""Handlers for {name}."""

from darkob import Router

router = Router("{name}")


@router.command("start")
async def start(bot, event):
    await event.reply("Hello from {name}!")
'''

CONFIG_TEMPLATE = '''"""Configuration, loaded from the environment."""

import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
'''

ENV_TEMPLATE = '''# Copy to .env and fill in
BOT_TOKEN=
'''

README_TEMPLATE = '''# {name}

A darkob bot.

```bash
pip install darkob
export BOT_TOKEN=...
python main.py
```
'''


def cmd_new(args: argparse.Namespace) -> int:
    target = Path(args.name)
    if target.exists() and any(target.iterdir()):
        _fail(f"{target} already exists and is not empty.")
        return 1

    (target / "routers").mkdir(parents=True, exist_ok=True)
    (target / "routers" / "__init__.py").write_text("", encoding="utf-8")
    (target / "routers" / "general.py").write_text(
        ROUTER_TEMPLATE.format(name=args.name), encoding="utf-8"
    )
    (target / "main.py").write_text(
        MAIN_TEMPLATE.format(name=args.name), encoding="utf-8"
    )
    (target / "config.py").write_text(CONFIG_TEMPLATE, encoding="utf-8")
    (target / ".env.example").write_text(ENV_TEMPLATE, encoding="utf-8")
    (target / "README.md").write_text(
        README_TEMPLATE.format(name=args.name), encoding="utf-8"
    )

    _ok(f"Created {target}")
    _print("\nNext:")
    _print(f"  cd {target}")
    _print("  export BOT_TOKEN=...")
    _print("  python main.py")
    return 0


# ---------------------------------------------------------------------------
# running a bot
# ---------------------------------------------------------------------------


def cmd_run(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.exists():
        _fail(f"No such file: {path}")
        return 1

    sys.argv = [str(path)] + list(args.arguments or [])
    sys.path.insert(0, str(path.parent.resolve()))

    source = path.read_text(encoding="utf-8")
    namespace = {"__name__": "__main__", "__file__": str(path.resolve())}
    try:
        exec(compile(source, str(path), "exec"), namespace)  # noqa: S102
    except KeyboardInterrupt:
        _warn("Stopped.")
        return 130
    return 0


# ---------------------------------------------------------------------------
# diagnostics
# ---------------------------------------------------------------------------


def cmd_doctor(args: argparse.Namespace) -> int:
    _heading("Environment")

    python_version = ".".join(str(part) for part in sys.version_info[:3])
    if sys.version_info >= (3, 9):
        _ok(f"Python {python_version}")
    else:
        _fail(f"Python {python_version} — darkob needs 3.9+")

    try:
        import darkob

        _ok(f"darkob {darkob.__version__}")
    except Exception as exc:  # pragma: no cover
        _fail(f"darkob import failed: {exc}")
        return 1

    for module in ("aiohttp", "aiofiles", "Crypto", "mutagen"):
        try:
            __import__(module)
            _ok(f"{module} available")
        except Exception:
            _fail(f"{module} is missing — run: pip install darkob")

    directory = _session_dir()
    if directory.exists():
        count = len(_list_sessions())
        _ok(f"Session directory {directory} ({count} session(s))")
    else:
        _warn(f"Session directory {directory} does not exist yet")

    _heading("Sessions")
    if not _list_sessions():
        _warn("None. Run darkob login.")

    return 0


def cmd_version(args: argparse.Namespace) -> int:
    import darkob

    _print(f"darkob {darkob.__version__}")
    return 0


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="darkob",
        description="Build and run Rubika/Shad bots.",
    )
    sub = parser.add_subparsers(dest="command")

    sessions = sub.add_parser("sessions", help="List saved logins")
    sessions.set_defaults(func=cmd_sessions)

    login = sub.add_parser("login", help="Log a user account in and save it")
    login.add_argument("--session", "-s", help="Session name (default: darkob_default)")
    login.set_defaults(func=cmd_login)

    new = sub.add_parser("new", help="Scaffold a new bot project")
    new.add_argument("name", help="Directory to create")
    new.set_defaults(func=cmd_new)

    run = sub.add_parser("run", help="Run a bot file")
    run.add_argument("file", help="Path to the bot script")
    run.add_argument("arguments", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    run.set_defaults(func=cmd_run)

    doctor = sub.add_parser("doctor", help="Check the environment")
    doctor.set_defaults(func=cmd_doctor)

    version = sub.add_parser("version", help="Print the version")
    version.set_defaults(func=cmd_version)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not getattr(args, "func", None):
        parser.print_help()
        return 0

    try:
        return args.func(args)
    except KeyboardInterrupt:
        _warn("Interrupted.")
        return 130


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

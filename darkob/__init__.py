"""darkob — async Python library for the Rubika & Shad platforms.

Derived from `maxrubika <https://github.com/MEH2RAB/maxrubika>`_ by
MEHRAB Farahmand (MIT License), rebranded and hardened.

Importing this package performs **no network I/O**. The optional update
check is opt-in via :func:`check_for_updates`.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import List, Optional, Tuple

from rich.console import Console
from rich.text import Text

from .TheBot import Bot
from .TheBot import Bot as bot

from .TheClient import Client, Messenger
from .TheClient import Messenger as messenger

from .shad import Shad
from .shad import Shad as shad

from .router import Router
from .fsm import (
    FSMContext,
    JsonFileStorage,
    MemoryStorage,
    SQLiteStorage,
    TTLMemoryStorage,
    StateFilter,
    Storage,
)

from .keyboards import Button, ChatKeyboard, InlineKeyboard, Keyboard
from .builders import MessageBuilder
from .bot.models import ButtonType, ChatType, FileType
from .retry import Retry
from .circuit import CircuitBreaker
from .ratelimit import RateLimiter, TokenBucket
from .queue import QueueFull, SendQueue
from .protocol import ProtocolSnapshot, ProtocolTracker
from .formatting import (
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

__author__ = "MEHRAB Farahmand"
__maintainer__ = "Mani Keikhosravi"
__version__ = "0.12.0"

logger = logging.getLogger(__name__)

_welcome_shown = False

__all__ = [
    "Bot",
    "bot",
    "Client",
    "Messenger",
    "messenger",
    "Shad",
    "shad",
    "show_welcome_message",
    "check_for_updates",
    "Router",
    "FSMContext",
    "Storage",
    "MemoryStorage",
    "TTLMemoryStorage",
    "SQLiteStorage",
    "JsonFileStorage",
    "StateFilter",
    "Keyboard",
    "InlineKeyboard",
    "ChatKeyboard",
    "Button",
    "MessageBuilder",
    "ButtonType",
    "ChatType",
    "FileType",
    "Retry",
    "CircuitBreaker",
    "RateLimiter",
    "TokenBucket",
    "SendQueue",
    "QueueFull",
    "ProtocolTracker",
    "ProtocolSnapshot",
    "bold",
    "italic",
    "strike",
    "underline",
    "spoiler",
    "code",
    "pre",
    "link",
    "join",
    "__version__",
]


def show_welcome_message(show_welcome: bool = True) -> None:
    """Print the one-time welcome banner.

    This never performs network I/O. The banner is shown at most once per
    process unless ``show_welcome`` is false.
    """
    global _welcome_shown

    if not show_welcome or _welcome_shown:
        return

    _welcome_shown = True

    console = Console()
    text = Text()
    text.append(
        "Welcome to darkob — async library for Rubika & Shad",
        style="bold magenta",
    )
    text.append(
        f"\nCopyright © {datetime.now().year} darkob contributors "
        "- All rights reserved.",
        style="cyan",
    )
    text.append("\nGithub: ", style="white")
    text.append(
        "https://github.com/ManiTheFerfri/darkob", style="green underline"
    )
    text.append("\nDocument: ", style="white")
    text.append(
        "https://ManiTheFerfri.github.io/darkob\n", style="yellow underline"
    )
    console.print(text)


def _parse_version(value: str) -> Tuple[int, ...]:
    """Parse a version string into a comparable tuple.

    Tolerates pre-release and non-numeric suffixes, e.g. ``"1.2.0rc1"``
    becomes ``(1, 2, 1)`` rather than raising.
    """
    parts: List[int] = []
    for chunk in value.split("."):
        digits = "".join(ch for ch in chunk if ch.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def check_for_updates(
    current_version: Optional[str] = None, *, timeout: float = 2.0
) -> Optional[str]:
    """Compare the installed version against the latest release on PyPI.

    This is **opt-in** and is never called automatically. Call it yourself
    if you want an update notice::

        import darkob
        darkob.check_for_updates()

    Args:
        current_version: Version to compare against; defaults to
            :data:`__version__`.
        timeout: Network timeout in seconds.

    Returns:
        The latest version string when an update is available, otherwise
        ``None``. Never raises on network or parsing failures.
    """
    import json
    from urllib.error import URLError
    from urllib.request import urlopen

    current_version = current_version or __version__

    try:
        with urlopen(
            "https://pypi.org/pypi/darkob/json", timeout=timeout
        ) as response:
            latest = json.loads(response.read().decode("utf-8"))["info"][
                "version"
            ]
    except (URLError, OSError, ValueError, KeyError) as exc:
        logger.debug("Update check skipped: %s", exc)
        return None

    try:
        is_newer = _parse_version(latest) > _parse_version(current_version)
    except (TypeError, ValueError):
        return None

    if not is_newer:
        return None

    console = Console(stderr=True)
    notice = Text()
    notice.append(
        f"A new version of darkob is available! "
        f"(v{current_version} → v{latest})\n",
        style="bold bright_red",
    )
    notice.append("   Run: ", style="white")
    notice.append("pip install darkob --upgrade\n", style="gold1")
    console.print(notice)

    return latest

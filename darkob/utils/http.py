"""Small HTTP helpers shared by both request paths.

darkob has two: :mod:`darkob.client.core.api` for the userbot surface and
:mod:`darkob.bot.request` for the Bot API. They were written separately and
historically drifted; anything both of them need lives here so the drift stops.
"""

from __future__ import annotations

from typing import Any, Optional

__all__ = ["retry_after_seconds"]


def retry_after_seconds(response: Any) -> Optional[float]:
    """Read a numeric ``Retry-After`` header, ignoring HTTP-date forms.

    Defensive on purpose: reading an optional header must never be the thing
    that breaks a request, and duck-typed test doubles may not carry headers.

    Returns:
        The delay in seconds, or ``None`` when the header is absent, not a
        number, or negative. HTTP-date values are ignored rather than guessed
        at, because the server clock is not necessarily our clock.
    """
    headers = getattr(response, "headers", None)
    if not headers:
        return None
    raw = headers.get("Retry-After")
    if not raw:
        return None
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return None
    return value if value >= 0 else None

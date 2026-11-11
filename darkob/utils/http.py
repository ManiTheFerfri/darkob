"""Small HTTP helpers shared by both request paths.

darkob has two: :mod:`darkob.client.core.api` for the userbot surface and
:mod:`darkob.bot.request` for the Bot API. They were written separately and
historically drifted; anything both of them need lives here so the drift stops.
"""

from __future__ import annotations

from typing import Any, Optional
from contextlib import asynccontextmanager

__all__ = ["redact_secrets", "request_session", "retry_after_seconds"]


def redact_secrets(text: str, *values: Any) -> str:
    """Replace non-trivial credential values in a diagnostic string.

    ``aiohttp`` exception messages include a request's full URL, and the Bot
    API puts its token in that URL. A token is a credential even when nested
    in a long message, so substring matching (not URL parsing alone) is the
    conservative choice. Small values and ``None`` are ignored to avoid
    hiding every short word in an error. The original exception is never
    modified, only its log/report-safe representation.
    """
    result = str(text)
    for value in values:
        if isinstance(value, str) and len(value) >= 4:
            result = result.replace(value, "<redacted>")
    return result


@asynccontextmanager
async def request_session(owner: Any):
    """Yield ``(session, proxy)`` for one of the API wrapper objects.

    Rubino, RubiAI and RubikaTV can wrap an existing ``Messenger``. When that
    client is connected, its pooled session is reused and never closed here.
    Otherwise a short-lived session is created with the wrapper's own TLS,
    timeout and proxy settings. This keeps upstream's auth-only mode working
    without silently disabling certificate verification.
    """
    import aiohttp

    client = getattr(owner, "_client", None) or getattr(owner, "client", None)
    connection = getattr(client, "connection", None)
    session = getattr(connection, "session", None)
    proxy = getattr(owner, "proxy", None)
    if proxy is None:
        proxy = getattr(client, "proxy", None)

    if session is not None and not getattr(session, "closed", False):
        yield session, proxy
        return

    timeout = getattr(owner, "timeout", 30)
    verify_ssl = getattr(owner, "verify_ssl", True)
    session = aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=verify_ssl),
        timeout=aiohttp.ClientTimeout(total=timeout),
    )
    try:
        yield session, proxy
    finally:
        await session.close()


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

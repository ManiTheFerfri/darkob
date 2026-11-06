"""Helpers for reusing the client's pooled HTTP session."""

from contextlib import asynccontextmanager

__all__ = ["borrowed_session"]


@asynccontextmanager
async def borrowed_session(session):
    """Yield the client's pooled session without closing it.

    Auxiliary work (fetching a remote file, reading a thumb URL) used to
    open its own ``aiohttp.ClientSession``, which paid a fresh TCP and TLS
    handshake and ignored the connection pool.
    """
    yield session

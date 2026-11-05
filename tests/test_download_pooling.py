"""Guard: the Bot download path must use the pooled session."""

from __future__ import annotations

import inspect

from darkob.bot import download_file as download_module


def test_download_module_does_not_open_its_own_session():
    """A fresh ClientSession per download meant a new TLS handshake per file.

    Downloads now borrow the client's pooled session, so this file must not
    construct one itself.
    """
    source = inspect.getsource(download_module)

    assert "aiohttp.ClientSession()" not in source
    assert "_borrowed(await self._get_session())" in source

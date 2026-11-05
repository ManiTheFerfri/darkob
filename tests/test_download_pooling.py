"""Tests for the Bot download path: pooling and byte-range resume."""

from __future__ import annotations

import inspect

from darkob import Bot
from darkob.bot import download_file as download_module

from conftest import VALID_TOKEN

BLOB = bytes(range(256)) * 4  # 1024 distinguishable bytes


class FakeContent:
    def __init__(self, data: bytes):
        self._data = data

    async def iter_chunked(self, size: int):
        for start in range(0, len(self._data), size):
            yield self._data[start : start + size]


class FakeResponse:
    def __init__(self, data: bytes, status: int, headers: dict):
        self._data = data
        self.status = status
        self.headers = headers
        self.content = FakeContent(data)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False


class FakeSession:
    def __init__(self, blob: bytes):
        self.blob = blob
        self.starts = []

    def get(self, url, headers=None, proxy=None):
        headers = headers or {}
        start = 0
        if "Range" in headers:
            start = int(headers["Range"].split("=")[1].split("-")[0])
        self.starts.append(start)
        data = self.blob[start:]
        status = 206 if start else 200
        return FakeResponse(data, status, {"Content-Length": str(len(data))})


def make_bot(session: FakeSession) -> Bot:
    bot = Bot(token=VALID_TOKEN, show_welcome=False)

    async def _get_session():
        return session

    bot._get_session = _get_session
    return bot


def test_download_module_does_not_open_its_own_session():
    """A fresh ClientSession per download meant a new TLS handshake per file."""
    source = inspect.getsource(download_module)

    assert "aiohttp.ClientSession()" not in source
    assert "_borrowed(await self._get_session())" in source


async def test_download_writes_the_whole_file(tmp_path):
    session = FakeSession(BLOB)
    bot = make_bot(session)
    target = tmp_path / "file.bin"

    written = await bot._download_to_path(
        "https://example/file", str(target), resume=False
    )

    assert written == len(BLOB)
    assert target.read_bytes() == BLOB
    assert session.starts == [0], "a fresh download uses no Range header"


async def test_download_resumes_from_the_existing_size(tmp_path):
    target = tmp_path / "partial.bin"
    target.write_bytes(BLOB[:400])

    session = FakeSession(BLOB)
    bot = make_bot(session)

    written = await bot._download_to_path("https://example/file", str(target))

    assert written == len(BLOB)
    assert target.read_bytes() == BLOB
    assert session.starts == [400], "only the missing tail is requested"


async def test_resume_can_be_disabled(tmp_path):
    target = tmp_path / "file.bin"
    target.write_bytes(b"stale")

    session = FakeSession(BLOB)
    bot = make_bot(session)

    await bot._download_to_path("https://example/file", str(target), resume=False)

    assert target.read_bytes() == BLOB
    assert session.starts == [0]


async def test_progress_callback_reports_bytes(tmp_path):
    session = FakeSession(BLOB)
    bot = make_bot(session)
    seen = []

    await bot._download_to_path(
        "https://example/file",
        str(tmp_path / "f.bin"),
        resume=False,
        callback=lambda done, total, percent: seen.append((done, total)),
    )

    assert seen, "progress should be reported"
    assert seen[-1][0] == len(BLOB)


async def test_already_complete_file_is_not_refetched(tmp_path):
    target = tmp_path / "done.bin"
    target.write_bytes(BLOB)

    class RangeRejecting(FakeSession):
        def get(self, url, headers=None, proxy=None):
            self.starts.append(-1)
            return FakeResponse(b"", 416, {})

    session = RangeRejecting(BLOB)
    bot = make_bot(session)

    written = await bot._download_to_path("https://example/file", str(target))

    assert written == len(BLOB)
    assert target.read_bytes() == BLOB


async def test_server_ignoring_range_does_not_corrupt_the_file(tmp_path):
    """A 200 response to a ranged request means the whole body was resent."""
    target = tmp_path / "partial.bin"
    target.write_bytes(BLOB[:400])

    class IgnoresRange(FakeSession):
        def get(self, url, headers=None, proxy=None):
            self.starts.append(0)
            return FakeResponse(self.blob, 200, {"Content-Length": str(len(self.blob))})

    bot = make_bot(IgnoresRange(BLOB))

    written = await bot._download_to_path("https://example/file", str(target))

    assert written == len(BLOB)
    assert target.read_bytes() == BLOB, "must restart, not append the whole body"

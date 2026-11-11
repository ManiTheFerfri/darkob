"""Offline regression tests for client transfer integrity and retry budgets."""

import logging
import shutil
import tempfile
from contextlib import asynccontextmanager
from pathlib import Path

import pytest

from darkob.client.base.download_file import DownloadFile
from darkob.client.base.upload_file import UploadFile
from darkob.client.exceptions import NetworkError, ServerError


class FakeResponse:
    def __init__(self, status=200, body=b"", payload=None):
        self.status = status
        self._body = body
        self._payload = payload

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        return False

    async def read(self):
        return self._body

    async def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status >= 400:
            raise ServerError(f"HTTP {self.status}")


class FakeDownloadSession:
    def __init__(self, data, failing_start=None, malformed=None):
        self.data = data
        self.failing_start = failing_start
        self.malformed = malformed or {}
        self.calls = []

    def post(self, url, headers=None, proxy=None):
        start = int(headers["start-index"])
        end = int(headers["last-index"])
        self.calls.append((start, end))
        if start == self.failing_start:
            return FakeResponse(status=500)
        body = self.malformed.get(start, self.data[start : end + 1])
        return FakeResponse(status=200, body=body)


class FakeUploadSession:
    def __init__(self):
        self.get_calls = 0
        self.post_calls = 0

    def get(self, url, timeout=None):
        self.get_calls += 1
        return FakeResponse(body=b"remote bytes")

    def post(self, url=None, **kwargs):
        self.post_calls += 1
        return FakeResponse(status=500)


class FakeConnection:
    def __init__(self, session):
        self.session = session

    @asynccontextmanager
    async def aux_session(self, base_url, verify_ssl):
        yield self.session


class DownloadClient(DownloadFile):
    def __init__(self, session, max_retries=2):
        self.connection = FakeConnection(session)
        self.max_retries = max_retries
        self.auth = "auth"
        self.user_agent = "tests"
        self._original_platform = "rubika"
        self.proxy = None
        self.verify_ssl = True
        self.logger = logging.getLogger("tests.download")


class UploadClient(UploadFile):
    def __init__(self, session, max_retries=0):
        self.connection = FakeConnection(session)
        self.max_retries = max_retries
        self.auth = "auth"
        self.proxy = None
        self.logger = logging.getLogger("tests.upload")

    async def request_send_file(self, file_name, file_size, mime):
        return {
            "id": "upload-id",
            "dc_id": 2,
            "upload_url": "https://upload.invalid/",
            "access_hash_send": "send-hash",
        }


async def download_in_mode(client, mode, directory=None, **overrides):
    kwargs = {
        "dc_id": 1,
        "file_id": 10,
        "access_hash": "hash",
        "size": 5,
        "chunk": 2,
    }
    if mode == "gather":
        kwargs["gather"] = True
    elif mode == "save_as":
        kwargs.update(save_as=directory, file_name="result.bin")
    kwargs.update(overrides)
    return await client.download_file(**kwargs)


@pytest.mark.parametrize("mode", ["bytes", "save_as", "gather"])
async def test_mid_chunk_server_error_raises_after_retry_budget(mode):
    session = FakeDownloadSession(b"abcde", failing_start=2)
    client = DownloadClient(session, max_retries=2)
    directory = tempfile.mkdtemp() if mode == "save_as" else None
    try:
        with pytest.raises(NetworkError):
            await download_in_mode(client, mode, directory)
        assert session.calls.count((2, 3)) == 2
        if directory is not None:
            assert (Path(directory) / "result.bin").read_bytes() == b"ab"
    finally:
        if directory is not None:
            shutil.rmtree(directory)


@pytest.mark.parametrize("mode", ["bytes", "save_as", "gather"])
@pytest.mark.parametrize("bad_body", [b"c", b"cdEXTRA"], ids=["short", "long"])
async def test_range_response_with_wrong_length_raises(mode, bad_body):
    session = FakeDownloadSession(b"abcde", malformed={2: bad_body})
    client = DownloadClient(session)
    directory = tempfile.mkdtemp() if mode == "save_as" else None
    try:
        with pytest.raises(NetworkError):
            await download_in_mode(client, mode, directory)
        if directory is not None:
            assert (Path(directory) / "result.bin").read_bytes() == b"ab"
    finally:
        if directory is not None:
            shutil.rmtree(directory)


@pytest.mark.parametrize("mode", ["bytes", "gather", "save_as"])
async def test_zero_byte_download_is_valid(mode):
    session = FakeDownloadSession(b"")
    client = DownloadClient(session)
    directory = tempfile.mkdtemp() if mode == "save_as" else None
    try:
        kwargs = {"size": 0}
        result = await download_in_mode(client, mode, directory, **kwargs)
        if mode == "save_as":
            assert result.status == "OK"
            assert (Path(directory) / "result.bin").read_bytes() == b""
        else:
            assert result == b""
        assert session.calls == []
    finally:
        if directory is not None:
            shutil.rmtree(directory)


async def test_upload_zero_retries_uses_borrowed_get_and_one_post():
    session = FakeUploadSession()
    client = UploadClient(session, max_retries=0)

    with pytest.raises(ServerError):
        await client.upload_file(file="https://files.invalid/source.bin")

    assert session.get_calls == 1
    assert session.post_calls == 1

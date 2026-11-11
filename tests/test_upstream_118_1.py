"""Regressions for maxrubika v1.18.1's media, download and retry fixes."""

from __future__ import annotations

import inspect
import shutil
import tempfile
from pathlib import Path
from types import SimpleNamespace

import aiohttp
import pytest

from darkob.client.messages.send.send_file import SendFile
from darkob.client.messages.send.send_gif import SendGif
from darkob.client.messages.send.send_image import SendImage
from darkob.client.messages.send.send_music import SendMusic
from darkob.client.messages.send.send_video import SendVideo
from darkob.client.messages.send.send_video_message import SendVideoMessage
from darkob.client.messages.send.send_voice import SendVoice
from darkob.rubiai.download_image import DownloadImage
from darkob.rubiai.exceptions import InvalidInput as AIInvalidInput
from test_upstream_118_surfaces import (
    RecordingPostSession,
    RecordingResponse,
    install_owner_session,
    make_offline_rubino,
    transparent_rubino_crypto,
)


@pytest.mark.parametrize(
    "class_, data",
    [
        (SendFile, "file"),
        (SendGif, "gif"),
        (SendImage, "image"),
        (SendMusic, "music"),
        (SendVideo, "video"),
        (SendVideoMessage, "video_message"),
        (SendVoice, "voice"),
    ],
)
def test_file_inline_remains_after_legacy_keyword_options(class_, data):
    # Wrappers are named after their media except SendFile itself.
    method = "send_file" if class_ is SendFile else next(
        name for name in class_.__dict__ if name.startswith("send_")
    )
    signature = inspect.signature(class_.__dict__[method])
    parameters = list(signature.parameters)
    assert parameters[-2:] == ["file_inline", "kwargs"]
    assert data in parameters[1:5]


class SendFileStub(SendFile):
    def __init__(self):
        self.guid = "u0self"
        self.as_dict = True
        self.user_agent = "test"
        self.calls = []

    async def get_guid(self, target):
        return target

    async def upload_file(self, **kwargs):
        self.calls.append(("upload", kwargs))
        return {}

    async def request(self, *, method, input):
        self.calls.append(("request", method, input))
        return input


@pytest.mark.parametrize("encoded", ["aGVsbG8=", "aGVs\nbG8="])
async def test_base64_parameter_does_not_shadow_the_base64_module(encoded):
    stub = SendFileStub()

    result = await stub.send_file(
        "u0recipient", base64=encoded, file_name="hello.txt"
    )

    upload = stub.calls[0][1]
    assert upload["file"] == b"hello"
    assert result["file_inline"]["type"] == "File"


async def test_missing_local_file_is_rejected_before_upload():
    stub = SendFileStub()

    with pytest.raises(FileNotFoundError):
        await stub.send_file("u0recipient", file="definitely-absent.mp4")

    assert stub.calls == []


async def test_invalid_base64_reports_the_public_error_not_leaked_decode_value():
    from darkob.client.exceptions import InvalidInput

    stub = SendFileStub()

    with pytest.raises(InvalidInput, match="Invalid base64 data"):
        await stub.send_file("u0recipient", base64="%%%not-base64%%%")


async def test_rubiai_server_error_retries_then_succeeds(monkeypatch):
    from darkob.rubiai.request import Request

    class StatusResponse:
        def __init__(self, status):
            self.status = status

        async def __aenter__(self):
            raise aiohttp.ClientResponseError(
                SimpleNamespace(real_url="https://rubiai.test/"),
                (),
                status=self.status,
            )

        async def __aexit__(self, *exc_info):
            return False

    class AIStub(Request):
        max_retries = 3

        def __init__(self):
            import logging
            self.logger = logging.getLogger("darkob.tests.rubiai1181")
            self.auth = "auth"
            self.client_info = {}
            self.base_url = "https://rubiai.test/"
            self.timeout = 1
            self.as_dict = True
            self.proxy = None

    session = RecordingPostSession(
        StatusResponse(503),
        RecordingResponse({"data": {"status": "OK", "output": {"answer": 42}}}),
    )
    install_owner_session(monkeypatch, session)

    assert await AIStub().request("getMe") == {"answer": 42}
    assert len(session.posts) == 2


async def test_rubiai_client_400_is_not_retried(monkeypatch):
    from darkob.rubiai.request import Request

    class BadRequest:
        async def __aenter__(self):
            raise aiohttp.ClientResponseError(
                SimpleNamespace(real_url="https://rubiai.test/"),
                (),
                status=400,
            )

        async def __aexit__(self, *exc_info):
            return False

    class AIStub(Request):
        max_retries = 3

        def __init__(self):
            import logging
            self.logger = logging.getLogger("darkob.tests.rubiai1181")
            self.auth = "auth"
            self.client_info = {}
            self.base_url = "https://rubiai.test/"
            self.timeout = 1
            self.as_dict = True
            self.proxy = None

    session = RecordingPostSession(BadRequest())
    install_owner_session(monkeypatch, session)

    with pytest.raises(aiohttp.ClientResponseError) as info:
        await AIStub().request("getMe")

    assert info.value.status == 400
    assert len(session.posts) == 1


async def test_rubino_transport_errors_use_global_retry_budget(monkeypatch):
    rubino = make_offline_rubino()
    transparent_rubino_crypto(monkeypatch)

    class TransportFailure:
        async def __aenter__(self):
            raise aiohttp.ClientConnectionError("could not connect")

        async def __aexit__(self, *exc_info):
            return False

    session = RecordingPostSession(
        TransportFailure(), TransportFailure(), TransportFailure()
    )
    install_owner_session(monkeypatch, session)

    from darkob.rubino.exceptions import NetworkError

    with pytest.raises(NetworkError, match="3 attempt"):
        await rubino.request("testMethod")

    assert len(session.posts) == 3


async def test_rubino_api_errors_do_not_retry_even_when_message_mentions_network(monkeypatch):
    from darkob.rubino.exceptions import InvalidInput

    class InvalidPayload(InvalidInput):
        def __str__(self):
            return "network unreachable"

    rubino = make_offline_rubino()
    transparent_rubino_crypto(monkeypatch)
    rubino_exceptions = __import__(
        "importlib"
    ).import_module("darkob.rubino.exceptions")

    def invalid_input(*args):
        raise InvalidPayload("network unreachable")

    monkeypatch.setattr(rubino_exceptions, "raise_exception", invalid_input)
    session = RecordingPostSession(
        RecordingResponse({"status": "ERROR", "status_det": "INVALID_INPUT"})
    )
    install_owner_session(monkeypatch, session)

    with pytest.raises(InvalidPayload):
        await rubino.request("testMethod")

    assert len(session.posts) == 1


async def test_generated_image_saves_to_a_pathlib_path():
    import base64

    directory = tempfile.mkdtemp(prefix="darkob-ai-image-")
    try:
        destination = Path(directory) / "image.jpg"
        owner = DownloadImage()
        owner.request = _image_request({
            "image": base64.b64encode(b"JPEG").decode()
        })

        result = await owner.download_image(
            "task-1", save_as=destination, interval=1
        )

        assert result.status == "Success"
        assert destination.read_bytes() == b"JPEG"
    finally:
        shutil.rmtree(directory, ignore_errors=True)


def _image_request(payload):
    async def request(*, method, input):
        return {"status": "Success", **payload}

    return request


async def test_missing_generated_image_payload_raises_not_a_type_error():
    from darkob.data import Data

    async def request(*, method, input):
        return Data({"status": "Success"})

    owner = DownloadImage()
    owner.request = request

    with pytest.raises(AIInvalidInput, match="Image data is missing"):
        await owner.download_image(
            "task-1", save_as=Path("not-written.jpg"), interval=1
        )

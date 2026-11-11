"""Regressions introduced by merging upstream v1.18's new endpoint shapes."""

from __future__ import annotations

import inspect

from darkob.client.chats.information.get_chat_ads import GetChatAds
from darkob.client.messages.fetch.get_chat_messages import GetChatMessages
from darkob.client.messages.send.send_message import SendMessage
from darkob.data import Data


class SendingStub(SendMessage):
    def __init__(self):
        self.calls = []
        self.guid = "u0self"
        self.user_agent = "test"
        self.max_retries = 1

    async def _send_text_message(self, **kwargs):
        self.calls.append(("text", kwargs))
        return kwargs

    async def send_file(self, **kwargs):
        self.calls.append(("file", kwargs))
        return kwargs

    async def get_guid(self, target):
        self.calls.append(("guid", target))
        return target

    async def request(self, *, method, input):
        self.calls.append(("request", method, input))
        return input


def test_send_message_keeps_its_pre_118_positional_layout():
    signature = inspect.signature(SendingStub.send_message)
    names = list(signature.parameters)[1:9]

    assert names == [
        "chat",
        "text",
        "reply_to_message_id",
        "via_bot",
        "file_inline",
        "base64_data",
        "sticker",
        "type",
    ]


async def test_text_and_file_calls_stay_separate():
    stub = SendingStub()

    await stub.send_message("u0user", "hello", metadata={"bold": True})
    await stub.send_message(
        "u0user", "caption", base64_data="YWJj", file_name="a.bin"
    )

    assert stub.calls[0][0] == "text"
    assert stub.calls[0][1]["metadata"] == {"bold": True}
    assert stub.calls[1][0] == "file"
    assert stub.calls[1][1]["base64"] == "YWJj"
    assert stub.calls[1][1]["file_name"] == "a.bin"
    assert stub.calls[1][1]["text"] == "caption"


async def test_pre_uploaded_inline_data_is_forwarded_not_silently_dropped():
    stub = SendingStub()
    inline = Data({"file_id": "123", "type": "File"})

    await stub.send_message("u0user", file_inline=inline)

    kind, payload = stub.calls[-1]
    assert kind == "file"
    assert payload["file_inline"] is inline
    assert payload["file"] is None


async def test_raw_sticker_payload_keeps_every_field():
    stub = SendingStub()
    sticker = {
        "emoji_character": "🙂",
        "sticker_id": "42",
        "sticker_set_id": "set",
        "file": {"file_id": "file-id"},
    }

    await stub.send_message("u0user", sticker=sticker, is_mute=True)

    call = stub.calls[-1]
    assert call[0] == "request"
    assert call[1] == "sendMessage"
    assert call[2]["sticker"] is sticker
    assert call[2]["is_mute"] is True


class MessagesStub(GetChatMessages):
    def __init__(self):
        self.requests = []
        self.as_dict = True

    async def get_guid(self, chat):
        return chat

    async def request(self, *, method, input):
        self.requests.append(input.copy())
        return Data({
            "messages": [],
            "has_continue": False,
        })


async def test_second_positional_max_id_still_means_max_id():
    stub = MessagesStub()

    result = await stub.get_chat_messages(
        "u0chat", "170", "FromMax", "File", 20
    )

    assert result["count"] == 0
    assert stub.requests[0]["max_id"] == "170"
    assert stub.requests[0]["sort"] == "FromMax"
    assert stub.requests[0]["filter_type"] == "File"


async def test_upstream_positional_direction_is_also_accepted():
    stub = MessagesStub()

    await stub.get_chat_messages("u0chat", "FromMax")

    assert "max_id" not in stub.requests[0]
    assert stub.requests[0]["sort"] == "FromMax"


async def test_folder_id_was_not_dropped():
    from darkob.client.settings.folders.add_folder import AddFolder

    class FolderStub(AddFolder):
        def __init__(self):
            self.payload = None

        async def get_guid(self, chat):
            return chat

        async def request(self, *, method, input):
            self.payload = input

    stub = FolderStub()
    await stub.add_folder(
        "work", include_chats=["u0person"],
        suggestion_folder_id="suggested", folder_id="folder",
    )

    assert stub.payload["folder_id"] == "folder"
    assert "folder_id" in stub.payload["updated_parameters"]


async def test_chat_ads_timestamp_is_evaluated_per_call(monkeypatch):
    import darkob.client.chats.information.get_chat_ads as module

    states = [2000, 2500]
    monkeypatch.setattr(module, "time", lambda: states.pop(0))
    seen = []

    class Stub(GetChatAds):
        async def request(self, *, method, input):
            seen.append(input["state"])

    await Stub().get_chat_ads()
    await Stub().get_chat_ads()

    assert seen == [1850, 2350]


async def test_missing_exceptions_import_in_upload_validation():
    import pytest
    from darkob.client.base.upload_file import UploadFile
    from darkob.client.exceptions import InvalidInput

    with pytest.raises(InvalidInput, match="not both"):
        await UploadFile().upload_file(file=b"x", base64_data="eA==")


async def test_channel_html_uses_pooled_session_and_real_timeout():
    from darkob.client.channels.get_channel_post_by_link import GetChannelPostByLink
    from types import SimpleNamespace

    class FakeResponse:
        status = 200
        text_value = "x" * 200

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc_info):
            return False

        async def text(self, encoding=None):
            return self.text_value

    class FakeConnection:
        def __init__(self):
            self.session = SimpleNamespace(closed=False)
            self.kwargs = None

            def get(url, **kwargs):
                self.kwargs = kwargs
                return FakeResponse()

            self.session.get = get

    connection = FakeConnection()

    receiver = GetChannelPostByLink()
    receiver.connection = connection
    receiver.proxy = "http://proxy.test"
    result = await receiver._fetch_html("https://go.rubika.ir/post")

    assert result is not None
    assert connection.kwargs["proxy"] == "http://proxy.test"
    assert connection.kwargs["timeout"].total == 30

"""Offline compatibility tests for pre-1.18 and upstream live/voice calls."""

import asyncio
import inspect

import pytest

from darkob.client.chats.voice_chat import VoiceChat
from darkob.client.exceptions import VoiceChatNotActive
from darkob.client.extras.add_live_comment import AddLiveComment
from darkob.client.extras.get_live_play_url import GetLivePlayUrl


CHAT = "g0" + "a" * 30
USER = "u0" + "b" * 30
PARTICIPANT = "u0" + "c" * 30
SELF = "u0" + "d" * 30
VOICE_CHAT_ID = "voice-chat-from-chat-info"
LIVE_ID = "123456789"
ACCESS_TOKEN = "u0" + "e" * 30


class FakeClient(AddLiveComment, GetLivePlayUrl, VoiceChat):
    def __init__(self, chat_info=None):
        self.guid = SELF
        self.calls = []
        self.info_calls = 0
        self.chat_info = (
            {"chat": {"group_voice_chat_id": VOICE_CHAT_ID}}
            if chat_info is None
            else chat_info
        )

    async def get_guid(self, value):
        return value

    async def get_chat_info(self, chat_guid):
        assert chat_guid == CHAT
        self.info_calls += 1
        return self.chat_info

    async def request(self, method, input):
        self.calls.append((method, input))
        return {"status": "OK"}

    @property
    def last_payload(self):
        assert len(self.calls) == 1
        return self.calls[0][1]


@pytest.mark.parametrize(
    "method_name,args,kwargs,method,expected",
    [
        (
            "add_live_comment",
            (ACCESS_TOKEN, LIVE_ID, "hello"),
            {},
            "addLiveComment",
            {"live_id": LIVE_ID, "access_token": ACCESS_TOKEN, "text": "hello"},
        ),
        (
            "add_live_comment",
            (LIVE_ID, "b0" + "f" * 30, "hello"),
            {},
            "addLiveComment",
            {
                "live_id": LIVE_ID,
                "access_token": "b0" + "f" * 30,
                "text": "hello",
            },
        ),
        (
            "add_live_comment",
            (),
            {"live_id": LIVE_ID, "access_token": ACCESS_TOKEN, "comment": "hello"},
            "addLiveComment",
            {"live_id": LIVE_ID, "access_token": ACCESS_TOKEN, "text": "hello"},
        ),
        (
            "get_live_play_url",
            (ACCESS_TOKEN, LIVE_ID),
            {},
            "getLivePlayUrl",
            {"live_id": LIVE_ID, "access_token": ACCESS_TOKEN},
        ),
        (
            "get_live_play_url",
            (LIVE_ID, ACCESS_TOKEN),
            {},
            "getLivePlayUrl",
            {"live_id": LIVE_ID, "access_token": ACCESS_TOKEN},
        ),
        (
            "get_live_play_url",
            (),
            {"live_id": LIVE_ID, "access_token": ACCESS_TOKEN},
            "getLivePlayUrl",
            {"live_id": LIVE_ID, "access_token": ACCESS_TOKEN},
        ),
    ],
)
async def test_live_helpers_accept_legacy_upstream_and_keyword_calls(
    method_name, args, kwargs, method, expected
):
    client = FakeClient()

    await getattr(client, method_name)(*args, **kwargs)

    assert client.calls == [(method, expected)]


async def test_ambiguous_live_positionals_keep_legacy_order_but_keywords_do_not_move():
    client = FakeClient()
    await client.get_live_play_url("opaque-token", "opaque-live")
    assert client.last_payload == {
        "live_id": "opaque-live",
        "access_token": "opaque-token",
    }

    client = FakeClient()
    await client.get_live_play_url(
        live_id="opaque-live", access_token="opaque-token"
    )
    assert client.last_payload == {
        "live_id": "opaque-live",
        "access_token": "opaque-token",
    }


@pytest.mark.parametrize(
    "method_name,args,endpoint,extra",
    [
        ("discard_voice_chat", (CHAT,), "discardGroupVoiceChat", {}),
        ("get_chat_voice_chat", (CHAT,), "getGroupVoiceChat", {}),
        ("leave_voice_chat", (CHAT,), "leaveGroupVoiceChat", {}),
        (
            "check_voice_chat_participants",
            (CHAT, USER),
            "getGroupVoiceChatParticipantsByObjectGuids",
            {"object_guids": [USER]},
        ),
        (
            "invite_to_voice_chat",
            (CHAT, USER),
            "inviteToGroupVoiceChat",
            {"invite_object_guid": USER},
        ),
        (
            "join_voice_chat",
            (CHAT, "legacy-sdp"),
            "joinGroupVoiceChat",
            {"sdp_offer_data": "legacy-sdp", "self_object_guid": SELF},
        ),
        (
            "set_voice_chat_setting",
            (CHAT, "new title", True),
            "setGroupVoiceChatSetting",
            {
                "title": "new title",
                "join_muted": True,
                "updated_parameters": ["title", "join_muted"],
            },
        ),
        (
            "send_voice_chat_activity",
            (CHAT, "Speaking", PARTICIPANT),
            "sendGroupVoiceChatActivity",
            {"activity": "Speaking", "participant_object_guid": PARTICIPANT},
        ),
        (
            "set_voice_chat_state",
            (CHAT, "Mute", PARTICIPANT),
            "setGroupVoiceChatState",
            {"action": "Mute", "participant_object_guid": PARTICIPANT},
        ),
    ],
)
async def test_legacy_voice_calls_resolve_the_current_voice_chat_id(
    method_name, args, endpoint, extra
):
    client = FakeClient()

    await getattr(client, method_name)(*args)

    expected = {"chat_guid": CHAT, "voice_chat_id": VOICE_CHAT_ID, **extra}
    if endpoint == "setGroupVoiceChatSetting":
        expected = {
            "chat_guid": CHAT,
            "voice_chat_id": VOICE_CHAT_ID,
            "updated_parameters": extra.pop("updated_parameters"),
            **extra,
        }
    assert client.calls == [(endpoint, expected)]
    assert client.info_calls == 1


async def test_legacy_second_positional_update_state_is_not_a_voice_chat_id():
    client = FakeClient()

    await client.get_voice_chat_updates(CHAT, 12345)

    assert client.calls == [
        (
            "getGroupVoiceChatUpdates",
            {"chat_guid": CHAT, "voice_chat_id": VOICE_CHAT_ID, "state": 12345},
        )
    ]


async def test_upstream_update_kwargs_and_explicit_id_are_forwarded():
    client = FakeClient()

    await client.get_voice_chat_updates(
        CHAT, state="next-state", voice_chat_id="explicit-voice-chat"
    )

    assert client.last_payload == {
        "chat_guid": CHAT,
        "voice_chat_id": "explicit-voice-chat",
        "state": "next-state",
    }
    assert client.info_calls == 0


async def test_activity_preserves_legacy_participant_and_accepts_upstream_id():
    client = FakeClient()

    await client.send_voice_chat_activity(
        CHAT,
        activity="speaking",
        participant_chat_guid=PARTICIPANT,
        voice_chat_id="explicit-voice-chat",
    )

    assert client.last_payload == {
        "chat_guid": CHAT,
        "voice_chat_id": "explicit-voice-chat",
        "activity": "Speaking",
        "participant_object_guid": PARTICIPANT,
    }
    assert client.info_calls == 0


async def test_participant_pagination_kwargs_remain_available():
    client = FakeClient()

    await client.get_voice_chat_participants(
        CHAT,
        True,
        all_pages=False,
        start_id="cursor",
        voice_chat_id="explicit-voice-chat",
    )

    assert client.last_payload == {
        "chat_guid": CHAT,
        "voice_chat_id": "explicit-voice-chat",
        "start_id": "cursor",
    }
    assert client.info_calls == 0


@pytest.mark.parametrize(
    "method_name",
    [
        "check_voice_chat_participants",
        "discard_voice_chat",
        "get_chat_voice_chat",
        "get_voice_chat_participants",
        "get_voice_chat_updates",
        "invite_to_voice_chat",
        "join_voice_chat",
        "leave_voice_chat",
        "send_voice_chat_activity",
        "set_voice_chat_setting",
        "set_voice_chat_state",
        "heartbeat",
        "speaking",
    ],
)
def test_voice_chat_id_is_optional(method_name):
    parameter = inspect.signature(getattr(VoiceChat, method_name)).parameters[
        "voice_chat_id"
    ]
    assert parameter.default is not inspect.Parameter.empty


async def test_heartbeat_and_speaking_accept_only_chat_guid():
    class LoopFake(FakeClient):
        def __init__(self):
            super().__init__()
            self.loop_calls = []

        async def get_voice_chat_updates(self, chat_guid, voice_chat_id=None):
            self.loop_calls.append(("heartbeat", chat_guid, voice_chat_id))
            raise asyncio.CancelledError

        async def send_voice_chat_activity(self, chat_guid, voice_chat_id=None):
            self.loop_calls.append(("speaking", chat_guid, voice_chat_id))
            raise asyncio.CancelledError

    client = LoopFake()
    await client.heartbeat(CHAT)
    await client.speaking(CHAT)

    assert client.loop_calls == [
        ("heartbeat", CHAT, None),
        ("speaking", CHAT, None),
    ]


async def test_missing_voice_chat_id_is_never_invented():
    client = FakeClient(chat_info={"chat": {}})

    with pytest.raises(VoiceChatNotActive):
        await client.get_chat_voice_chat(CHAT)

    assert client.calls == []

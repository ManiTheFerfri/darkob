"""Regression tests for the project-wide engineering/security review."""

from __future__ import annotations

import json
import logging
import shutil
import tempfile
from types import SimpleNamespace

import pytest

from darkob import Bot
from darkob.client.base.connect import Connect
from darkob.client.base.get_updates import GetUpdates
from darkob.client.core.api import Api
from darkob.client.core.session import StringSession
from darkob.client.exceptions import SessionError
from darkob.data import Data
from darkob.hybrid import async_to_sync

from conftest import VALID_TOKEN, attach


def client_for(*, stop=True, handlers=None):
    return SimpleNamespace(
        DEFAULT_PLATFORM={"platform": "PWA"},
        _original_platform="pwa",
        user_agent="test",
        max_retries=1,
        timeout=1,
        verify_ssl=True,
        proxy=None,
        stop_on_first_match=stop,
        handlers={} if handlers is None else handlers,
        plugin_manager=None,
        _conversations=None,
    )


async def test_connect_never_logs_session_credentials(caplog):
    stored = SimpleNamespace(
        information=lambda: (
            "+1000000",
            "TEST-AUTH-DO-NOT-LOG",
            "u0fake",
            "agent",
            "TEST-PRIVATE-KEY-DO-NOT-LOG",
        )
    )
    caplog.set_level(logging.DEBUG)
    client = client_for()
    client.session = stored
    client.logger = logging.getLogger("darkob.tests.session-privacy")

    connector = Connect()
    for name, value in vars(client).items():
        setattr(connector, name, value)
    await connector.connect()
    await connector.connection.close()

    assert "TEST-AUTH-DO-NOT-LOG" not in caplog.text
    assert "TEST-PRIVATE-KEY-DO-NOT-LOG" not in caplog.text
    assert isinstance(connector.connection, Api)


async def test_bot_error_paths_redact_token_in_logs_and_plugins(caplog):
    bot = Bot(token=VALID_TOKEN, show_welcome=False, max_retries=1)
    payload = RuntimeError(f"request URL was {bot.base_url}/getMe")
    attach(bot, payload)
    reports = []

    async def on_error(error, context):
        reports.append((str(error), context))

    async def passthrough_before(action, data):
        return data

    async def passthrough_after(action, data):
        return data

    bot.plugin_manager = SimpleNamespace(
        active=1,
        run_on_error=on_error,
        apply_before_request=passthrough_before,
        apply_after_response=passthrough_after,
    )
    caplog.set_level(logging.WARNING)

    try:
        with pytest.raises(Exception):
            await bot.request("POST", "getMe", json={})
    finally:
        await bot.close()

    assert VALID_TOKEN not in caplog.text
    assert reports
    error, context = reports[0]
    assert VALID_TOKEN not in error
    assert VALID_TOKEN not in json.dumps(context)
    assert "<redacted>" in error or "<redacted>" in context["endpoint"]


async def test_redacted_throttle_preserves_exception_type_and_status():
    from darkob.bot.exceptions import TooRequests

    bot = Bot(token=VALID_TOKEN, show_welcome=False, max_retries=1)
    reports = []

    async def run_on_error(error, context):
        reports.append((error, context))

    async def before(action, data):
        return data

    async def after(action, data):
        return data

    bot.plugin_manager = SimpleNamespace(
        active=1,
        run_on_error=run_on_error,
        apply_before_request=before,
        apply_after_response=after,
    )
    replaced_path = f"{bot.base_url}/getMe"
    from conftest import FakeResponse

    attach(bot, FakeResponse(429, text=replaced_path))

    try:
        with pytest.raises(TooRequests) as info:
            await bot.request("POST", "getMe", json=replaced_path)
    finally:
        await bot.close()

    assert info.value.status == "TOO_REQUESTS"
    assert VALID_TOKEN not in str(info.value)
    error, context = reports[0]
    assert isinstance(error, TooRequests)
    assert error.status == "TOO_REQUESTS"
    assert VALID_TOKEN not in error.dev_message
    assert "getMe" in context["action"]


async def test_early_exit_does_not_scan_remaining_handlers():
    evaluated = []

    class Matching:
        __name__ = "MessageUpdates"

        async def __call__(self, *, event):
            evaluated.append(1)
            return True

    async def first(event):
        return None

    handlers = {}
    for _ in range(500):
        async def unique_handler(event):
            return None

        handlers[unique_handler] = Matching()

    client = client_for(handlers=handlers)
    api = Api(client)
    try:
        for _ in range(20):
            await api.handle_update("message_updates", {})
    finally:
        await api.close()

    # One matching filter per update, not 500 * 20 evaluations.
    assert len(evaluated) == 20


async def test_replacing_a_handler_without_changing_len_invalidates_it():
    class Match:
        __name__ = "MessageUpdates"

        def __init__(self, value):
            self.value = value

        async def __call__(self, *, event):
            return self.value

    async def receiver(event):
        return None

    first, second = Match(True), Match(False)
    client = client_for(handlers={receiver: first})
    api = Api(client)
    try:
        assert (await api._handlers_for("MessageUpdates")[0][1](event={})) is True

        # The dict retains identity and size; only the filter object changed.
        client.handlers[receiver] = second

        assert (await api._handlers_for("MessageUpdates")[0][1](event={})) is False
    finally:
        await api.close()


async def test_stop_on_first_match_does_not_continue_after_failure():
    seen = []

    async def first(event):
        seen.append("first")
        raise ValueError("handler failed")

    async def second(event):
        seen.append("second")

    class Match:
        __name__ = "MessageUpdates"

        async def __call__(self, *, event):
            return True

    client = client_for(handlers={first: Match(), second: Match()})
    api = Api(client)
    try:
        await api.handle_update("message_updates", {})
    finally:
        await api.close()

    assert seen == ["first"]


async def test_recovery_dispatches_only_new_updates_and_advances_cursor():
    class Recovery(GetUpdates):
        def __init__(self, payload):
            self.payload = payload
            self.received = []
            self.states = []
            self.logger = logging.getLogger("darkob.tests.recovery")
            self.connection = SimpleNamespace(handle_update=self.receive)

        async def receive(self, name, payload):
            self.received.append((name, payload))

        async def get_chats_updates(self, state=None):
            self.states.append(state)
            return self.payload(state)

    first = {"message_id": "A", "time": 100}
    second = {"message_id": "B", "time": 101}
    payload = lambda _state: Data({"message_updates": [first, second]})
    recovery = Recovery(payload)
    name = "message_updates"

    # A is observed just before the outage and must not replay on recovery.
    await recovery._dispatch_if_new(name, first)
    assert await recovery._recover_chats_updates() == 1
    assert await recovery._recover_chats_updates() == 0

    assert [payload["message_id"] for _, payload in recovery.received] == ["A", "B"]
    assert recovery.states[-1] == 101


def test_slotted_instances_can_be_wrapped_individually(monkeypatch):
    import darkob.hybrid as hybrid

    class Slotted:
        __slots__ = ()

        async def double(self, number):
            return number * 2

    # test_hybrid deliberately terminates the process-global worker. Give this
    # independent test its own loop; close() remains an intentional terminal
    # state for that worker rather than an implicit restart operation.
    worker = hybrid.SyncLoop("test-slotted-worker")
    monkeypatch.setattr(hybrid, "_sync_loop", worker)
    try:
        instance = Slotted()
        async_to_sync(instance, "double")

        assert instance.double(12) == 24
    finally:
        worker.close()


async def test_queue_persists_permanent_error_removal():
    directory = tempfile.mkdtemp(prefix="darkob-queue-")
    path = directory + "/outbox.json"
    try:
        class AlwaysOffline:
            async def send_message(self, **kwargs):
                raise OSError("offline")

        from darkob import SendQueue

        queue = SendQueue(AlwaysOffline(), path=path)
        await queue.put("chat", "message")
        assert queue.pending == 1

        class BadMessage:
            async def send_message(self, **kwargs):
                raise ValueError("permanent failure")

        queue.bot = BadMessage()
        assert await queue.flush() == 0
        assert SendQueue(AlwaysOffline(), path=path).pending == 0
    finally:
        shutil.rmtree(directory, ignore_errors=True)


async def test_incomplete_string_session_errors_before_use():
    valid = StringSession.from_data({"auth": "a" * 32})
    encoded = str(valid)

    from darkob.client.core.session import Session

    loaded = Session(string_session=encoded)
    assert loaded.information()[4] is None
    assert loaded.information()[1] == "a" * 32

    from darkob import Messenger
    with pytest.raises(SessionError, match="API v6"):
        Messenger(string_session=encoded, show_welcome=False)


def test_string_session_without_auth_is_rejected():
    from darkob.client.core.session import Session

    incomplete = StringSession.from_data({"phone": "+100000000"})

    with pytest.raises(ValueError, match="incomplete"):
        Session(string_session=str(incomplete))

    not_a_mapping = StringSession.from_data([1, 2, 3])
    with pytest.raises(ValueError, match="incomplete"):
        Session(string_session=str(not_a_mapping))

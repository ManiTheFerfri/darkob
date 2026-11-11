"""Offline regression coverage for the merged maxrubika 1.18 surfaces."""

from __future__ import annotations

import importlib
import json
import logging
import os
import random
import shutil
import sqlite3
import tempfile
from contextlib import asynccontextmanager
from hashlib import sha256
from pathlib import Path
from types import SimpleNamespace

import aiohttp
import pytest

import darkob
from darkob import Bot, Messenger, Shad
from darkob.TheRubino import Rubino
from darkob.client.core.session import Session, StringSession
from darkob.data import Data
from darkob.rubino.crypto import Crypto
from darkob.rubino.exceptions import InvalidInput, NetworkError
from darkob.utils import http as http_utils


PROXY = "http://127.0.0.1:8765"
AUTH = "a" * 32
SESSION_VALUES = (
    "+989000000000",
    AUTH,
    "u0session-guid",
    "darkob-upstream-tests",
    "private-key",
)
ROOT_ALIASES = {
    "Rubino",
    "rubino",
    "RubiAI",
    "RubiAi",
    "rubiai",
    "RubikaAI",
    "RubikaAi",
    "RubikaTV",
    "rubikatv",
}


# A) Root exports -----------------------------------------------------------


def test_root_aliases_resolve_after_all_ordinary_exports():
    for name in darkob.__all__:
        if name not in ROOT_ALIASES:
            getattr(darkob, name)

    from darkob import (  # noqa: PLC0415 - import order is the behavior tested
        RubiAI,
        RubiAi,
        RubikaAI,
        RubikaAi,
        RubikaTV,
        Rubino as RootRubino,
        rubiai,
        rubikatv,
        rubino,
    )

    for alias in (RootRubino, rubino, RubiAI, RubiAi, rubiai, RubikaAI,
                  RubikaAi, RubikaTV, rubikatv):
        assert isinstance(alias, type)

    assert RootRubino is rubino is darkob.Rubino is darkob.rubino
    assert RubiAI is RubiAi is rubiai is RubikaAI is RubikaAi
    assert darkob.RubiAI is RubiAI
    assert darkob.RubikaAI is RubiAI
    assert RubikaTV is rubikatv is darkob.RubikaTV is darkob.rubikatv
    assert ROOT_ALIASES <= set(darkob.__all__)


def test_root_metadata_helpers_exported_and_unknown_attribute_fails():
    from darkob import __author__, show_announcements  # noqa: PLC0415

    assert callable(show_announcements)
    assert isinstance(__author__, str) and __author__
    assert {"show_announcements", "__author__"} <= set(darkob.__all__)
    with pytest.raises(AttributeError):
        getattr(darkob, "not_an_upstream_118_export")


# B) API retention ----------------------------------------------------------


def test_documented_class_methods_remain_a_subset_of_merged_api():
    api_path = Path(__file__).resolve().parents[1] / "docs" / "api.json"
    if not api_path.is_file():
        pytest.skip("docs/api.json is not available")

    with api_path.open(encoding="utf-8") as stream:
        document = json.load(stream)

    for class_name, cls in (("Bot", Bot), ("Messenger", Messenger), ("Shad", Shad)):
        methods = {
            item["name"]
            for item in document["classes"][class_name]["methods"]
        }
        assert methods
        # Bot intentionally injects decorators through DecoratorBridge on each
        # instance. Check the actual runtime object users get, not a class
        # attribute that was never part of the documented dispatch model.
        subject = (
            Bot(token="ABCDE" + "0" * 59, show_welcome=False)
            if cls is Bot
            else cls
        )
        missing = sorted(
            name for name in methods if not callable(getattr(subject, name, None))
        )
        assert not missing, f"{class_name} lost documented methods: {missing}"


@pytest.mark.parametrize("cls", [Messenger, Shad])
def test_representative_118_messenger_methods_are_callable(cls):
    expected = {
        "iter_messages",
        "delete_message",
        "save_message_draft",
        "send_live_location",
        "get_abs_chats",
        "delete_no_access_group_chat",
        "on_scheduled_message",
    }
    assert all(callable(getattr(cls, name, None)) for name in expected)


def test_representative_old_and_118_bot_methods_are_callable():
    for name in (
        "send_message",
        "get_me",
        "delete_message",
        "edit_message",
        "request_send_file",
    ):
        assert callable(getattr(Bot, name, None)), name


# C) Data behavior ----------------------------------------------------------


def test_data_repr_keeps_subclass_prefix_and_cleaning_removes_track_ids():
    class EventData(Data):
        pass

    payload = {
        "track_id": "root",
        "nested": {"track_id": "child", "value": 7},
    }
    data = EventData(payload)

    assert repr(data) == f"EventData({payload!r})"
    assert data.to_clean_dict() == {"nested": {"value": 7}}
    assert json.loads(data.jsonify()) == {"nested": {"value": 7}}


def test_data_index_sees_late_nested_data_and_mutation_invalidates_it():
    data = Data({"stale": 1, "nested": {"removed": 2}})

    # Build the recursive index before inserting a nested Data instance.
    assert data.removed == 2
    data["nested"] = Data({"added": {"late": 42}})

    assert data.late == 42
    assert data.find_keys("removed", default="gone") == "gone"

    del data["nested"]
    assert data.find_keys("late", default="gone") == "gone"
    assert data.stale == 1


# D) Session compatibility --------------------------------------------------


def test_modern_max_database_session_roundtrip_uses_temporary_files():
    directory = tempfile.mkdtemp(prefix="darkob-modern-session-")
    writer = reader = None
    try:
        filename = os.path.join(directory, "modern.max")
        writer = Session(filename, create_file=True)
        writer.insert(*SESSION_VALUES)
        writer.close()

        reader = Session(filename)
        assert reader.is_logged_in is True
        assert reader.information() == SESSION_VALUES
        assert os.path.isfile(filename)
    finally:
        if writer is not None:
            writer.close()
        if reader is not None:
            reader.close()
        shutil.rmtree(directory, ignore_errors=True)


def test_legacy_maxrubika_database_key_reads_without_quarantine():
    from Crypto.Cipher import AES

    directory = tempfile.mkdtemp(prefix="darkob-legacy-session-")
    reader = None
    try:
        filename = os.path.join(directory, "legacy.max")
        payload = {
            "phone": SESSION_VALUES[0],
            "auth": SESSION_VALUES[1],
            "guid": SESSION_VALUES[2],
            "agent": SESSION_VALUES[3],
            "private_key": SESSION_VALUES[4],
        }
        key = sha256(b"maxrubika_session_full_encrypt_v2").digest()
        nonce = b"\x01" * 12
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(
            json.dumps(payload).encode("utf-8")
        )

        connection = sqlite3.connect(filename)
        try:
            connection.execute("CREATE TABLE session (data BLOB)")
            connection.execute(
                "INSERT INTO session VALUES (?)", (nonce + tag + ciphertext,)
            )
            connection.commit()
        finally:
            connection.close()

        original_bytes = Path(filename).read_bytes()
        reader = Session(filename)

        assert reader.is_logged_in is True
        assert reader.information() == SESSION_VALUES
        assert Path(filename).read_bytes() == original_bytes
        assert list(Path(directory).glob("legacy.max.corrupt-*")) == []
    finally:
        if reader is not None:
            reader.close()
        shutil.rmtree(directory, ignore_errors=True)


def test_current_string_session_roundtrip_and_wrong_password_rejection():
    payload = {"phone": "+989000000000", "auth": AUTH, "nested": {"ok": True}}
    encoded = str(StringSession.from_data(payload))

    assert StringSession(encoded).to_data() == payload
    with pytest.raises(ValueError, match="wrong password"):
        Session(string_session=encoded, password="definitely-wrong")


def test_legacy_string_session_password_roundtrip_after_secret_restoration():
    payload = {"phone": "+989000000000", "auth": AUTH, "legacy": True}
    original_secret = StringSession._SECRET_PASSWORD
    try:
        StringSession._SECRET_PASSWORD = b"MAXRubika_Ultra_Secret_2026"
        encoded = str(StringSession.from_data(payload))
    finally:
        StringSession._SECRET_PASSWORD = original_secret

    assert StringSession._SECRET_PASSWORD == original_secret
    assert StringSession(encoded).to_data() == payload


# Shared offline HTTP doubles ----------------------------------------------


class RecordingResponse:
    def __init__(self, result, status=200):
        self._result = result
        self.status = status

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        return False

    async def json(self):
        return self._result

    def raise_for_status(self):
        if self.status >= 400:
            raise aiohttp.ClientResponseError(
                request_info=None,
                history=(),
                status=self.status,
            )


class RecordingPostSession:
    def __init__(self, *responses):
        self._responses = list(responses)
        self.posts = []

    def post(self, url, **kwargs):
        self.posts.append((url, kwargs))
        if not self._responses:
            raise AssertionError("No fake response queued for post")
        response = self._responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return response


def install_owner_session(monkeypatch, session):
    @asynccontextmanager
    async def fake_request_session(owner):
        yield session, owner.proxy

    monkeypatch.setattr(http_utils, "request_session", fake_request_session)


# E) Shared request_session -------------------------------------------------


def install_aiohttp_recorder(monkeypatch):
    connectors = []
    timeouts = []
    sessions = []

    def tcp_connector(*, ssl):
        connector = SimpleNamespace(ssl=ssl)
        connectors.append(connector)
        return connector

    def client_timeout(*, total):
        timeout = SimpleNamespace(total=total)
        timeouts.append(timeout)
        return timeout

    class StandaloneSession:
        def __init__(self, *, connector, timeout):
            self.connector = connector
            self.timeout = timeout
            self.closed = False
            self.close_calls = 0

        async def close(self):
            self.close_calls += 1
            self.closed = True

    def client_session(*, connector, timeout):
        session = StandaloneSession(connector=connector, timeout=timeout)
        sessions.append(session)
        return session

    monkeypatch.setattr(aiohttp, "TCPConnector", tcp_connector)
    monkeypatch.setattr(aiohttp, "ClientTimeout", client_timeout)
    monkeypatch.setattr(aiohttp, "ClientSession", client_session)
    return connectors, timeouts, sessions


@pytest.mark.parametrize("configured_ssl, expected_ssl", [(None, True), (False, False)])
async def test_standalone_request_session_forwards_tls_proxy_timeout_and_closes(
    monkeypatch, configured_ssl, expected_ssl
):
    connectors, timeouts, sessions = install_aiohttp_recorder(monkeypatch)
    owner = SimpleNamespace(
        _client=None,
        client=None,
        proxy=PROXY,
        timeout=12.75,
    )
    if configured_ssl is not None:
        owner.verify_ssl = configured_ssl

    async with http_utils.request_session(owner) as (session, proxy):
        assert session is sessions[0]
        assert proxy == PROXY
        assert session.closed is False

    assert connectors[0].ssl is expected_ssl
    assert timeouts[0].total == 12.75
    assert session.timeout is timeouts[0]
    assert session.connector is connectors[0]
    assert session.close_calls == 1
    assert session.closed is True


async def test_pooled_connected_session_is_reused_without_close(monkeypatch):
    class PooledSession:
        closed = False
        close_calls = 0

        async def close(self):
            self.close_calls += 1

    def unexpected_session(*args, **kwargs):
        raise AssertionError("A pooled owner must not construct ClientSession")

    monkeypatch.setattr(aiohttp, "ClientSession", unexpected_session)
    pooled = PooledSession()
    client = SimpleNamespace(
        connection=SimpleNamespace(session=pooled),
        proxy="http://client-proxy.invalid:8080",
    )
    owner = SimpleNamespace(_client=client, client=None, proxy=PROXY)

    async with http_utils.request_session(owner) as (session, proxy):
        assert session is pooled
        assert proxy == PROXY

    assert pooled.close_calls == 0


# F) Auth-only wrappers and bounded Rubino requests -------------------------


@pytest.mark.parametrize("class_name", ["RubiAI", "RubikaTV", "Rubino"])
def test_auth_only_wrapper_tls_default_and_opt_out(class_name):
    cls = getattr(darkob, class_name)

    assert cls(auth=AUTH, show_welcome=False).verify_ssl is True
    assert cls(auth=AUTH, show_welcome=False, verify_ssl=False).verify_ssl is False


async def test_rubiai_request_uses_configured_base_url_and_proxy(monkeypatch):
    rubiai = darkob.RubiAI(
        auth=AUTH, proxy=PROXY, as_dict=True, show_welcome=False
    )
    session = RecordingPostSession(
        RecordingResponse({"data": {"status": "OK", "output": {"ok": True}}})
    )
    install_owner_session(monkeypatch, session)

    assert await rubiai.request("testMethod", {"value": 1}) == {"ok": True}
    url, kwargs = session.posts[0]
    assert url == "https://rubichat1.iranlms.ir/"
    assert kwargs["proxy"] == PROXY
    assert kwargs["json"]["data"]["input"] == {"value": 1}


async def test_tv_request_uses_selected_vod_url_and_proxy(monkeypatch):
    tv = darkob.RubikaTV(
        auth=AUTH, proxy=PROXY, as_dict=True, show_welcome=False
    )
    session = RecordingPostSession(RecordingResponse({"data": {"ok": True}}))
    install_owner_session(monkeypatch, session)
    monkeypatch.setattr(random, "choice", lambda urls: urls[7])

    assert await tv.request("testMethod") == {"ok": True}
    url, kwargs = session.posts[0]
    assert url == tv.VOD_URLS[7]
    assert kwargs["proxy"] == PROXY
    assert kwargs["json"]["auth"] == AUTH


def make_offline_rubino():
    rubino = Rubino.__new__(Rubino)
    rubino.api_version = 1
    rubino.as_dict = False
    rubino._client = None
    rubino._auth = AUTH
    rubino.profile_id = "default-profile"
    rubino.rubino_url = "https://rubino-test.invalid/"
    rubino.failed_count = 0
    rubino.max_retries = 3
    rubino.logger = logging.getLogger("darkob.tests.rubino")
    rubino.proxy = PROXY
    rubino.timeout = 1.0
    rubino.verify_ssl = True
    return rubino


def transparent_rubino_crypto(monkeypatch):
    monkeypatch.setattr(Crypto, "encrypt_auth", lambda text, auth: text)
    monkeypatch.setattr(Crypto, "decrypt_auth", lambda data, auth: data)


async def test_rubino_v1_payload_success_and_decrypted_data(monkeypatch):
    rubino = make_offline_rubino()
    transparent_rubino_crypto(monkeypatch)
    response_payload = {
        "data_enc": json.dumps(
            {"data": {"answer": 42}, "status": "OK", "status_det": None}
        )
    }
    session = RecordingPostSession(RecordingResponse(response_payload))
    install_owner_session(monkeypatch, session)

    result = await rubino.request(
        "testMethod", {"profile_id": "override-profile", "value": 7}
    )

    assert isinstance(result, Data)
    assert result.answer == 42
    url, kwargs = session.posts[0]
    assert url == "https://rubino-test.invalid/"
    assert kwargs["proxy"] == PROXY
    assert kwargs["json"]["api_version"] == "1"
    assert kwargs["json"]["auth"] == AUTH
    inner = json.loads(kwargs["json"]["data_enc"])
    assert inner["method"] == "testMethod"
    assert inner["profile_id"] == "override-profile"
    assert inner["input"] == {"value": 7}


async def test_rubino_v1_nontransient_api_error_raises_without_retry(monkeypatch):
    rubino = make_offline_rubino()
    transparent_rubino_crypto(monkeypatch)
    session = RecordingPostSession(
        RecordingResponse({"status": "ERROR", "status_det": "INVALID_INPUT"})
    )
    install_owner_session(monkeypatch, session)

    with pytest.raises(InvalidInput):
        await rubino.request("testMethod")

    assert len(session.posts) == 1


async def test_rubino_transient_errors_use_one_bounded_attempt_budget(monkeypatch):
    rubino = make_offline_rubino()
    transparent_rubino_crypto(monkeypatch)
    rubino_exceptions = importlib.import_module("darkob.rubino.exceptions")

    def transient_error(*args):
        raise RuntimeError("server error")

    monkeypatch.setattr(rubino_exceptions, "raise_exception", transient_error)
    session = RecordingPostSession(
        *(RecordingResponse({"status": "ERROR", "status_det": "SERVER_ERROR"})
          for _ in range(3))
    )
    install_owner_session(monkeypatch, session)

    with pytest.raises(NetworkError):
        await rubino.request("testMethod")

    assert len(session.posts) == 3
    assert len(session.posts) != len(rubino.RUBINO_URLS) * rubino.max_retries
    assert all(kwargs["proxy"] == PROXY for _, kwargs in session.posts)

"""Tests for Phase 2 (failover, flood ceiling) and Phase 3 (crypto engine)."""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from Crypto.PublicKey import RSA

import darkob
from darkob.client.core.api import Api
from darkob.crypto import LARGE_PAYLOAD, CryptoEngine

# ---------------------------------------------------------------------------
# CryptoEngine
# ---------------------------------------------------------------------------

AUTH = "abcdefgh" * 4
PEM = RSA.generate(1024).export_key().decode()


def engine(**kwargs) -> CryptoEngine:
    return CryptoEngine(auth=AUTH, **kwargs)


def test_key_is_derived_once():
    crypto = engine()

    assert crypto.key is not None
    assert crypto.key == engine().key


def test_encrypt_decrypt_roundtrip():
    crypto = engine()

    encrypted = crypto.encrypt_json({"method": "getMe", "input": {}})

    assert crypto.decrypt_json(encrypted) == {"method": "getMe", "input": {}}


def test_api_version_5_roundtrip():
    crypto = CryptoEngine(auth=AUTH, api_version=5)

    assert crypto.decrypt_json(crypto.encrypt_json({"a": 1})) == {"a": 1}


def test_signer_is_cached_and_reused():
    crypto = engine(private_key_pem=PEM)

    assert crypto.can_sign is True
    assert crypto.signer is crypto.signer


def test_sign_requires_a_private_key():
    crypto = engine()

    with pytest.raises(RuntimeError):
        crypto.sign("payload")


def test_sign_and_verify():
    from Crypto.Hash import SHA256
    from Crypto.Signature import pkcs1_15
    import base64

    crypto = engine(private_key_pem=PEM)
    signature = crypto.sign("payload")

    public = pkcs1_15.new(RSA.import_key(PEM).publickey())
    public.verify(SHA256.new(b"payload"), base64.b64decode(signature))


async def test_async_roundtrip_small_payload():
    crypto = engine()

    encrypted = await crypto.encrypt_json_async({"a": 1})

    assert await crypto.decrypt_json_async(encrypted) == {"a": 1}


async def test_large_payload_is_offloaded():
    crypto = engine()
    big = {"blob": "x" * (LARGE_PAYLOAD + 1024)}

    encrypted = await crypto.encrypt_json_async(big)

    assert len(encrypted) > LARGE_PAYLOAD
    assert await crypto.decrypt_json_async(encrypted) == big


def test_repr_reports_state():
    text = repr(engine(private_key_pem=PEM))

    assert "has_key=True" in text
    assert "can_sign=True" in text


# ---------------------------------------------------------------------------
# Latency-aware failover
# ---------------------------------------------------------------------------


def make_client(**overrides):
    base = dict(
        DEFAULT_PLATFORM={"platform": "PWA"},
        _original_platform="pwa",
        user_agent="test",
        max_retries=2,
        timeout=5,
        verify_ssl=False,
        proxy=None,
        stop_on_first_match=False,
        handlers={},
        flood_sleep_threshold=0,
    )
    base.update(overrides)
    return SimpleNamespace(**base)


def wire(api: Api, count: int = 3) -> None:
    api.api_map = {str(i): f"https://dc{i}.test/" for i in range(count)}
    api.api_priority = [str(i) for i in range(count)]
    api.api_url = "https://dc0.test/"
    api._api_code_by_url = {f"https://dc{i}.test": str(i) for i in range(count)}


async def test_record_latency_uses_a_moving_average():
    api = Api(make_client())

    api.record_latency("a", 0.100)
    api.record_latency("a", 0.200)

    assert api._latency["a"] == pytest.approx(100 * 0.8 + 200 * 0.2)


async def test_fastest_endpoint_is_tried_first():
    api = Api(make_client())
    wire(api, 3)

    api._latency["https://dc2.test"] = 10.0
    api._latency["https://dc0.test"] = 100.0
    api._latency["https://dc1.test"] = 50.0

    assert api._endpoint_candidates()[0] == "https://dc2.test"


async def test_open_endpoints_sort_last():
    api = Api(make_client())
    wire(api, 2)

    breaker = api.breaker_for("https://dc0.test")
    breaker.threshold = 1
    breaker.record_failure()
    api._latency["https://dc0.test"] = 1.0  # fastest, but unhealthy
    api._latency["https://dc1.test"] = 500.0

    assert api._endpoint_candidates()[0] == "https://dc1.test"


async def test_unmeasured_endpoints_keep_discovery_order():
    api = Api(make_client())
    wire(api, 3)

    assert api._endpoint_candidates() == [
        "https://dc0.test",
        "https://dc1.test",
        "https://dc2.test",
    ]


# ---------------------------------------------------------------------------
# Flood-wait ceiling
# ---------------------------------------------------------------------------


class FakeResponse:
    def __init__(self, status, payload=None):
        self.status = status
        self._payload = payload

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    def raise_for_status(self):
        if self.status >= 400:
            raise RuntimeError(f"HTTP {self.status}")

    async def json(self):
        return self._payload


class FakeSession:
    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = []

    def post(self, url, json=None, proxy=None):
        self.calls.append(url)
        return FakeResponse(*self._responses.pop(0))


async def test_flood_threshold_gives_up_instead_of_waiting():
    api = Api(make_client(flood_sleep_threshold=1.0))
    wire(api, 1)
    api._RATE_LIMIT_BACKOFF = 60.0  # the first wait already exceeds the ceiling

    real = api.session
    session = FakeSession([(429, None)] * 5)
    api.session = session

    try:
        result = await api._http_request({}, max_retries=5)
    finally:
        await real.close()

    assert result is None
    assert len(session.calls) == 1, "it must not sleep through a long flood wait"


async def test_without_a_threshold_rate_limits_are_retried():
    api = Api(make_client(flood_sleep_threshold=0))
    wire(api, 1)
    api._RATE_LIMIT_BACKOFF = 0.01

    real = api.session
    session = FakeSession([(429, None), (200, {"status": "OK"})])
    api.session = session

    try:
        result = await api._http_request({}, max_retries=3)
    finally:
        await real.close()

    assert result == {"status": "OK"}
    assert len(session.calls) == 2


def test_crypto_engine_is_exported():
    assert hasattr(darkob, "__version__")
    assert CryptoEngine(auth=AUTH).key

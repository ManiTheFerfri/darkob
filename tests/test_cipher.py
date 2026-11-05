"""Tests for the Cipher helpers (no network, pure crypto roundtrips)."""

from __future__ import annotations

import pytest

from darkob.client.core.cipher import Cipher

KEY = "a" * 32
PAYLOAD = {"method": "sendMessage", "input": {"text": "سلام world"}}


def test_secret_is_lowercase_and_has_requested_length():
    secret = Cipher.secret(32)

    assert len(secret) == 32
    assert secret.islower()
    assert secret.isalpha()


def test_secret_is_random():
    assert Cipher.secret(32) != Cipher.secret(32)


@pytest.mark.parametrize("value,expected", [("a", "g")])
def test_decode_auth_single_characters(value, expected):
    assert Cipher.decode_auth(value) == expected


def test_decode_auth_preserves_length_and_case_class():
    encoded = Cipher.decode_auth("abcDEF123")

    assert len(encoded) == 9
    assert encoded[0:3].islower()
    assert encoded[3:6].isupper()
    assert encoded[6:].isdigit()


def test_decode_auth_passes_through_unknown_characters():
    assert Cipher.decode_auth("-_.!") == "-_.!"


def test_passphrase_requires_32_characters():
    with pytest.raises(ValueError):
        Cipher.passphrase("short")


def test_passphrase_is_deterministic_and_32_chars():
    auth = "abcdefgh" * 4

    first = Cipher.passphrase(auth)

    assert first == Cipher.passphrase(auth)
    assert len(first) == 32


def test_secret_v5_requires_32_characters():
    with pytest.raises(ValueError):
        Cipher.secret_v5("short")


def test_secret_v5_is_deterministic_and_shifts_characters():
    auth = "abcdefgh" * 4

    result = Cipher.secret_v5(auth)

    assert result == Cipher.secret_v5(auth)
    assert len(result) == 32
    assert result != auth


def test_encrypt_decrypt_roundtrip():
    encrypted = Cipher.encrypt(PAYLOAD, KEY)

    assert isinstance(encrypted, str)
    assert Cipher.decrypt(encrypted, KEY) == PAYLOAD


def test_encrypt_decrypt_v5_roundtrip():
    encrypted = Cipher.encrypt_v5(PAYLOAD, KEY)

    assert Cipher.decrypt_v5(encrypted, KEY) == PAYLOAD


def test_encrypt_produces_different_ciphertext_than_plaintext():
    encrypted = Cipher.encrypt(PAYLOAD, KEY)

    assert "sendMessage" not in encrypted


def test_decrypt_with_wrong_key_fails():
    encrypted = Cipher.encrypt(PAYLOAD, KEY)

    with pytest.raises(Exception):
        Cipher.decrypt(encrypted, "b" * 32)


def test_sign_and_verify_with_generated_keys():
    from Crypto.Hash import SHA256
    from Crypto.PublicKey import RSA
    from Crypto.Signature import pkcs1_15
    import base64

    keys = RSA.generate(1024)
    signer = pkcs1_15.new(keys)
    payload = '{"method":"getMe"}'

    signature = Cipher.sign(signer, payload)

    verifier = pkcs1_15.new(RSA.import_key(keys.publickey().export_key()))
    verifier.verify(
        SHA256.new(payload.encode("utf-8")), base64.b64decode(signature)
    )

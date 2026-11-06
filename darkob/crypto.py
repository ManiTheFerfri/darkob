"""Cached cryptography for session traffic.

The cipher itself is fast; what used to be slow was re-deriving keys and
re-parsing PEM material on every call. :class:`CryptoEngine` keeps the AES
key, the IV and the parsed RSA signer for the life of a session, and
offloads genuinely large payloads to a worker thread so the event loop
keeps running other handlers::

    from darkob.crypto import CryptoEngine

    engine = CryptoEngine(auth="...", private_key_pem="-----BEGIN RSA ...")
    payload = engine.encrypt_json({"method": "getMe"})
    signature = engine.sign(payload)
"""

from __future__ import annotations

import asyncio
from typing import Any, Optional

from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA

from .client.core.cipher import Cipher
from .utils.json_backend import dumps, loads

__all__ = ["CryptoEngine", "LARGE_PAYLOAD"]

#: Payloads above this size are encrypted off the event loop.
LARGE_PAYLOAD = 256 * 1024


class CryptoEngine:
    """Owns the key material for one session."""

    __slots__ = ("_key", "_key_bytes", "_iv", "_signer", "_api_version")

    def __init__(
        self,
        auth: Optional[str] = None,
        private_key_pem: Optional[str] = None,
        *,
        api_version: int = 6,
    ) -> None:
        self._api_version = api_version
        self._iv = Cipher.AES_IV
        self._signer: Optional[Any] = None
        self._key: Optional[str] = None
        self._key_bytes: Optional[bytes] = None

        if auth:
            self._set_auth(auth)

        if private_key_pem:
            self._set_private_key(private_key_pem)

    # -- key material -----------------------------------------------------

    def _set_auth(self, auth: str) -> None:
        """Derive and cache the AES key once per session."""
        if self._key == auth:
            return

        if self._api_version == 5:
            key = Cipher.secret_v5(auth)
        else:
            key = Cipher.passphrase(auth)

        self._key = key
        self._key_bytes = key.encode()

    def _set_private_key(self, private_key_pem: Any) -> None:
        """Parse the RSA key and build the signer once."""
        if self._signer is not None:
            return

        pem = private_key_pem
        if isinstance(pem, str):
            pem = pem.encode()
        self._signer = pkcs1_15.new(RSA.import_key(pem))

    # -- properties -------------------------------------------------------

    @property
    def key(self) -> Optional[str]:
        """The AES key string, as the wire format expects."""
        return self._key

    @property
    def signer(self) -> Optional[Any]:
        """The cached PKCS#1 v1.5 signer, or ``None`` when unsigned."""
        return self._signer

    @property
    def can_sign(self) -> bool:
        return self._signer is not None

    # -- synchronous ------------------------------------------------------

    def encrypt_json(self, data: Any) -> str:
        """Serialise and encrypt in one step."""
        payload = dumps(data) if not isinstance(data, str) else data
        if self._api_version == 5:
            return Cipher.encrypt_v5(payload, key=self._key_bytes)
        return Cipher.encrypt(payload, key=self._key)

    def decrypt_json(self, data: str) -> Any:
        """Decrypt and deserialise in one step."""
        if self._api_version == 5:
            decrypted = Cipher.decrypt_v5(data, key=self._key_bytes)
        else:
            decrypted = Cipher.decrypt(data, key=self._key)
        return decrypted if isinstance(decrypted, (dict, list)) else loads(decrypted)

    def sign(self, data: str) -> str:
        """Sign *data*; raises when the engine has no private key."""
        if self._signer is None:
            raise RuntimeError("CryptoEngine has no private key to sign with.")
        return Cipher.sign(self._signer, data)

    # -- asynchronous -----------------------------------------------------

    async def encrypt_json_async(self, data: Any) -> str:
        """Encrypt on a worker thread when the payload is large."""
        payload = dumps(data) if not isinstance(data, str) else data
        if len(payload) < LARGE_PAYLOAD:
            return self.encrypt_json(payload)
        return await asyncio.to_thread(self.encrypt_json, payload)

    async def decrypt_json_async(self, data: str) -> Any:
        """Decrypt on a worker thread when the payload is large."""
        if len(data) < LARGE_PAYLOAD:
            return self.decrypt_json(data)
        return await asyncio.to_thread(self.decrypt_json, data)

    def __repr__(self) -> str:
        return (
            f"CryptoEngine(api_version={self._api_version}, "
            f"has_key={self._key is not None}, can_sign={self.can_sign})"
        )

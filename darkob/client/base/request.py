import asyncio
import json
from ...data import Data  # noqa: F401 - public compatibility alias
from typing import Dict, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    import darkob

#: Payloads at or above this size are encrypted off the event loop.
LARGE_PAYLOAD = 256 * 1024


class Request:
    async def request(
        self: "darkob.Messenger",
        method: str,
        input: Optional[Dict] = None,
        tmp_session: bool = False,
        encrypt: bool = True
    ):
        """
        Build and send a request to the Rubika API.

        Parameters:
            method (str): API method name (e.g., 'sendMessage', 'getUserInfo').
            input (dict, optional): Input data for the method.
            tmp_session (bool): Use temporary session instead of auth (default: False).
            encrypt (bool): Encrypt the request data (default: True).

        Returns:
            Data, Event, dict, or None: The API response.
                - If `as_dict=True` on the client, returns a plain dict.
                - Otherwise, returns a Data object.

        Raises:
            NoConnection: If the client has not been started and `tmp_session=False`.
        """
        from ..core.cipher import Cipher
        from ...types import Event
        from .. import exceptions
        from ...data import Data

        if not getattr(self, 'connection', None):
            if tmp_session:
                await self.connect()
            else:
                raise exceptions.NoConnection(
                    "Client is not connected. Call 'start()' first or use the client as a context manager.")

        if not self.connection.api_url:
            await self.connection.get_dcs(max_retries=self.max_retries)

        if self.auth is None:
            self.auth = Cipher.secret(length=32)

        if self.key is None:
            if self.API_VERSION == 5:
                self.key = Cipher.secret_v5(self.auth)
            else:
                self.key = Cipher.passphrase(self.auth)

        client = self.DEFAULT_PLATFORM.copy()

        data = {"api_version": str(self.API_VERSION)}

        if self.API_VERSION == 5:
            if tmp_session:
                data["tmp_session"] = self.auth
            else:
                data["auth"] = self.auth
        else:
            data["tmp_session" if tmp_session else "auth"] = (
                self.auth if tmp_session else self.decode_auth
            )

        data_enc = {"method": method, "input": input or {}, "client": client}

        if encrypt:
            # Large payloads (long media metadata, big batches) are encrypted
            # on a worker thread so other handlers keep running.
            plain = json.dumps(data_enc)
            if len(plain) >= LARGE_PAYLOAD:
                if self.API_VERSION == 5:
                    data["data_enc"] = await asyncio.to_thread(
                        Cipher.encrypt_v5, plain, self.key
                    )
                else:
                    data["data_enc"] = await asyncio.to_thread(
                        Cipher.encrypt, plain, self.key
                    )
                    if not tmp_session:
                        data["sign"] = await asyncio.to_thread(
                            Cipher.sign, self.import_key, data["data_enc"]
                        )
            elif self.API_VERSION == 5:
                data["data_enc"] = Cipher.encrypt_v5(plain, key=self.key)
            else:
                data["data_enc"] = Cipher.encrypt(data_enc, key=self.key)
                if not tmp_session:
                    data["sign"] = Cipher.sign(self.import_key, data["data_enc"])

        result = await self.connection._http_request(
            data, max_retries=self.max_retries
        )

        if result is None:
            return None

        data_enc = result.get('data_enc')
        if data_enc is not None:
            if self.API_VERSION == 5:
                result = Cipher.decrypt_v5(data_enc, key=self.key)
            else:
                result = Cipher.decrypt(data_enc, key=self.key)

        status = result.get('status')
        status_det = result.get('status_det')

        if status == 'OK' and status_det == 'OK':
            data_result = result.get('data')

            if data_result is None:
                return Data({})

            if isinstance(data_result, dict):
                data_result['client'] = self

            result_obj = Event(data_result)

            if getattr(self, 'as_dict', False):
                return result_obj.to_dict()

            return result_obj

        exceptions.raise_exception(status_det, result, None)
import asyncio
import os
from typing import Callable, Optional, Union, TYPE_CHECKING

from ..exceptions import NetworkError

if TYPE_CHECKING:
    import darkob
    from ...data import Data


class DownloadFile:
    async def download_file(
        self: "darkob.Messenger",
        file_inline: Optional[Union[dict, "Data"]] = None,
        dc_id: Optional[int] = None,
        file_id: Optional[int] = None,
        access_hash: Optional[str] = None,
        size: Optional[int] = None,
        chunk: int = 131072,
        callback: Optional[Callable[[int, int], Optional["asyncio.Future"]]] = None,
        gather: bool = False,
        save_as: Optional[Union[str, bool]] = None,
        file_name: Optional[str] = None,
        as_base64: bool = False
    ) -> Union[bytes, str, "Data"]:
        """
        Download a file from Rubika/Shad.

        Parameters:
            file_inline (dict | Data, optional): File inline object from messages.
                If provided, dc_id, file_id, access_hash, size will be extracted.
            dc_id (int, optional): Data Center ID (if file_inline not provided).
            file_id (int, optional): Unique identifier of the file.
            access_hash (str, optional): Access hash associated with the file.
            size (int, optional): Total size of the file in bytes.
            chunk (int, optional): Size of each download chunk (default: 131072).
            callback (callable, optional): Progress callback(total_size, downloaded_size).
            gather (bool, optional): Download chunks in parallel (default: False).
            save_as (str | bool, optional): Directory path or True for current dir. If None, returns bytes.
            file_name (str, optional): Custom file name.
            as_base64 (bool, optional): Return as base64 encoded string (default: False).

        Returns:
            bytes, str, or Data: File content (bytes), base64 string, or Data object (when save_as used).

        Raises:
            NetworkError: A chunk fails all retries or returns the wrong length.
                With save_as, a partial file is left on disk; no OK result is returned.
        """
        import inspect
        import base64
        import aiofiles
        from ...data import Data
        from .. import exceptions
        from ..core.configs import PLATFORMS

        if file_inline:
            if isinstance(file_inline, Data):
                fi = file_inline
            elif isinstance(file_inline, dict):
                fi = Data(file_inline)
            else:
                raise exceptions.InvalidInput("'file_inline' must be a dict or Data object.")

            dc_id = fi.find_keys('dc_id')
            file_id = fi.find_keys('file_id')
            access_hash = fi.find_keys('access_hash_rec')
            size = fi.find_keys('size')

            if not file_name:
                file_name = fi.find_keys('file_name')

        if any(value is None for value in (dc_id, file_id, access_hash, size)):
            raise exceptions.InvalidInput(
                "Either 'file_inline' or all of 'dc_id', 'file_id', 'access_hash', 'size' must be provided."
            )

        if save_as is True:
            save_dir = os.getcwd()
        elif isinstance(save_as, str):
            save_dir = save_as
        else:
            save_dir = None

        max_retries = self.max_retries

        headers = {
            "auth": self.auth,
            "access-hash-rec": access_hash,
            "file-id": str(file_id),
            "user-agent": self.user_agent,
        }

        platform = self._original_platform
        platform_config = PLATFORMS.get(platform, {})
        storage_prefix = platform_config.get('storage_prefix', 'messenger')
        base_url = f"https://{storage_prefix}{dc_id}.iranlms.ir"

        async def fetch_chunk(session, start: int, end: int) -> bytes:
            chunk_headers = {
                **headers,
                "start-index": str(start),
                "last-index": str(end),
            }
            expected_length = end - start + 1
            for attempt in range(max_retries):
                try:
                    async with session.post(
                        "/GetFile.ashx",
                        headers=chunk_headers,
                        proxy=self.proxy
                    ) as resp:
                        if resp.status == 200:
                            data = await resp.read()
                            if len(data) != expected_length:
                                raise NetworkError(
                                    f"Chunk {start}-{end} returned {len(data)} bytes; "
                                    f"expected {expected_length}."
                                )
                            return data
                        if resp.status >= 500:
                            raise exceptions.ServerError(
                                f"Server error: {resp.status}"
                            )
                        self.logger.warning(
                            f"Download failed with status {resp.status}"
                        )
                except asyncio.TimeoutError:
                    self.logger.warning(
                        f"Timeout on chunk {start}-{end} (attempt {attempt+1})"
                    )
                except exceptions.ServerError:
                    self.logger.warning(
                        f"Server error on chunk {start}-{end} (attempt {attempt+1})"
                    )
                except NetworkError:
                    raise
                except Exception as e:
                    self.logger.warning(
                        f"Error downloading chunk {start}-{end} (attempt {attempt+1}): {e}"
                    )

                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)

            raise NetworkError(
                f"Download failed for chunk {start}-{end} after {max_retries} attempts."
            )

        async def handle_callback(total: int, current: int):
            if not callable(callback):
                return
            try:
                if inspect.iscoroutinefunction(callback):
                    await callback(total, current)
                else:
                    callback(total, current)
            except exceptions.CancelledError:
                return
            except Exception as e:
                self.logger.error(f"Callback error: {e}")

        verify_ssl = getattr(self, "verify_ssl", True)
        connection = getattr(self, "connection", None)
        if connection is None:
            raise exceptions.NoConnection(
                "Client is not connected. Call 'start()' first."
            )
        # Reuse the pooled session for this file server rather than
        # opening a new one (and a new TLS handshake) per download.
        async with connection.aux_session(base_url, verify_ssl) as session:
            if save_dir:
                filename = file_name or "download.bin"
                filepath = os.path.join(save_dir, filename)
                os.makedirs(save_dir, exist_ok=True)

                async with aiofiles.open(filepath, "wb") as f:
                    for start in range(0, size, chunk):
                        end = min(start + chunk, size) - 1
                        data = await fetch_chunk(session, start, end)
                        await f.write(data)
                        await handle_callback(size, end + 1)

                result_dict = {
                    "status": "OK",
                    "message": f"File saved to {filepath}"
                }

                if getattr(self, 'as_dict', False):
                    return result_dict
                return Data(result_dict)

            elif gather:
                tasks = [
                    fetch_chunk(session, start, min(start + chunk, size) - 1)
                    for start in range(0, size, chunk)
                ]
                chunks = await asyncio.gather(*tasks)
                result = b"".join(chunks)
                await handle_callback(size, len(result))
                return base64.b64encode(result).decode() if as_base64 else result

            else:
                result = bytearray()
                for start in range(0, size, chunk):
                    end = min(start + chunk, size) - 1
                    data = await fetch_chunk(session, start, end)
                    result.extend(data)
                    await handle_callback(size, len(result))
                result = bytes(result)
                return base64.b64encode(result).decode() if as_base64 else result
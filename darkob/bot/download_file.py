import asyncio
import base64
import datetime
import logging
import os
import re
from contextlib import asynccontextmanager
from typing import Callable, Optional, TYPE_CHECKING

from .file_extensions import FILE_EXTENSIONS
from .exceptions import InvalidAccess, InvalidInput, Network

if TYPE_CHECKING:
    import darkob

logger = logging.getLogger(__name__)

@asynccontextmanager
async def _borrowed(session):
    """Yield a pooled session without closing it.

    Downloading used to open its own aiohttp.ClientSession, which meant a
    fresh TCP and TLS handshake per file and ignored the client's pool.
    """
    yield session



class DownloadFile:
    def _validate_filename(self, name: str) -> Optional[str]:
        if not name or len(name) > 200:
            return None

        invalid_chars = r'[<>:"/\\|?*]'
        if re.search(invalid_chars, name):
            return None
        return name.strip()

    def _validate_path(self, path: str) -> Optional[str]:
        if not path:
            return None

        if not os.path.isabs(path):
            return None

        if not os.path.exists(path):
            try:
                os.makedirs(path, exist_ok=True)
            except Exception:
                return None

        return path

    def _get_file_extension(self, content_type: str) -> str:
        return FILE_EXTENSIONS.get(content_type.lower(), '.bin')

    def _format_size(self, size: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    async def _download_with_retry(self, download_url: str) -> bytes:
        import aiohttp
        from .exceptions import Network

        max_retries = getattr(self, 'max_retries', 5)
        last_error = None

        for attempt in range(max_retries):
            try:
                async with _borrowed(await self._get_session()) as session:
                    async with session.get(download_url) as response:
                        if response.status == 502:
                            logger.warning(
                                f"Bad Gateway (502) - Attempt {attempt + 1}/{max_retries}"
                            )
                            if attempt < max_retries - 1:
                                await asyncio.sleep(2 ** attempt)
                                continue
                            raise Network("Download failed: Server temporarily unavailable.")

                        if response.status != 200:
                            message = f"Download failed: Server error {response.status}"
                            raise Network(message)

                        return await response.read()

            except aiohttp.ClientError as e:
                last_error = e
                if attempt < max_retries - 1:
                    logger.warning(
                        f"Connection issue - Attempt {attempt + 1}/{max_retries}: {e}"
                    )
                    await asyncio.sleep(2 ** attempt)
                    continue
                message = f"Download failed after multiple attempts: {last_error}"
                raise Network(message)

        if last_error:
            raise Exception(f"Download failed: {last_error}")
        return b''


    async def _download_to_path(
        self,
        url: str,
        full_path: str,
        *,
        resume: bool = True,
        chunk_size: int = 256 * 1024,
        callback=None,
    ) -> int:
        """Stream a file to disk, continuing a partial download.

        Returns the number of bytes written in total (including what was
        already on disk).
        """
        existing = 0
        if resume and os.path.exists(full_path):
            existing = os.path.getsize(full_path)

        session = await self._get_session()
        headers = {"Range": f"bytes={existing}-"} if existing else {}

        async with session.get(
            url, headers=headers, proxy=getattr(self, "proxy", None)
        ) as response:
            if response.status == 416:
                # Nothing left to fetch: the file is already complete.
                return existing
            if response.status not in (200, 206):
                raise Network(
                    dev_message=f"Download failed with HTTP {response.status}."
                )

            if existing and response.status == 200:
                # The server ignored the Range header and sent the whole
                # file. Appending would corrupt it, so start over.
                existing = 0

            mode = "ab" if existing else "wb"
            written = existing

            length = response.headers.get("Content-Length")
            total = written + int(length) if length else 0

            with open(full_path, mode) as handle:
                async for block in response.content.iter_chunked(chunk_size):
                    handle.write(block)
                    written += len(block)
                    if callback:
                        percent = (written / total * 100.0) if total else 0.0
                        callback(written, total or written, percent)

        return written

    async def download_file(
        self: "darkob.Bot",
        file_id: str,
        name: Optional[str] = None,
        path: Optional[str] = None,
        save_as: bool = False,
        as_base64: bool = False,
        callback: Optional[Callable[[int, int, float], None]] = None,
        resume: bool = True,
    ):
        """Download a file by ID, preserving darkob's original return types.

        ``save_as=True`` returns a status dictionary with ``file_path`` and
        ``size``. Otherwise the raw bytes are returned, or a base64 string
        when ``as_base64=True``. Upstream 1.18 changed these returns to a
        ``Data`` wrapper, which would break existing darkob callers, so its
        validation improvements are kept without its return-type change.
        """

        file_response = await self.get_file(file_id)
        if file_response.get("status") != "OK":
            raise InvalidAccess("Failed to get file info.")

        download_url = file_response["data"]["download_url"]

        async with _borrowed(await self._get_session()) as session:
            content_type = "application/octet-stream"
            for attempt in range(self.max_retries):
                try:
                    async with session.head(
                        download_url, allow_redirects=True
                    ) as head_response:
                        if head_response.status == 502:
                            if attempt < self.max_retries - 1:
                                logger.warning(
                                    "Getting file info (502) - Attempt %d/%d",
                                    attempt + 1,
                                    self.max_retries,
                                )
                                await asyncio.sleep(2 ** attempt)
                                continue
                        else:
                            content_type = head_response.headers.get(
                                "Content-Type", ""
                            )
                        break
                except Exception as exc:
                    if attempt < self.max_retries - 1:
                        logger.warning(
                            "Cannot get file info - Attempt %d/%d: %s",
                            attempt + 1,
                            self.max_retries,
                            exc,
                        )
                        await asyncio.sleep(2 ** attempt)
                        continue
                    break

            file_ext = self._get_file_extension(content_type)
            if name:
                validated_name = self._validate_filename(name)
                if not validated_name:
                    raise InvalidInput("Invalid filename.")
                filename = validated_name + file_ext
            else:
                now = datetime.datetime.now()
                filename = now.strftime("%Y%m%d_%H%M%S") + file_ext

            if save_as:
                if path:
                    validated_path = self._validate_path(path)
                    if not validated_path:
                        raise InvalidInput("Invalid or inaccessible path.")
                    save_path = validated_path
                else:
                    downloads_path = os.path.join(
                        os.path.expanduser("~"), "Downloads"
                    )
                    current_path = os.getcwd()
                    save_path = (
                        downloads_path
                        if "Microsoft VS Code" in current_path
                        else current_path
                    )

                full_path = os.path.join(save_path, filename)
                os.makedirs(save_path, exist_ok=True)
                written = await self._download_to_path(
                    download_url,
                    full_path,
                    resume=resume,
                    callback=callback,
                )
                return {
                    "status": "OK",
                    "file_path": full_path,
                    "size": self._format_size(written),
                }

            file_data = await self._download_with_retry(download_url)
            if callback:
                callback(len(file_data), len(file_data), 100.0)
            if as_base64:
                return base64.b64encode(file_data).decode("utf-8")
            return file_data

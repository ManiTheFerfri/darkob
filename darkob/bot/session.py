import asyncio
import logging
import aiohttp
import darkob

logger = logging.getLogger(__name__)

class Session:
    async def _get_session(self: "darkob.Bot") -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            connector = aiohttp.TCPConnector(
                ssl=getattr(self, "verify_ssl", True), limit=20
            )
            self._session = aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
            )
            self._session_loop = asyncio.get_running_loop()
        return self._session

    def _forget_session(self: "darkob.Bot") -> None:
        self._session = None
        self._session_loop = None
        self._close_task = None

    async def close(self: "darkob.Bot") -> None:
        """Async close — must be awaited inside the session's loop."""
        session = self._session
        if session is None or session.closed:
            self._forget_session()
            return

        try:
            await session.close()
        except Exception:
            logger.debug("Error while closing session.", exc_info=True)

        # A failed close must remain retryable; never discard a live transport.
        if session.closed and self._session is session:
            self._forget_session()

    def _schedule_close(self: "darkob.Bot", loop: asyncio.AbstractEventLoop):
        future = asyncio.run_coroutine_threadsafe(self.close(), loop)
        self._close_task = future
        return future

    def disconnect(self: "darkob.Bot") -> None:
        """
        Close the session synchronously, from any context:
          - schedule on a running owner (waiting briefly from synchronous code);
          - run a stopped, open owner to completion from synchronous code;
          - never block the current loop by waiting on itself.

        An already-closed owner cannot await the transport close. This method
        raises an actionable error and retains the reference in that case; the
        transport must instead be closed in its owner before that loop closes.
        """
        session = self._session
        if session is None or session.closed:
            self._forget_session()
            return

        owner = self._session_loop
        if owner is not None and owner.is_closed():
            raise RuntimeError(
                "Cannot disconnect: the owning event loop is closed while the "
                "HTTP session is still open. Close the session in its owning "
                "loop before closing that loop."
            )

        try:
            current = asyncio.get_running_loop()
        except RuntimeError:
            current = None

        if current is not None:
            if owner is None or owner is current:
                self._close_task = current.create_task(self.close())
            elif owner.is_running():
                self._schedule_close(owner)
            else:
                raise RuntimeError(
                    "Cannot disconnect: the owning event loop is stopped and "
                    "cannot be driven while another loop is running. Call "
                    "disconnect() from synchronous code or close the session "
                    "in its owning loop."
                )
            return

        if owner is None:
            try:
                asyncio.run(self.close())
            except Exception:
                logger.debug("Error while closing session.", exc_info=True)
        elif owner.is_running():
            future = self._schedule_close(owner)
            try:
                future.result(timeout=5.0)
            except Exception:
                logger.warning(
                    "Timed out or failed while closing the HTTP session on its "
                    "owning event loop; the live session was retained for retry.",
                    exc_info=True,
                )
        else:
            try:
                owner.run_until_complete(self.close())
            except Exception:
                logger.warning(
                    "Could not close the HTTP session on its stopped owning "
                    "event loop; retry disconnect() before closing that loop.",
                    exc_info=True,
                )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
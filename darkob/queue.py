"""Queue outgoing messages while the network is down.

Bots lose messages when the connection drops mid-send. A ``SendQueue``
tries immediately, keeps what failed, and flushes once the network is back::

    from darkob import Bot, SendQueue

    bot = Bot(token="...")
    queue = SendQueue(bot, path="outbox.json")

    await queue.put(chat_id, "report ready")   # returns True if sent now

    await queue.flush()                        # retry what is pending

Swapping ``bot.send_message`` for ``queue.put`` is the whole integration.
"""

from __future__ import annotations

import logging
import asyncio
import json
import os
import tempfile
from collections import deque
from typing import Any, Deque, Dict, List, Optional

from .bot.exceptions import Network as BotNetwork
from .client.exceptions import NetworkError
from .metrics import metrics as _metrics
from .utils.concurrency import LazyLock

__all__ = ["SendQueue", "QueueFull"]

#: Errors that mean "try again later" rather than "this message is bad".
TRANSIENT = (BotNetwork, NetworkError, asyncio.TimeoutError, OSError)


logger = logging.getLogger(__name__)

class QueueFull(RuntimeError):
    """Raised when the queue is at capacity and cannot accept more."""


class SendQueue:
    """A durable, bounded outbox for messages that could not be sent."""

    def __init__(
        self,
        bot: Any,
        *,
        path: Optional[str] = None,
        max_size: int = 1000,
        retry_delay: float = 5.0,
    ) -> None:
        if max_size < 1:
            raise ValueError("max_size must be >= 1.")

        self.bot = bot
        self.path = path
        self.max_size = max_size
        self.retry_delay = retry_delay
        self._items: Deque[Dict[str, Any]] = deque(maxlen=None)
        # Lazily, so a SendQueue can be built at import time on Python 3.9.
        self._lock = LazyLock()
        self._worker: Optional[asyncio.Task] = None
        self._stopping = False

        if path:
            self._load()

    # -- persistence ------------------------------------------------------

    def _load(self) -> None:
        if not self.path or not os.path.exists(self.path):
            return
        try:
            with open(self.path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, ValueError):
            return
        if isinstance(data, list):
            for item in data[: self.max_size]:
                if isinstance(item, dict) and item.get("chat_id"):
                    self._items.append(item)

    def _save(self) -> None:
        if not self.path:
            return

        directory = os.path.dirname(os.path.abspath(self.path)) or "."
        os.makedirs(directory, exist_ok=True)
        handle, temp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
        try:
            with os.fdopen(handle, "w", encoding="utf-8") as stream:
                json.dump(list(self._items), stream, ensure_ascii=False)
            os.replace(temp_path, self.path)
        except BaseException:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise

    # -- public api -------------------------------------------------------

    @property
    def pending(self) -> int:
        """How many messages are waiting."""
        return len(self._items)

    def _publish_depth(self) -> None:
        """Keep the ``darkob.queue.pending`` gauge in step with the outbox.

        A growing backlog is the first sign that sends are failing, long
        before the queue overflows — but only if something is watching.
        """
        if _metrics.enabled:
            _metrics.set("darkob.queue.pending", len(self._items))

    async def put(self, chat_id: str, text: Optional[str] = None, **kwargs: Any) -> bool:
        """Send now, or queue if the network is down.

        Returns:
            ``True`` when it was sent immediately, ``False`` when queued.

        Raises:
            QueueFull: When the outbox already holds ``max_size`` messages.
        """
        payload = {"chat_id": chat_id, "text": text, **kwargs}

        try:
            await self.bot.send_message(**payload)
            return True
        except TRANSIENT:
            pass

        async with self._lock:
            if len(self._items) >= self.max_size:
                raise QueueFull(
                    f"Outbox holds {self.max_size} messages; dropping is safer "
                    "than growing without bound."
                )
            self._items.append(payload)
            self._publish_depth()
            self._save()
        return False

    async def flush(self) -> int:
        """Try to send everything queued. Returns how many were delivered."""
        delivered = 0
        changed = False

        async with self._lock:
            while self._items:
                payload = self._items[0]
                try:
                    await self.bot.send_message(**payload)
                except TRANSIENT:
                    break
                except Exception:
                    # Not a network problem: the message itself is bad, so
                    # keeping it would block the queue forever.
                    self._items.popleft()
                    changed = True
                    continue
                else:
                    self._items.popleft()
                    delivered += 1
                    changed = True

            if changed:
                self._publish_depth()
                self._save()

        return delivered

    def drain(self) -> List[Dict[str, Any]]:
        """Remove and return everything queued."""
        items = list(self._items)
        self._items.clear()
        self._publish_depth()
        self._save()
        return items

    # -- background worker ------------------------------------------------

    async def _run(self) -> None:
        while not self._stopping:
            await asyncio.sleep(self.retry_delay)
            try:
                await self.flush()
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.debug("Suppressed exception", exc_info=True)

    def start(self) -> "asyncio.Task":
        """Start a background task that flushes periodically."""
        if self._worker is None or self._worker.done():
            self._stopping = False
            self._worker = asyncio.create_task(self._run())
        return self._worker

    async def stop(self) -> None:
        """Stop the background task (queued items are kept)."""
        self._stopping = True
        worker = self._worker
        self._worker = None
        if worker is not None and not worker.done():
            worker.cancel()
            try:
                await worker
            except asyncio.CancelledError:
                pass

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"SendQueue(pending={len(self._items)}, path={self.path!r})"

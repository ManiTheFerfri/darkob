"""Finite-state machine helpers for multi-step conversations.

A conversation usually needs two things: which step the user is on, and
whatever they already told us. darkob keeps both behind a small storage
interface::

    from darkob import FSMContext, MemoryStorage, StateFilter

    storage = MemoryStorage()

    @bot.on_command("order")
    async def start(bot, event):
        ctx = FSMContext(storage, key=event.chat_id)
        await ctx.set_state("waiting_for_address")
        await bot.send_message(event.chat_id, "What is your address?")

    @bot.on_new_message(StateFilter(storage, "waiting_for_address"))
    async def address(bot, event):
        ctx = FSMContext(storage, key=event.chat_id)
        await ctx.update_data(address=event.text)
        await ctx.set_state(None)
        await bot.send_message(event.chat_id, "Thanks!")

Storage is pluggable: :class:`MemoryStorage` keeps everything in
process, :class:`JsonFileStorage` survives restarts. Implement
:class:`Storage` to back it with Redis or a database.
"""

from __future__ import annotations

import asyncio
import json
import os
import tempfile
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional

from .bot.filters import EventConstraint

__all__ = [
    "Storage",
    "MemoryStorage",
    "JsonFileStorage",
    "FSMContext",
    "StateFilter",
    "default_storage_key",
]


def default_storage_key(event: Any) -> str:
    """Pick a stable per-conversation key from an event.

    Prefers the chat, then the object/sender guid, and falls back to a
    single shared bucket when the event carries none of them.
    """
    for attribute in ("chat_id", "object_guid", "author_object_guid", "sender_id"):
        value = getattr(event, attribute, None)
        if value:
            return str(value)
    return "default"


class Storage(ABC):
    """Minimal async key/value store used by :class:`FSMContext`."""

    @abstractmethod
    async def get_state(self, key: str) -> Optional[str]:
        """Return the state stored for *key*, or ``None``."""

    @abstractmethod
    async def set_state(self, key: str, state: Optional[str]) -> None:
        """Store *state* for *key*; ``None`` clears it."""

    @abstractmethod
    async def get_data(self, key: str) -> Dict[str, Any]:
        """Return the free-form data stored for *key*."""

    @abstractmethod
    async def set_data(self, key: str, data: Dict[str, Any]) -> None:
        """Replace the free-form data stored for *key*."""

    async def clear(self, key: str) -> None:
        """Drop both the state and the data for *key*."""
        await self.set_state(key, None)
        await self.set_data(key, {})

    async def close(self) -> None:
        """Release any resources held by the storage."""


class MemoryStorage(Storage):
    """In-process storage. Fast, but lost when the process exits."""

    def __init__(self) -> None:
        self._states: Dict[str, Optional[str]] = {}
        self._data: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    async def get_state(self, key: str) -> Optional[str]:
        async with self._lock:
            return self._states.get(key)

    async def set_state(self, key: str, state: Optional[str]) -> None:
        async with self._lock:
            if state is None:
                self._states.pop(key, None)
            else:
                self._states[key] = state

    async def get_data(self, key: str) -> Dict[str, Any]:
        async with self._lock:
            return dict(self._data.get(key, {}))

    async def set_data(self, key: str, data: Dict[str, Any]) -> None:
        async with self._lock:
            if data:
                self._data[key] = dict(data)
            else:
                self._data.pop(key, None)

    async def clear(self, key: str) -> None:
        async with self._lock:
            self._states.pop(key, None)
            self._data.pop(key, None)


class JsonFileStorage(Storage):
    """Storage that persists to a JSON file and survives restarts."""

    def __init__(self, path: str = "darkob_fsm.json") -> None:
        self.path = path
        self._lock = asyncio.Lock()
        self._loaded = False
        self._states: Dict[str, str] = {}
        self._data: Dict[str, Dict[str, Any]] = {}

    def _load(self) -> None:
        if self._loaded:
            return
        self._loaded = True

        if not os.path.exists(self.path):
            return

        try:
            with open(self.path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except (OSError, ValueError):
            # A corrupt cache must not prevent the bot from starting.
            return

        if isinstance(payload, dict):
            states = payload.get("states")
            data = payload.get("data")
            if isinstance(states, dict):
                self._states = {
                    str(k): str(v) for k, v in states.items() if v is not None
                }
            if isinstance(data, dict):
                self._data = {
                    str(k): dict(v)
                    for k, v in data.items()
                    if isinstance(v, dict)
                }

    def _flush(self) -> None:
        directory = os.path.dirname(os.path.abspath(self.path)) or "."
        os.makedirs(directory, exist_ok=True)

        payload = {"states": self._states, "data": self._data}
        handle, temp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
        try:
            with os.fdopen(handle, "w", encoding="utf-8") as stream:
                json.dump(payload, stream, ensure_ascii=False)
            os.replace(temp_path, self.path)
        except BaseException:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise

    async def get_state(self, key: str) -> Optional[str]:
        async with self._lock:
            self._load()
            return self._states.get(key)

    async def set_state(self, key: str, state: Optional[str]) -> None:
        async with self._lock:
            self._load()
            if state is None:
                self._states.pop(key, None)
            else:
                self._states[key] = state
            self._flush()

    async def get_data(self, key: str) -> Dict[str, Any]:
        async with self._lock:
            self._load()
            return dict(self._data.get(key, {}))

    async def set_data(self, key: str, data: Dict[str, Any]) -> None:
        async with self._lock:
            self._load()
            if data:
                self._data[key] = dict(data)
            else:
                self._data.pop(key, None)
            self._flush()

    async def clear(self, key: str) -> None:
        async with self._lock:
            self._load()
            self._states.pop(key, None)
            self._data.pop(key, None)
            self._flush()


class FSMContext:
    """State and data for one conversation, bound to a storage and key."""

    __slots__ = ("storage", "key")

    def __init__(self, storage: Storage, key: str) -> None:
        self.storage = storage
        self.key = key

    @classmethod
    def from_event(
        cls,
        storage: Storage,
        event: Any,
        key_func: Optional[Callable[[Any], str]] = None,
    ) -> "FSMContext":
        """Build a context whose key is derived from *event*."""
        resolver = key_func or default_storage_key
        return cls(storage, resolver(event))

    async def get_state(self) -> Optional[str]:
        return await self.storage.get_state(self.key)

    async def set_state(self, state: Optional[str]) -> None:
        await self.storage.set_state(self.key, state)

    async def get_data(self) -> Dict[str, Any]:
        return await self.storage.get_data(self.key)

    async def set_data(self, data: Dict[str, Any]) -> None:
        await self.storage.set_data(self.key, data)

    async def update_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Merge *kwargs* into the stored data and return the result."""
        data = await self.storage.get_data(self.key)
        data.update(kwargs)
        await self.storage.set_data(self.key, data)
        return data

    async def clear(self) -> None:
        await self.storage.clear(self.key)

    def __repr__(self) -> str:
        return f"FSMContext(key={self.key!r})"


class StateFilter(EventConstraint):
    """Matches events whose conversation is currently in a given state."""

    def __init__(
        self,
        storage: Storage,
        state: str,
        key_func: Optional[Callable[[Any], str]] = None,
    ) -> None:
        self.storage = storage
        self.state = state
        self._key_func = key_func or default_storage_key

    async def evaluate(self, event: Any) -> bool:
        key = self._key_func(event)
        return await self.storage.get_state(key) == self.state

    def __repr__(self) -> str:
        return f"StateFilter(state={self.state!r})"

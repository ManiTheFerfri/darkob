"""Track the discovered data-centre layout for drift.

The Messenger protocol discovers its endpoints at runtime. When Rubika
reshuffles them, bots break in confusing ways. A snapshot makes the change
visible instead::

    from darkob import ProtocolTracker

    tracker = ProtocolTracker(path="protocol.json")
    tracker.record(client.connection)
    tracker.diff()      # [] when nothing changed since last time
"""

from __future__ import annotations

import json
import os
import tempfile
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

__all__ = ["ProtocolSnapshot", "ProtocolTracker"]


@dataclass(frozen=True)
class ProtocolSnapshot:
    """The endpoint layout a client discovered."""

    api_url: Optional[str] = None
    wss_url: Optional[str] = None
    api_codes: List[str] = field(default_factory=list)
    platform: Optional[str] = None
    app_version: Optional[str] = None
    captured_at: float = 0.0

    @classmethod
    def capture(cls, connection: Any, client: Any = None) -> "ProtocolSnapshot":
        """Build a snapshot from a live ``Api`` connection."""
        platform_config: Dict[str, Any] = {}
        if client is not None:
            platform_config = getattr(client, "DEFAULT_PLATFORM", {}) or {}

        codes = [
            str(code)
            for code in (getattr(connection, "api_priority", None) or [])
        ]

        return cls(
            api_url=getattr(connection, "api_url", None),
            wss_url=getattr(connection, "wss_url", None),
            api_codes=codes,
            platform=platform_config.get("platform"),
            app_version=platform_config.get("app_version"),
            captured_at=time.time(),
        )


class ProtocolTracker:
    """Keep the last snapshot on disk and report what changed."""

    def __init__(self, path: Optional[str] = None) -> None:
        self.path = path
        self._previous: Optional[ProtocolSnapshot] = None
        if path:
            self._previous = self._load()

    # -- persistence ------------------------------------------------------

    def _load(self) -> Optional[ProtocolSnapshot]:
        if not self.path or not os.path.exists(self.path):
            return None
        try:
            with open(self.path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, ValueError):
            return None
        if not isinstance(data, dict):
            return None

        return ProtocolSnapshot(
            api_url=data.get("api_url"),
            wss_url=data.get("wss_url"),
            api_codes=list(data.get("api_codes") or []),
            platform=data.get("platform"),
            app_version=data.get("app_version"),
            captured_at=float(data.get("captured_at") or 0.0),
        )

    def _save(self, snapshot: ProtocolSnapshot) -> None:
        if not self.path:
            return

        directory = os.path.dirname(os.path.abspath(self.path)) or "."
        os.makedirs(directory, exist_ok=True)
        handle, temp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
        try:
            with os.fdopen(handle, "w", encoding="utf-8") as stream:
                json.dump(asdict(snapshot), stream, ensure_ascii=False)
            os.replace(temp_path, self.path)
        except BaseException:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise

    # -- api --------------------------------------------------------------

    @property
    def previous(self) -> Optional[ProtocolSnapshot]:
        return self._previous

    def diff(self, current: ProtocolSnapshot) -> List[str]:
        """Human-readable differences between the stored and new snapshot."""
        previous = self._previous
        if previous is None:
            return []

        changes: List[str] = []
        for label in ("api_url", "wss_url", "platform", "app_version"):
            before = getattr(previous, label)
            after = getattr(current, label)
            if before != after:
                changes.append(f"{label}: {before!r} -> {after!r}")

        if list(previous.api_codes) != list(current.api_codes):
            changes.append(
                f"api_codes: {previous.api_codes!r} -> {current.api_codes!r}"
            )

        return changes

    def record(self, connection: Any, client: Any = None) -> List[str]:
        """Snapshot ``connection``, store it, and return what changed."""
        current = ProtocolSnapshot.capture(connection, client)
        changes = self.diff(current)
        self._previous = current
        self._save(current)
        return changes

    def __repr__(self) -> str:
        stored = "yes" if self._previous else "no"
        return f"ProtocolTracker(path={self.path!r}, stored={stored})"

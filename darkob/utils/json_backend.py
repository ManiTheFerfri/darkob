"""A fast JSON backend with a standard-library fallback.

Rubika and Shad encrypt stringified JSON inside every ``data_enc`` payload,
so deserialisation sits on the hot path of every update. ``msgspec`` is
several times faster than :mod:`json`; when it is not installed this module
falls back transparently, so the dependency stays optional.
"""

from __future__ import annotations

from typing import Any, Dict, Type, TypeVar

__all__ = ["dumps", "dumps_bytes", "loads", "convert", "BACKEND"]

T = TypeVar("T")

BACKEND = "stdlib"

try:  # pragma: no cover - exercised only when msgspec is installed
    import msgspec

    _encoder = msgspec.json.Encoder()
    _decoder = msgspec.json.Decoder()
    BACKEND = "msgspec"

    def dumps(obj: Any) -> str:
        """Serialise *obj* to a compact JSON string."""
        return _encoder.encode(obj).decode("utf-8")

    def dumps_bytes(obj: Any) -> bytes:
        """Serialise *obj* to UTF-8 JSON bytes without a decode round-trip."""
        return _encoder.encode(obj)

    def loads(data: "str | bytes | bytearray") -> Any:
        """Deserialise JSON from ``str`` or ``bytes``."""
        return _decoder.decode(data)

    def convert(data: Dict[str, Any], cls: Type[T]) -> T:
        """Convert a mapping into a ``msgspec.Struct``/dataclass type."""
        return msgspec.convert(data, type=cls, strict=False)

except ImportError:  # pragma: no cover
    import json

    def dumps(obj: Any) -> str:
        """Serialise *obj* to a compact JSON string."""
        return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)

    def dumps_bytes(obj: Any) -> bytes:
        """Serialise *obj* to UTF-8 JSON bytes."""
        return dumps(obj).encode("utf-8")

    def loads(data: "str | bytes | bytearray") -> Any:
        """Deserialise JSON from ``str`` or ``bytes``."""
        return json.loads(data)

    def _convert_stdlib(data: Dict[str, Any], cls: Type[T]) -> T:
        annotations = getattr(cls, "__annotations__", {})
        return cls(**{key: value for key, value in data.items() if key in annotations})

    convert = _convert_stdlib

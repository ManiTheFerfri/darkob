"""Utilities that keep the core dependency-free."""

from .console import HAS_RICH, Console, Text
from .json_backend import BACKEND, convert, dumps, dumps_bytes, loads
from .media_parser import (
    AudioMetadata,
    ImageMetadata,
    MediaInfo,
    VideoMetadata,
    parse_audio,
    parse_image,
    parse_video,
    probe,
)

__all__ = [
    "Console",
    "Text",
    "HAS_RICH",
    "BACKEND",
    "dumps",
    "dumps_bytes",
    "loads",
    "convert",
    "probe",
    "parse_audio",
    "parse_image",
    "parse_video",
    "AudioMetadata",
    "ImageMetadata",
    "VideoMetadata",
    "MediaInfo",
]

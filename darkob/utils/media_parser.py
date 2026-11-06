"""Zero-dependency binary header parsing for images, audio and video.

Rubika and Shad need a file's duration and dimensions *before* upload.
Reading that used to mean installing `mutagen` and writing the bytes to a
temporary file. This module parses the headers directly, in memory, with
only the standard library::

    from darkob.utils.media_parser import probe

    info = probe(data)
    if info.audio:
        print(info.audio.duration, info.audio.performer)

Supported: PNG, JPEG, GIF, WebP (images); MP3 (audio); MP4 / MOV (video).
Anything unrecognised returns an empty :class:`MediaInfo` rather than
raising — metadata is a nicety, never a reason to fail an upload.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from typing import Optional

__all__ = [
    "AudioMetadata",
    "ImageMetadata",
    "VideoMetadata",
    "MediaInfo",
    "probe",
    "parse_audio",
    "parse_image",
    "parse_video",
]


@dataclass(frozen=True)
class ImageMetadata:
    width: int
    height: int
    format: str


@dataclass(frozen=True)
class AudioMetadata:
    duration: float
    bitrate: Optional[int] = None
    sample_rate: Optional[int] = None
    performer: Optional[str] = None
    title: Optional[str] = None


@dataclass(frozen=True)
class VideoMetadata:
    duration: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None


@dataclass(frozen=True)
class MediaInfo:
    image: Optional[ImageMetadata] = None
    audio: Optional[AudioMetadata] = None
    video: Optional[VideoMetadata] = None
    mime: Optional[str] = None


# --- images --------------------------------------------------------------

def _parse_png(data: bytes) -> Optional[ImageMetadata]:
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    width, height = struct.unpack(">II", data[16:24])
    return ImageMetadata(width, height, "PNG")


def _parse_gif(data: bytes) -> Optional[ImageMetadata]:
    if len(data) < 10 or data[:6] not in (b"GIF87a", b"GIF89a"):
        return None
    width, height = struct.unpack("<HH", data[6:10])
    return ImageMetadata(width, height, "GIF")


def _parse_webp(data: bytes) -> Optional[ImageMetadata]:
    if len(data) < 30 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    chunk = data[12:16]
    if chunk == b"VP8X":
        width = 1 + int.from_bytes(data[24:27], "little")
        height = 1 + int.from_bytes(data[27:30], "little")
        return ImageMetadata(width, height, "WebP")
    if chunk == b"VP8 ":
        width = int.from_bytes(data[26:28], "little") & 0x3FFF
        height = int.from_bytes(data[28:30], "little") & 0x3FFF
        return ImageMetadata(width, height, "WebP")
    if chunk == b"VP8L":
        bits = int.from_bytes(data[21:25], "little")
        width = (bits & 0x3FFF) + 1
        height = ((bits >> 14) & 0x3FFF) + 1
        return ImageMetadata(width, height, "WebP")
    return None


# Frame markers that carry dimensions; 0xC4/0xC8/0xCC are not SOF markers.
_JPEG_SOF = {
    0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
    0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
}


def _parse_jpeg(data: bytes) -> Optional[ImageMetadata]:
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        return None

    index = 2
    length = len(data)
    while index + 9 < length:
        if data[index] != 0xFF:
            index += 1
            continue

        marker = data[index + 1]
        index += 2

        # Standalone markers carry no length field.
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7 or marker == 0x01:
            continue

        if index + 2 > length:
            return None
        segment_length = struct.unpack(">H", data[index : index + 2])[0]

        if marker in _JPEG_SOF:
            if index + 7 > length:
                return None
            height, width = struct.unpack(">HH", data[index + 3 : index + 7])
            return ImageMetadata(width, height, "JPEG")

        if segment_length < 2:
            return None
        index += segment_length

    return None


# --- audio (MP3) ---------------------------------------------------------

_MP3_BITRATES = {
    ("1", 3): (0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320),
    ("1", 2): (0, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384),
    ("2", 3): (0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160),
}
_MP3_RATES = {
    "1": (44100, 48000, 32000),
    "2": (22050, 24000, 16000),
    "2.5": (11025, 12000, 8000),
}
_MP3_SAMPLES_PER_FRAME = {"1": 1152, "2": 576, "2.5": 576}


def _id3v2_size(data: bytes) -> int:
    """Total bytes occupied by an ID3v2 tag at the start of *data*."""
    if len(data) < 10 or data[:3] != b"ID3":
        return 0
    size_bytes = data[6:10]
    if any(byte & 0x80 for byte in size_bytes):  # not synchsafe; unusable
        return 0
    size = (size_bytes[0] << 21) | (size_bytes[1] << 14) | (size_bytes[2] << 7) | size_bytes[3]
    footer = 10 if (data[5] & 0x10) else 0
    return 10 + size + footer


def _id3_text_frame(data: bytes, frame_id: bytes) -> Optional[str]:
    index = data.find(frame_id)
    if index < 0 or index + 10 > len(data):
        return None

    size_bytes = data[index + 4 : index + 8]
    if any(byte & 0x80 for byte in size_bytes):
        return None
    size = (size_bytes[0] << 21) | (size_bytes[1] << 14) | (size_bytes[2] << 7) | size_bytes[3]
    if size <= 0 or index + 10 + size > len(data):
        return None

    payload = data[index + 10 : index + 10 + size]
    if not payload:
        return None

    encoding = payload[0]
    body = payload[1:]
    if encoding in (0, 3):
        text = body.decode("latin-1" if encoding == 0 else "utf-8", errors="ignore")
    elif encoding == 1:
        text = body.decode("utf-16", errors="ignore")
    else:
        text = body.decode("utf-16-be", errors="ignore")

    return text.strip("\x00 ").strip() or None


def _id3v1_artist(data: bytes) -> Optional[str]:
    if len(data) < 128 or data[-128:-125] != b"TAG":
        return None
    artist = data[-128 + 33 : -128 + 63].strip(b"\x00 ").decode("latin-1", "ignore").strip()
    return artist or None


def parse_audio(data: bytes) -> Optional[AudioMetadata]:
    """Parse MP3 header information without loading a decoder."""
    if len(data) < 4:
        return None

    tag_size = _id3v2_size(data)
    performer = _id3_text_frame(data, b"TPE1") or _id3v1_artist(data)
    title = _id3_text_frame(data, b"TIT2")

    index = tag_size
    length = len(data)
    frame = None

    while index + 4 <= length:
        if data[index] == 0xFF and (data[index + 1] & 0xE0) == 0xE0:
            header = data[index : index + 4]
            version_bits = (header[1] >> 3) & 0x03
            layer_bits = (header[1] >> 1) & 0x03
            bitrate_index = (header[2] >> 4) & 0x0F
            rate_index = (header[2] >> 2) & 0x03

            if layer_bits == 0x01 and version_bits != 0x01 and bitrate_index not in (0, 15) and rate_index != 3:
                version = {0: "2.5", 2: "2", 3: "1"}[version_bits]
                frame = (index, version, bitrate_index, rate_index)
                break
        index += 1

    if frame is None:
        return AudioMetadata(duration=0.0, performer=performer, title=title)

    start, version, bitrate_index, rate_index = frame
    table = _MP3_BITRATES.get((version, 3)) or _MP3_BITRATES[("2", 3)]
    bitrate = table[bitrate_index] * 1000
    sample_rate = _MP3_RATES[version][rate_index]
    samples_per_frame = _MP3_SAMPLES_PER_FRAME[version]

    duration = 0.0

    # Xing/Info or VBRI headers carry the exact frame count (VBR files).
    side_info = 32 if version == "1" else 17
    xing = data.find(b"Xing", start, start + 200) if length - start > 200 else -1
    if xing < 0:
        xing = data.find(b"Info", start, min(length, start + 200))
    if xing >= 0 and xing + 12 <= length:
        flags = struct.unpack(">I", data[xing + 4 : xing + 8])[0]
        if flags & 0x1:
            frames = struct.unpack(">I", data[xing + 8 : xing + 12])[0]
            duration = frames * samples_per_frame / sample_rate

    if duration <= 0 and bitrate:
        # Constant bitrate: audio payload size over bitrate.
        payload = max(0, length - tag_size)
        duration = payload * 8 / bitrate

    return AudioMetadata(
        duration=round(duration, 3),
        bitrate=bitrate or None,
        sample_rate=sample_rate,
        performer=performer,
        title=title,
    )


# --- video (MP4 family) --------------------------------------------------

def _iter_atoms(data: bytes, start: int, end: int):
    index = start
    while index + 8 <= end:
        size = struct.unpack(">I", data[index : index + 4])[0]
        kind = data[index + 4 : index + 8]
        header = 8
        if size == 1 and index + 16 <= end:
            size = struct.unpack(">Q", data[index + 8 : index + 16])[0]
            header = 16
        elif size == 0:
            size = end - index

        if size < header or index + size > end:
            return
        yield kind, index + header, index + size
        index += size


def _mvhd_duration(data: bytes, start: int, end: int) -> Optional[float]:
    if start + 4 > end:
        return None
    version = data[start]
    if version == 1:
        if start + 32 > end:
            return None
        timescale, duration = struct.unpack(">IQ", data[start + 20 : start + 32])
    else:
        if start + 20 > end:
            return None
        timescale, duration = struct.unpack(">II", data[start + 12 : start + 20])
    if not timescale:
        return None
    return duration / timescale


def _tkhd_size(data: bytes, start: int, end: int) -> Optional[tuple]:
    if start + 4 > end:
        return None
    version = data[start]
    offset = start + (88 if version == 1 else 76)
    if offset + 8 > end:
        return None
    width_fixed, height_fixed = struct.unpack(">II", data[offset : offset + 8])
    width = width_fixed >> 16
    height = height_fixed >> 16
    if width and height:
        return width, height
    return None


def parse_video(data: bytes) -> Optional[VideoMetadata]:
    """Parse MP4/MOV duration and dimensions by walking ISO BMFF atoms."""
    if len(data) < 12 or data[4:8] not in (b"ftyp", b"moov", b"mdat", b"free"):
        return None

    duration: Optional[float] = None
    dimensions: Optional[tuple] = None

    for kind, start, end in _iter_atoms(data, 0, len(data)):
        if kind != b"moov":
            continue
        for child, child_start, child_end in _iter_atoms(data, start, end):
            if child == b"mvhd":
                duration = _mvhd_duration(data, child_start, child_end)
            elif child == b"tkhd":
                # Some muxers place tkhd directly under moov.
                dimensions = _tkhd_size(data, child_start, child_end) or dimensions
            elif child == b"trak":
                for leaf, leaf_start, leaf_end in _iter_atoms(data, child_start, child_end):
                    if leaf == b"tkhd":
                        dimensions = _tkhd_size(data, leaf_start, leaf_end) or dimensions
        break

    if duration is None and dimensions is None:
        return None
    return VideoMetadata(
        duration=round(duration, 3) if duration else None,
        width=dimensions[0] if dimensions else None,
        height=dimensions[1] if dimensions else None,
    )


# --- entry point ---------------------------------------------------------

def probe(data: bytes) -> MediaInfo:
    """Identify *data* and parse whatever metadata its header exposes."""
    if not data:
        return MediaInfo()

    image = _parse_png(data) or _parse_jpeg(data) or _parse_gif(data) or _parse_webp(data)
    if image is not None:
        return MediaInfo(image=image, mime=f"image/{image.format.lower()}")

    video = parse_video(data)
    if video is not None:
        return MediaInfo(video=video, mime="video/mp4")

    audio = parse_audio(data)
    if audio is not None and (audio.duration or audio.performer or audio.title):
        return MediaInfo(audio=audio, mime="audio/mpeg")

    return MediaInfo()


def parse_image(data: bytes) -> Optional[ImageMetadata]:
    """Parse image dimensions, or ``None`` when the format is unknown."""
    return _parse_png(data) or _parse_jpeg(data) or _parse_gif(data) or _parse_webp(data)

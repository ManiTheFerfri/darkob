"""Tests for the zero-dependency media header parser."""

from __future__ import annotations

import struct

import pytest

from darkob.utils.media_parser import (
    parse_audio,
    parse_image,
    parse_video,
    probe,
)


# ---------------------------------------------------------------------------
# Fixtures: minimal but structurally valid headers
# ---------------------------------------------------------------------------


def png_bytes(width: int, height: int) -> bytes:
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr_length = struct.pack(">I", 13)
    ihdr = b"IHDR" + struct.pack(">II", width, height) + b"\x08\x06\x00\x00\x00"
    return signature + ihdr_length + ihdr + b"\x00" * 32


def jpeg_bytes(width: int, height: int) -> bytes:
    # SOI, then an APP0 segment, then SOF0 carrying the dimensions.
    app0 = b"\xff\xe0" + struct.pack(">H", 16) + b"JFIF\x00\x01\x01\x00" + b"\x00" * 6
    sof0 = b"\xff\xc0" + struct.pack(">H", 17) + b"\x08" + struct.pack(">HH", height, width) + b"\x03" * 9
    return b"\xff\xd8" + app0 + sof0 + b"\xff\xd9"


def gif_bytes(width: int, height: int) -> bytes:
    return b"GIF89a" + struct.pack("<HH", width, height) + b"\x00" * 8


def mp4_bytes(duration_seconds: float = 12.5, width: int = 640, height: int = 480) -> bytes:
    """A minimal MP4: one ``mvhd`` (timing) and one ``tkhd`` (dimensions).

    Every atom is ``[uint32 size][4-byte type][payload]``.
    """
    timescale = 1000
    duration = int(duration_seconds * timescale)

    mvhd_payload = bytearray(100)
    # version/flags(4) creation(4) modification(4) timescale(4) duration(4)
    struct.pack_into(">II", mvhd_payload, 12, timescale, duration)
    mvhd = struct.pack(">I", 8 + len(mvhd_payload)) + b"mvhd" + bytes(mvhd_payload)

    tkhd_payload = bytearray(92)
    # width and height are 16.16 fixed point at payload offset 76 (version 0)
    struct.pack_into(">II", tkhd_payload, 76, width << 16, height << 16)
    tkhd = struct.pack(">I", 8 + len(tkhd_payload)) + b"tkhd" + bytes(tkhd_payload)

    trak = struct.pack(">I", 8 + len(tkhd)) + b"trak" + tkhd
    body = mvhd + trak
    moov = struct.pack(">I", 8 + len(body)) + b"moov" + body
    ftyp = struct.pack(">I", 16) + b"ftyp" + b"isom" + b"\x00" * 4
    return ftyp + moov


def mp3_bytes(duration_frames: int = 100) -> bytes:
    """A single MPEG1 Layer III frame header plus a Xing frame count."""
    header = bytes([0xFF, 0xFB, 0x90, 0x00])  # MPEG1 L3, 128kbps, 44100Hz
    xing = b"Xing" + struct.pack(">I", 0x1) + struct.pack(">I", duration_frames)
    return header + xing + b"\x00" * (417 - 12)


# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------


def test_png_dimensions():
    info = parse_image(png_bytes(1920, 1080))

    assert (info.width, info.height, info.format) == (1920, 1080, "PNG")


def test_jpeg_dimensions():
    info = parse_image(jpeg_bytes(800, 600))

    assert (info.width, info.height, info.format) == (800, 600, "JPEG")


def test_gif_dimensions():
    info = parse_image(gif_bytes(64, 32))

    assert (info.width, info.height, info.format) == (64, 32, "GIF")


def test_unknown_image_returns_none():
    assert parse_image(b"not an image at all") is None


def test_truncated_png_is_safe():
    assert parse_image(png_bytes(10, 10)[:12]) is None


# ---------------------------------------------------------------------------
# Audio
# ---------------------------------------------------------------------------


def test_mp3_duration_from_xing_header():
    info = parse_audio(mp3_bytes(100))

    assert info is not None
    assert info.duration == pytest.approx(100 * 1152 / 44100, rel=1e-3)
    assert info.sample_rate == 44100
    assert info.bitrate == 128000


def test_mp3_without_frames_returns_zero_duration():
    info = parse_audio(b"\x00" * 128)

    assert info is not None
    assert info.duration == 0.0


def test_mp3_skips_an_id3v2_tag():
    tag = b"ID3\x04\x00\x00" + bytes([0, 0, 0x02, 0x00]) + b"\x00" * 256
    info = parse_audio(tag + mp3_bytes(50))

    assert info is not None
    assert info.duration > 0


def test_mp3_reads_the_artist_frame():
    frame_body = b"\x00" + b"Ada Lovelace"
    frame = b"TPE1" + bytes([0, 0, 0, len(frame_body)]) + b"\x00\x00" + frame_body
    tag = b"ID3\x03\x00\x00" + bytes([0, 0, 0x02, 0x00]) + b"\x00" * (256 - len(frame)) + frame

    info = parse_audio(tag + mp3_bytes(10))

    assert info.performer == "Ada Lovelace"


# ---------------------------------------------------------------------------
# Video
# ---------------------------------------------------------------------------


def test_mp4_duration_and_dimensions():
    info = parse_video(mp4_bytes(12.5, 640, 480))

    assert info is not None
    assert info.duration == pytest.approx(12.5, rel=1e-3)
    assert (info.width, info.height) == (640, 480)


def test_mp4_garbage_is_safe():
    # An empty moov carries no timing or dimensions.
    assert parse_video(b"\x00\x00\x00\x08moov") is None
    assert parse_video(b"definitely not a video") is None


# ---------------------------------------------------------------------------
# probe()
# ---------------------------------------------------------------------------


def test_probe_detects_an_image():
    info = probe(png_bytes(10, 20))

    assert info.image is not None
    assert info.mime == "image/png"


def test_probe_detects_video():
    info = probe(mp4_bytes())

    assert info.video is not None
    assert info.mime == "video/mp4"


def test_probe_of_empty_data_is_empty():
    info = probe(b"")

    assert info.image is None and info.audio is None and info.video is None


def test_probe_never_raises_on_random_bytes():
    for payload in (b"\x00", b"\xff" * 64, bytes(range(256))):
        probe(payload)  # must not raise

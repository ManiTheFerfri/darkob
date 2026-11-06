"""Reproducible comparison between darkob and maxrubika.

    python benchmarks/benchmark_suite.py            # prints a Markdown table
    python benchmarks/benchmark_suite.py --json     # machine-readable

Measures cold import time, payload deserialization, retained memory and
media metadata extraction. Runs entirely offline; any competitor that is
not installed is reported as "n/a" rather than guessed at.
"""

from __future__ import annotations

import argparse
import gc
import json
import subprocess
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

ITERATIONS = 10_000
HELD_OBJECTS = 5_000

UPDATE_PAYLOAD: Dict[str, Any] = {
    "type": "NewMessage",
    "chat_id": "b0" + "a" * 30,
    "new_message": {
        "message_id": "1234567890123456789",
        "text": "hello world",
        "time": "1793880483",
        "is_edited": False,
        "sender_type": "User",
        "sender_id": "u0" + "b" * 30,
        "chat": {"chat_id": "b0" + "a" * 30, "chat_type": "User"},
        "file_inline": {"file_id": "f" * 40, "size": 1024, "type": "Image"},
    },
}


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def best_of(func: Callable[[], Any], repeats: int = 3) -> float:
    """Best wall-clock time of *repeats* runs, in seconds."""
    timings = []
    for _ in range(repeats):
        gc.collect()
        started = time.perf_counter()
        func()
        timings.append(time.perf_counter() - started)
    return min(timings)


def cold_import(module: str) -> Optional[float]:
    """Import time measured in a fresh interpreter."""
    code = f"import {module}"
    timings = []
    for _ in range(3):
        started = time.perf_counter()
        result = subprocess.run(
            [sys.executable, "-c", code], capture_output=True, cwd=REPO_ROOT
        )
        if result.returncode != 0:
            return None
        timings.append(time.perf_counter() - started)
    return min(timings)


def deserialize_loop(factory: Callable[[dict], Any], iterations: int = ITERATIONS) -> float:
    payload = UPDATE_PAYLOAD

    def run() -> None:
        for _ in range(iterations):
            factory(payload)

    return best_of(run)


def retained_memory(factory: Callable[[dict], Any], count: int = HELD_OBJECTS) -> int:
    gc.collect()
    tracemalloc.start()
    try:
        held = [factory(UPDATE_PAYLOAD) for _ in range(count)]
        current, _peak = tracemalloc.get_traced_memory()
        assert len(held) == count
        return current
    finally:
        tracemalloc.stop()


def lookup_loop(factory: Callable[[dict], Any], iterations: int = ITERATIONS) -> float:
    """Repeatedly read a nested key from one instance."""
    instance = factory(UPDATE_PAYLOAD)

    def run() -> None:
        for _ in range(iterations):
            instance.find_keys("text")

    return best_of(run)

def media_parse_seconds(parse: Callable[[], Any], iterations: int = 2_000) -> float:
    def run() -> None:
        for _ in range(iterations):
            parse()

    return best_of(run)


# ---------------------------------------------------------------------------
# contenders
# ---------------------------------------------------------------------------


def darkob_contenders() -> Dict[str, Any]:
    from darkob.data import Data
    from darkob.utils.media_parser import parse_image

    png = b"\x89PNG\r\n\x1a\n" + (13).to_bytes(4, "big") + b"IHDR" + (800).to_bytes(
        4, "big"
    ) + (600).to_bytes(4, "big") + b"\x08\x06\x00\x00\x00" + b"\x00" * 32

    return {
        "available": True,
        "import": "darkob",
        "deserialize": lambda payload: Data(payload),
        "media": lambda: parse_image(png),
        "media_label": "media header (in-memory)",
    }


def maxrubika_contenders() -> Optional[Dict[str, Any]]:
    try:
        import maxrubika
        from maxrubika.data import Data
        from maxrubika.client.core.media import MediaThumbnail
    except Exception:
        return None

    png = b"\x89PNG\r\n\x1a\n" + (13).to_bytes(4, "big") + b"IHDR" + (800).to_bytes(
        4, "big"
    ) + (600).to_bytes(4, "big") + b"\x08\x06\x00\x00\x00" + b"\x00" * 32

    def media_via_mutagen() -> Any:
        # maxrubika has no in-memory parser; the fair equivalent is the
        # image path it uses, which shells out to PIL/mutagen helpers.
        return MediaThumbnail.from_image(png)

    return {
        "available": True,
        "import": "maxrubika",
        "deserialize": lambda payload: Data(payload),
        "media": media_via_mutagen,
        "media_label": "image metadata (library helper)",
        "version": maxrubika.__version__,
    }


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------


def markdown_table(rows: List[Dict[str, Any]]) -> str:
    lines = [
        "| Benchmark | darkob | maxrubika | Difference |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['name']} | {row['ours']} | {row['theirs']} | {row['delta']} |"
        )
    return "\n".join(lines)


def fmt_seconds(value: Optional[float]) -> str:
    if value is None:
        return "n/a"
    if value < 0.001:
        return f"{value * 1e6:.0f} µs"
    if value < 1:
        return f"{value * 1000:.1f} ms"
    return f"{value:.3f} s"


def fmt_bytes(value: int) -> str:
    return f"{value / 1024:.0f} KB"


def ratio(ours: Optional[float], theirs: Optional[float]) -> str:
    if not ours or not theirs:
        return "n/a"
    factor = theirs / ours
    if 0.95 <= factor <= 1.05:
        return "comparable"
    return f"{factor:.1f}x {'faster' if factor > 1 else 'slower'}"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON instead")
    args = parser.parse_args(argv)

    ours = darkob_contenders()
    theirs = maxrubika_contenders()

    rows: List[Dict[str, Any]] = []

    our_import = cold_import(ours["import"])
    their_import = cold_import(theirs["import"]) if theirs else None
    rows.append(
        {
            "name": "Cold import",
            "ours": fmt_seconds(our_import),
            "theirs": fmt_seconds(their_import),
            "delta": ratio(our_import, their_import),
        }
    )

    our_deser = deserialize_loop(ours["deserialize"])
    their_deser = deserialize_loop(theirs["deserialize"]) if theirs else None
    rows.append(
        {
            "name": f"Deserialize {ITERATIONS:,} updates",
            "ours": fmt_seconds(our_deser),
            "theirs": fmt_seconds(their_deser),
            "delta": ratio(our_deser, their_deser),
        }
    )

    our_lookup = lookup_loop(ours["deserialize"])
    their_lookup = lookup_loop(theirs["deserialize"]) if theirs else None
    rows.append(
        {
            "name": f"Nested key lookup x{ITERATIONS:,}",
            "ours": fmt_seconds(our_lookup),
            "theirs": fmt_seconds(their_lookup),
            "delta": ratio(our_lookup, their_lookup),
        }
    )

    our_mem = retained_memory(ours["deserialize"])
    their_mem = retained_memory(theirs["deserialize"]) if theirs else None
    rows.append(
        {
            "name": f"Retained memory, {HELD_OBJECTS:,} objects",
            "ours": fmt_bytes(our_mem),
            "theirs": fmt_bytes(their_mem) if their_mem else "n/a",
            "delta": ratio(float(our_mem), float(their_mem) if their_mem else None),
        }
    )

    our_media = media_parse_seconds(ours["media"])
    their_media: Optional[float] = None
    their_media_label = "n/a"

    if theirs is not None:
        import warnings

        rival_works = False
        try:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                result = theirs["media"]()
            # A fallback (string) result or any warning means it could not
            # parse, so timing it would only measure exception overhead.
            rival_works = not caught and not isinstance(result, str)
        except Exception:
            rival_works = False

        if rival_works:
            their_media = media_parse_seconds(theirs["media"], iterations=200)
            their_media_label = theirs["media_label"]
        else:
            their_media_label = "n/a (rival has no working parser here)"

    rows.append(
        {
            "name": "Media metadata (image header)",
            "ours": fmt_seconds(our_media),
            "theirs": fmt_seconds(their_media) if their_media else "n/a",
            "delta": ratio(our_media, their_media) if their_media else "n/a",
        }
    )

    if args.json:
        print(json.dumps({"rows": rows, "payload": UPDATE_PAYLOAD}, indent=2))
    else:
        print(markdown_table(rows))
        if theirs is None:
            print("\n_maxrubika is not installed; competitor column is n/a._")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""End-to-end scenario benchmarks: darkob measured under realistic load.

    python benchmarks/scenarios.py            # human-readable table
    python benchmarks/scenarios.py --json     # raw numbers

Each scenario runs in its own interpreter so a previous case cannot leave
caches warm. Nothing touches the network: the transport is an in-memory fake
that implements HTTP range requests, so what is measured is darkob's own
work — routing, queueing, chunked writing, filtering, decoding — with the
variable part (the network) held constant.

Why the numbers are reported as a *ratio*
-----------------------------------------

Absolute milliseconds are meaningless across machines: a CI runner and a
laptop differ by 3× on identical code. So every run also measures a fixed
calibration workload (a pure-integer loop, no allocation), and each case is
reported as ``seconds / calibration`` as well as in seconds. The ratio is
what :mod:`benchmarks.check_regression` compares, which makes the regression
gate portable instead of only meaningful on the machine that produced the
baseline.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

#: Matches ``Bot.TOKEN_PATTERN``; never used for network access.
FAKE_TOKEN = "ABCDE" + "0" * 59

#: A realistic ``new_message`` update, the shape every bot handles.
PAYLOAD: Dict[str, Any] = {
    "type": "NewMessage",
    "chat_id": "b0" + "a" * 30,
    "new_message": {
        "message_id": "1789000000000000000",
        "text": "/start please",
        "time": "1793880483",
        "is_edited": False,
        "sender_type": "User",
        "sender_id": "u0" + "b" * 30,
        "chat": {"chat_id": "b0" + "a" * 30, "chat_type": "User"},
    },
}


# ---------------------------------------------------------------------------
# machine-independent calibration
# ---------------------------------------------------------------------------


def calibration() -> float:
    """A fixed, allocation-free CPU workload used to normalise the results.

    Deliberately integer-only and branch-simple: it should scale with raw
    single-thread speed and nothing else.
    """
    started = time.perf_counter()
    total = 0
    for index in range(300_000):
        total += (index * 7) % 13
    elapsed = time.perf_counter() - started
    if total < 0:  # pragma: no cover - keeps the loop from being optimised out
        raise AssertionError
    return elapsed


# ---------------------------------------------------------------------------
# fakes
# ---------------------------------------------------------------------------


class _Chunks:
    """Async-iterable body, mirroring aiohttp's ``content.iter_chunked``."""

    def __init__(self, data: bytes) -> None:
        self._data = data

    async def iter_chunked(self, size: int):
        for offset in range(0, len(self._data), size):
            yield self._data[offset : offset + size]


class _RangedResponse:
    """A response that understands ``Range`` the way a file server does."""

    def __init__(self, body: bytes, start: int) -> None:
        self.status = 206 if start else 200
        self.headers = {"Content-Length": str(len(body))}
        self.content = _Chunks(body)

    async def __aenter__(self) -> "_RangedResponse":
        return self

    async def __aexit__(self, *exc_info: Any) -> bool:
        return False


class _RangedSession:
    """In-memory transport with resume support."""

    def __init__(self, blob: bytes) -> None:
        self.blob = blob
        self.requests = 0

    def get(self, url: str, headers: Any = None, proxy: Any = None):
        """Synchronous method returning an async context manager, like aiohttp."""
        self.requests += 1
        start = 0
        header = (headers or {}).get("Range")
        if header:
            start = int(header.split("=", 1)[1].split("-", 1)[0])
        return _RangedResponse(self.blob[start:], start)

    async def close(self) -> None:
        return None


class _OkBot:
    """A bot whose sends always succeed instantly."""

    def __init__(self) -> None:
        self.sent = 0

    async def send_message(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        self.sent += 1
        return {"status": "OK"}


# ---------------------------------------------------------------------------
# scenarios
# ---------------------------------------------------------------------------


def scenario_dispatch(updates: int = 1000, handlers: int = 100) -> float:
    """Handle *updates* updates with *handlers* registered handlers.

    None of the handlers match, so this is the routing cost every bot pays
    for every update: build an event, run each filter, move on.
    """
    from darkob.client.core.api import Api

    async def run() -> float:
        # Api opens an aiohttp session, so it must be built inside the loop.
        client = SimpleNamespace(
            DEFAULT_PLATFORM={"platform": "PWA"},
            _original_platform="pwa",
            user_agent="bench",
            max_retries=1,
            timeout=5,
            verify_ssl=False,
            proxy=None,
            stop_on_first_match=False,
            handlers={},
            _conversations=None,
            plugin_manager=None,
        )

        class MessageUpdates:
            __name__ = "MessageUpdates"

            async def __call__(self, event: Any = None) -> bool:
                return False

        # Handlers are keyed by the function object, so each one must be a
        # distinct function or the dict would collapse to a single entry.
        registry: Dict[Any, Any] = {}
        for index in range(handlers):
            async def handler(event: Any = None, _index: int = index) -> None:
                return None

            registry[handler] = MessageUpdates()

        client.handlers = registry
        api = Api(client)

        started = time.perf_counter()
        for _ in range(updates):
            await api.handle_update("message_updates", dict(PAYLOAD))
        elapsed = time.perf_counter() - started
        await api.close()
        return elapsed

    return asyncio.run(run())


def scenario_sendqueue(messages: int = 100) -> float:
    """Push *messages* messages through ``SendQueue`` (success path)."""
    from darkob.queue import SendQueue

    async def run() -> float:
        queue = SendQueue(_OkBot())
        started = time.perf_counter()
        for index in range(messages):
            await queue.put(f"chat{index % 10}", f"message {index}")
        return time.perf_counter() - started

    return asyncio.run(run())


def scenario_resume_download(size_mb: int = 4) -> float:
    """Resume a half-finished *size_mb* MiB download and finish it.

    Measures the resumable-write path only: range header, append mode and the
    chunked copy loop. The bytes come from memory, so this is the library's
    overhead rather than network throughput.
    """
    from darkob import Bot

    directory = tempfile.mkdtemp(prefix="darkob-bench-")
    target = os.path.join(directory, "payload.bin")
    try:
        blob = b"x" * (size_mb * 1024 * 1024)
        with open(target, "wb") as handle:  # simulate an interrupted download
            handle.write(blob[: len(blob) // 2])

        session = _RangedSession(blob)
        bot = Bot(token=FAKE_TOKEN, show_welcome=False)

        async def _get_session():
            return session

        bot._get_session = _get_session  # type: ignore[method-assign]

        async def run() -> float:
            started = time.perf_counter()
            written = await bot._download_to_path(  # type: ignore[attr-defined]
                "https://files.test/payload.bin", target, resume=True
            )
            elapsed = time.perf_counter() - started
            if written != len(blob):
                raise AssertionError(f"resumed to {written}, expected {len(blob)}")
            return elapsed

        return asyncio.run(run())
    finally:
        shutil.rmtree(directory, ignore_errors=True)


def scenario_filters(events: int = 2000, filters: int = 5) -> float:
    """Evaluate *filters* text filters against *events* events."""
    import importlib

    filters_module = importlib.import_module("darkob.bot.filters")
    event_module = importlib.import_module("darkob.types.event")
    event = event_module.Event({"message": {"text": "/start please"}})
    chain = [filters_module.Text("please") for _ in range(filters)]

    async def run() -> float:
        started = time.perf_counter()
        for _ in range(events):
            for check in chain:
                await check.evaluate(event)
        return time.perf_counter() - started

    return asyncio.run(run())


def scenario_json_decode(count: int = 5000) -> float:
    """Decode a realistic update payload *count* times."""
    from darkob.utils import dumps, loads

    encoded = dumps(PAYLOAD)

    started = time.perf_counter()
    for _ in range(count):
        loads(encoded)
    return time.perf_counter() - started


SCENARIOS: List[Dict[str, Any]] = [
    {
        "key": "dispatch_1000x100",
        "label": "1,000 updates × 100 handlers",
        "unit": "updates",
        "count": 1000,
        "fn": lambda: scenario_dispatch(),
    },
    {
        "key": "sendqueue_100",
        "label": "100 messages through SendQueue",
        "unit": "messages",
        "count": 100,
        "fn": lambda: scenario_sendqueue(),
    },
    {
        "key": "resume_download_4mb",
        "label": "Resume a 4 MiB download from 50%",
        "unit": "MiB",
        "count": 4,
        "fn": lambda: scenario_resume_download(),
    },
    {
        "key": "filters_2000x5",
        "label": "2,000 events × 5 filters",
        "unit": "events",
        "count": 2000,
        "fn": lambda: scenario_filters(),
    },
    {
        "key": "json_5000",
        "label": "Decode 5,000 update payloads",
        "unit": "payloads",
        "count": 5000,
        "fn": lambda: scenario_json_decode(),
    },
]

SCENARIO_BY_KEY = {scenario["key"]: scenario for scenario in SCENARIOS}


def run_in_process(key: str, repeats: int = 3) -> Dict[str, Any]:
    """Measure one scenario *repeats* times and keep the best run."""
    scenario = SCENARIO_BY_KEY[key]
    best = min(scenario["fn"]() for _ in range(repeats))
    baseline = min(calibration() for _ in range(repeats))
    return {
        "seconds": best,
        "calibration": baseline,
        "ratio": best / baseline if baseline else 0.0,
        "throughput": scenario["count"] / best if best else 0.0,
        "unit": scenario["unit"],
        "count": scenario["count"],
    }


def measure_one(key: str) -> Optional[Dict[str, Any]]:
    """Measure one scenario in a fresh interpreter."""
    code = (
        "import json,sys;"
        f"sys.path.insert(0, {str(REPO_ROOT)!r});"
        "import benchmarks.scenarios as s;"
        f"print(json.dumps(s.run_in_process({key!r})))"
    )
    try:
        result = subprocess.run(
            [sys.executable, "-W", "ignore", "-c", code],
            capture_output=True,
            text=True,
            timeout=600,
        )
    except subprocess.TimeoutExpired:
        return None
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return None


def environment() -> Dict[str, Any]:
    """Everything a reader needs to judge whether the numbers apply to them."""
    import platform

    import darkob

    try:
        import maxrubika

        rival = getattr(maxrubika, "__version__", "unknown")
    except Exception:  # pragma: no cover - optional competitor
        rival = None

    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor() or "unknown",
        "cpu_count": os.cpu_count(),
        "darkob": darkob.__version__,
        "maxrubika": rival,
    }


def human(seconds: Optional[float], throughput: Optional[float], unit: str) -> str:
    if seconds is None:
        return "failed"
    return f"{seconds * 1000:.1f} ms · {throughput:,.0f} {unit}/s"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--key", help="measure only this scenario")
    args = parser.parse_args(argv)

    keys = [args.key] if args.key else [item["key"] for item in SCENARIOS]
    results = {key: measure_one(key) for key in keys}

    if args.json:
        print(json.dumps({"environment": environment(), "cases": results}, indent=2))
        return 0

    print("| Scenario | Time | Throughput |")
    print("| --- | --- | --- |")
    for scenario in SCENARIOS:
        if scenario["key"] not in results:
            continue
        measured = results[scenario["key"]]
        if measured is None:
            print(f"| {scenario['label']} | failed | — |")
            continue
        row = human(
            measured["seconds"], measured["throughput"], measured["unit"]
        )
        time_part, throughput_part = row.split(" · ", 1)
        print(f"| {scenario['label']} | {time_part} | {throughput_part} |")

    print()
    for name, value in environment().items():
        print(f"<!-- {name}: {value} -->")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

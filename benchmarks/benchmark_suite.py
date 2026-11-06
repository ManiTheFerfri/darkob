"""Head-to-head benchmark: darkob vs maxrubika on hot paths.

    python benchmarks/benchmark_suite.py           # Markdown table
    python benchmarks/benchmark_suite.py --json    # raw numbers

Only workloads where the two libraries do the same job are measured, and
each runs in a fresh process so neither benefits from the other's warm
state. A competitor that is not installed is reported as ``n/a``.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

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
# individual measurements (run inside one subprocess)
# ---------------------------------------------------------------------------


def _best(fn: Callable[[], Any], repeats: int = 3) -> float:
    timings = []
    for _ in range(repeats):
        started = time.perf_counter()
        fn()
        timings.append(time.perf_counter() - started)
    return min(timings)


def measure_event_text(module: str, iterations: int = 20_000) -> float:
    """Read a message's text through the public event property."""
    event_cls = __import__(f"{module}.types.event", fromlist=["Event"]).Event
    event = event_cls(dict(PAYLOAD))

    def run() -> None:
        for _ in range(iterations):
            event.text

    return _best(run)


def measure_lookup(module: str, iterations: int = 20_000) -> float:
    """Single-key recursive/索引ed lookup on a nested payload."""
    data_cls = __import__(f"{module}.data", fromlist=["Data"]).Data
    instance = data_cls(PAYLOAD)

    def run() -> None:
        for _ in range(iterations):
            instance.find_keys("text")

    return _best(run)


def measure_filter(module: str, iterations: int = 5_000) -> float:
    """Evaluate a Text filter against an event."""
    import importlib

    # __import__("darkob.bot.filters") resolves to the Bot class alias, not
    # the submodule, so import the module explicitly.
    filters = importlib.import_module(f"{module}.bot.filters")
    event_module = importlib.import_module(f"{module}.types.event")
    event_cls = event_module.Event
    event = event_cls({"message": {"text": "/start please"}})
    text_filter = filters.Text("start")

    async def loop() -> None:
        for _ in range(iterations):
            await text_filter.evaluate(event)

    def run() -> None:
        asyncio.run(loop())

    return _best(run)


async def _dispatch_run(module: str, handlers: int, events: int) -> float:
    api_cls = __import__(f"{module}.client.core.api", fromlist=["Api"]).Api
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
    )
    api = api_cls(client)

    class MessageUpdates:
        __name__ = "MessageUpdates"

        async def __call__(self, event: Any = None) -> bool:
            return False  # never matches: measures pure routing cost

    async def handler(event: Any) -> None:
        return None

    client.handlers = {handler: MessageUpdates() for _ in range(handlers)}
    if hasattr(api, "_dispatch_index"):
        api._dispatch_index = None

    started = time.perf_counter()
    for _ in range(events):
        await api.handle_update("message_updates", dict(PAYLOAD))
    elapsed = time.perf_counter() - started

    try:
        await api.close()
    except Exception:
        pass
    return elapsed


def measure_dispatch(module: str, handlers: int, events: int = 5_000) -> float:
    """Route *events* updates; long enough to amortise one-time setup."""
    return min(asyncio.run(_dispatch_run(module, handlers, events)) for _ in range(3))


MEASUREMENTS: List[Dict[str, Any]] = [
    {"key": "event_text", "label": "Read `event.text` ×20,000",
     "fn": lambda m: measure_event_text(m)},
    {"key": "lookup", "label": "Nested key lookup ×20,000",
     "fn": lambda m: measure_lookup(m)},
    {"key": "filter", "label": "Filter evaluation ×5,000",
     "fn": lambda m: measure_filter(m)},
    {"key": "dispatch_50", "label": "Route an update, 50 handlers",
     "fn": lambda m: measure_dispatch(m, 50)},
    {"key": "dispatch_500", "label": "Route an update, 500 handlers",
     "fn": lambda m: measure_dispatch(m, 500)},
]


def run_one(module: str, key: str) -> Optional[float]:
    """Measure one case in a clean interpreter, so caches stay honest."""
    code = (
        "import json,sys;"
        f"sys.path.insert(0, {str(REPO_ROOT)!r});"
        "import benchmarks.benchmark_suite as b;"
        f"print(b.MEASURE_BY_KEY[{key!r}]({module!r}))"
    )
    result = subprocess.run(
        [sys.executable, "-W", "ignore", "-c", code],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        return None
    try:
        return float(result.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return None


MEASURE_BY_KEY = {item["key"]: item["fn"] for item in MEASUREMENTS}


def fmt(seconds: Optional[float]) -> str:
    if seconds is None:
        return "n/a"
    if seconds < 0.001:
        return f"{seconds * 1e6:.0f} µs"
    if seconds < 1:
        return f"{seconds * 1000:.1f} ms"
    return f"{seconds:.2f} s"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    rows = []
    for item in MEASUREMENTS:
        ours = run_one("darkob", item["key"])
        theirs = run_one("maxrubika", item["key"])
        if ours and theirs:
            factor = theirs / ours
            delta = f"{factor:.1f}× faster" if factor >= 1.05 else (
                "comparable" if factor > 0.95 else f"{1 / factor:.1f}× slower"
            )
        else:
            delta = "n/a"
        rows.append(
            {
                "name": item["label"],
                "ours": fmt(ours),
                "theirs": fmt(theirs),
                "delta": delta,
                "factor": round(theirs / ours, 2) if ours and theirs else None,
            }
        )

    if args.json:
        print(json.dumps(rows, indent=2))
        return 0

    print("| Benchmark | darkob | maxrubika | Result |")
    print("| --- | --- | --- | --- |")
    for row in rows:
        print(f"| {row['name']} | {row['ours']} | {row['theirs']} | {row['delta']} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

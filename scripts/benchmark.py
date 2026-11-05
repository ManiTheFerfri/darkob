"""Local micro-benchmarks for the hot paths.

    python scripts/benchmark.py

No network and no sleeping: this measures the library's own overhead, so
it can run in CI to catch regressions.
"""

from __future__ import annotations

import asyncio
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from darkob.builders import MessageBuilder          # noqa: E402
from darkob.data import Data                        # noqa: E402
from darkob.retry import Retry                      # noqa: E402
from darkob.router import Router                    # noqa: E402


def measure(label: str, func, iterations: int = 20_000) -> float:
    """Run *func* and report microseconds per call."""
    timings = []
    for _ in range(5):
        start = time.perf_counter()
        for _ in range(iterations):
            func()
        timings.append((time.perf_counter() - start) / iterations * 1_000_000)

    best = min(timings)
    spread = statistics.pstdev(timings)
    print(f"{label:<38} {best:8.3f} us  (+/- {spread:.3f})")
    return best


async def dispatch_cost() -> None:
    from darkob.bot.filters import EventConstraint
    from darkob.bot.registry import HandlerRegistry

    class Always(EventConstraint):
        async def evaluate(self, event):
            return True

    class BotStub:
        run_all_handlers = True

    registry = HandlerRegistry(BotStub())

    async def handler(bot, event):
        return None

    for _ in range(10):
        registry.store(handler, Always())

    iterations = 5_000
    start = time.perf_counter()
    for _ in range(iterations):
        await registry.feed({"x": 1})
    elapsed = (time.perf_counter() - start) / iterations * 1_000_000
    print(f"{'dispatch (10 handlers)':<38} {elapsed:8.3f} us")


def main() -> None:
    print("darkob micro-benchmarks\n")

    data = Data({"message": {"text": "hi", "chat_id": "g0"}})
    measure("Data attribute lookup", lambda: data.text)
    measure("Data nested item lookup", lambda: data["message"]["text"])

    builder = MessageBuilder("hello").inline("kb")
    measure("MessageBuilder.build", builder.build)

    retry = Retry()
    measure("Retry.delay", lambda: retry.delay(2))

    router = Router("bench")

    @router.command("start")
    async def _start(bot, event):
        return None

    measure("Router.route declaration", lambda: len(router.routes))

    asyncio.run(dispatch_cost())
    print("\ndone")


if __name__ == "__main__":
    main()

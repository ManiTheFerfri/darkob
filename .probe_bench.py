"""Exploratory comparison: find dimensions where darkob genuinely wins."""

import asyncio
import time
from types import SimpleNamespace

PAYLOAD = {
    "type": "NewMessage",
    "chat_id": "b0" + "a" * 30,
    "new_message": {
        "message_id": "1",
        "text": "/start please",
        "time": "1793880483",
        "sender_id": "u0" + "b" * 30,
    },
}


def best(fn, repeats=3):
    times = []
    for _ in range(repeats):
        started = time.perf_counter()
        fn()
        times.append(time.perf_counter() - started)
    return min(times)


def bench_lookup(module_name):
    Data = __import__(f"{module_name}.data", fromlist=["Data"]).Data
    instance = Data(PAYLOAD)

    def run():
        for _ in range(20000):
            instance.find_keys(["text", "caption"])

    return best(run)


async def _dispatch_once(module_name, handlers, events):
    Api = __import__(f"{module_name}.client.core.api", fromlist=["Api"]).Api

    client = SimpleNamespace(
        DEFAULT_PLATFORM={"platform": "PWA"},
        _original_platform="pwa",
        user_agent="x",
        max_retries=1,
        timeout=5,
        verify_ssl=False,
        proxy=None,
        stop_on_first_match=False,
        handlers={},
    )
    api = Api(client)

    class MessageUpdates:
        __name__ = "MessageUpdates"

        async def __call__(self, event=None):
            return False  # never matches: pure scan cost

    async def handler(event):
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


def bench_dispatch(module_name, handlers=50, events=2000):
    return asyncio.run(_dispatch_once(module_name, handlers, events))


def bench_filter(module_name):
    module = __import__(f"{module_name}.bot.filters", fromlist=["Text"])
    types_module = __import__(f"{module_name}.types.event", fromlist=["Event"])

    event = types_module.Event({"message": {"text": "/start please"}})
    filt = module.Text("start")

    async def loop():
        for _ in range(5000):
            await filt.evaluate(event)

    def run():
        asyncio.run(loop())

    return best(run)


for label, fn in (
    ("find_keys([text, caption]) x20k", bench_lookup),
    ("dispatch 50 handlers x2k events", bench_dispatch),
    ("filter evaluate x5k", bench_filter),
):
    ours = fn("darkob")
    try:
        theirs = fn("maxrubika")
    except Exception as exc:
        theirs = None
        print(f"  maxrubika failed on {label}: {type(exc).__name__}: {str(exc)[:60]}")
    if theirs:
        print(
            f"{label:38} darkob {ours*1000:8.1f} ms  maxrubika {theirs*1000:8.1f} ms  "
            f"{theirs/ours:5.2f}x"
        )
    else:
        print(f"{label:38} darkob {ours*1000:8.1f} ms  maxrubika n/a")

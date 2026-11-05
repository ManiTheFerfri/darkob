# Errors

darkob raises typed exceptions instead of returning `None` and hoping.

## Bot API exceptions

Import from `darkob.bot.exceptions`. All inherit from `APIException`.

| Exception | Raised when |
| --- | --- |
| `Network` | The request could not complete after the retry budget |
| `Timeout` | The request or the server timed out |
| `BadGateway` | Upstream returned HTTP 502 |
| `ServerError` | Server-side failure (`SERVER_ERROR`) |
| `JSONDecode` | The response body was not valid JSON |
| `InvalidResponse` | Unexpected response shape |
| `InvalidInput` | The request was rejected (`INVALID_INPUT`) |
| `InvalidAccess` | Not authorised (`INVALID_ACCESS`) |
| `TooRequests` | Rate limited (`TOO_REQUESTS`) |
| `TokenError` | The bot token is malformed |

```python
from darkob.bot.exceptions import TooRequests, Network

try:
    await bot.send_message(chat_id, "hi")
except TooRequests:
    await asyncio.sleep(5)
except Network:
    log.warning("network down, giving up on this message")
```

## Messenger exceptions

| Exception | Raised when |
| --- | --- |
| `NetworkError` | Could not reach a data centre |
| `RequestError` | The API rejected the request |
| `ValidationError` | Bad argument passed by you |
| `InvalidInput`, `InvalidAccess`, `TooRequests`, `ServerError` | API-level statuses |
| `AuthError`, `SessionError`, `ApiVersionError`, `PlatformError` | Construction / login problems |
| `TimeoutError`, `MaxRetriesError`, `ProxyError` | Configuration problems |
| `NoConnection` | You called a method before `start()` |

## Retries

`max_retries` is a **budget for one request**, not per endpoint.

- Attempts rotate across known data-centre endpoints before repeating.
- Backoff carries jitter, so many bots do not retry in lockstep.
- HTTP `429` and a `TOO_REQUESTS` payload get a longer, escalating delay.
- The endpoint that answered last is promoted for the next request.

```python
bot = Bot(token="...", max_retries=3)     # 3 attempts total
```

Set `max_retries=0` to fail fast in tests.

## Surviving a bad connection

`SendQueue` wraps sending so a dropped connection does not lose
messages:

```python
from darkob import Bot, SendQueue

bot = Bot(token="...")
queue = SendQueue(bot, path="outbox.json")   # survives a restart
queue.start()                                  # flush in the background

await queue.put(event.chat_id, "report ready")
```

`put` returns `True` when the message went out immediately and
`False` when it was queued. Only transient failures (network,
timeout) are queued; a permanent error such as an invalid chat id
is raised at once, and is dropped during a flush rather than
blocking everything behind it.

## Tracking protocol drift

Rubika reshuffles its data-centre endpoints from time to time. A tracker
makes that visible instead of mysterious:

`python
from darkob import ProtocolTracker

tracker = ProtocolTracker(path="protocol.json")
changes = tracker.record(client.connection, client)
if changes:
    print("protocol changed:", changes)
`

It snapshots the API and socket URLs, the endpoint codes, the platform and
the app version, stores the last snapshot, and reports differences.

## Rate limiting

Rubika throttles bots, and a burst of sends is the fastest way to
earn a `TOO_REQUESTS`. A limiter keeps you under the ceiling before
the server has to enforce it.

```python
from darkob import Bot, RateLimiter

bot = Bot(
    token="...",
    rate_limiter=RateLimiter(rate=20, burst=5, per_chat_rate=3),
)
```

`rate` is tokens per second, `burst` the bucket size. With
`per_chat_rate`, each conversation gets its own bucket so one busy
group cannot starve the rest; the buckets are capped and evicted
oldest-first, so memory stays bounded.

The limiter applies to every attempt, including retries.

## Circuit breaker

Each data-centre endpoint has its own breaker. After 5 consecutive
failures it opens, and requests stop being sent to that endpoint
for 30 seconds. After the timeout it half-opens and one request is
allowed through as a probe; success closes it, failure reopens it.

This stops a dead endpoint from consuming the retry budget of every
request:

```python
client.connection.breaker_for("https://api.example")
breaker.threshold = 10        # be more tolerant
breaker.reset_timeout = 60.0  # wait longer before probing
```

If every endpoint is open, the request fails immediately with a log
line instead of timing out.

## Retry policy

For anything more than a count, pass a :class:`Retry` policy. It
overrides `max_retries` on both the Bot and Messenger surfaces.

```python
from darkob import Retry

bot = Bot(token="...", retry=Retry(attempts=5, backoff=0.5))
bot = Bot(token="...", retry=Retry.none())        # fail fast
bot = Bot(token="...", retry=Retry.patient())     # few, slow tries
bot = Bot(token="...", retry=Retry.aggressive())  # many, quick tries
```

| Field | Meaning |
| --- | --- |
| `attempts` | Total attempts, including the first |
| `backoff` | Base delay in seconds, growing linearly |
| `jitter` | Fraction of the delay randomised (0–1) |
| `max_delay` | Ceiling for any single wait |
| `rate_limit_backoff` | Base delay when the server reports rate limiting |

`Retry.delay(attempt)` and `Retry.should_retry(attempt)` are pure
functions, so they are easy to unit test.

## What darkob does not do

- It never swallows `KeyboardInterrupt` or `SystemExit` — only `Exception`.
- It does not retry `4xx` responses from the Bot API; those are your bug.
- It does not hide handler crashes: a failing handler is logged with a
  traceback and the remaining handlers still run.

## Debugging a silent bot

1. Turn on logging:

   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. Check that your filter actually matches — log inside the handler.
3. Check the bot token and chat id.
4. If nothing is delivered at all, switch to polling to rule out the
   webhook path.

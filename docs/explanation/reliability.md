# Reliability

What darkob does when a request fails, and which knobs decide how hard it tries before giving up.

## The failure ladder

Every call has four layers of protection, in this order:

1. **Retry budget** — a bounded number of attempts.
2. **Circuit breakers** — dead data centres are skipped, not retried.
3. **Rate limiting** — requests wait before the server has to decline them.
4. **A durable outbox** — `SendQueue` keeps what could not be sent.

On the Bot surface only layers 1, 3 and 4 exist: one fixed base URL means
there is nothing to discover, no breaker to trip, and no endpoint to rank.

## Retries

```python
bot = Bot(token="...", max_retries=3)          # 3 attempts total
client = Messenger(string_session="...", retry=Retry(attempts=5, backoff=0.5))
```

`max_retries` is a count; `Retry` is a policy object that overrides it on
both surfaces:

| Field | Default | Meaning |
| --- | --- | --- |
| `attempts` | `3` | Total attempts, including the first. Must be `>= 1` |
| `backoff` | `1.0` | Base delay in seconds, growing with the attempt number |
| `jitter` | `0.5` | Fraction of each delay randomised, `0.0`–`1.0` |
| `max_delay` | `30.0` | Ceiling for one delay |
| `rate_limit_backoff` | `5.0` | Base delay when the server says "slow down" |

```python
Retry.none()         # 1 attempt, no waiting  — tests and CLIs
Retry.aggressive()   # 5 attempts, 0.25s base, max 5s
Retry.patient()      # 4 attempts, 3s base, max 60s
```

`Retry.delay(attempt)` and `Retry.should_retry(attempt)` are pure, so a
retry policy can be unit-tested without any I/O.

With no policy, the two surfaces differ:

- **Bot** sleeps `2 ** attempt` seconds between attempts;
- **Messenger/Shad** backs off once per full pass over the endpoint list
  (`backoff * (1 + attempts // len(candidates))`) and always applies jitter.

| Failure | Bot | Messenger / Shad |
| --- | --- | --- |
| `Network`, `Timeout`, HTTP 502/500 | Retried | Retried |
| `TOO_REQUESTS` / HTTP 429 | Raised to you at once | Retried after a longer wait |
| `InvalidInput`, `InvalidAccess`, `JSONDecode` | Raised at once | Raised at once |

## The retry budget belongs to the request

`attempts` is a budget for **the whole request**, not for each endpoint.
This matters: a nested `for endpoint: for attempt:` loop — the obvious
implementation, and the one darkob replaced — can fire
`len(endpoints) × attempts` requests when the network is down, stalling a
handler for minutes.

Instead, the client walks its endpoint list once per attempt:

```python
while attempts < attempts_budget:
    candidate = candidates[attempts % len(candidates)]
    ...
```

Three endpoints with `attempts=5` means five requests, not fifteen, and the
budget is spent in bounded time. `Retry.none()` therefore means "one
attempt, fail fast" rather than "one attempt per endpoint".

## Circuit breakers

Each discovered endpoint has its own breaker, so a dead data centre stops
being tried by every subsequent request instead of consuming the budget of
each one.

```text
closed --(5 consecutive failures)--> open
open   --(30 s elapsed)-----------> half_open
half_open --(success)-------------> closed
half_open --(failure)-------------> open
```

While a breaker is open its endpoint is dropped from the candidate list. If
**every** endpoint is open, the request fails immediately with a log line
instead of timing out.

```python
breaker = client.connection.breaker_for("https://api.example/")
breaker.threshold = 10        # be more tolerant
breaker.reset_timeout = 60.0  # wait longer before probing
breaker.state                 # "closed" | "open" | "half_open"
breaker.failures              # consecutive failures
breaker.reset()
```

`record_success()` closes the circuit, `record_failure()` counts a failure
and trips it at the threshold. Half-open is the probe state: one request is
allowed through, and its outcome decides whether the endpoint comes back.

## Latency-based ordering

Candidates are sorted by:

1. breaker open? (healthy endpoints first),
2. measured latency (exponential moving average, `0.8 * old + 0.2 * new`),
3. discovery order, as the tie-break.

The endpoint that answered last is also promoted to the front of the
priority list. A fast node is tried first; a node that just failed sits at
the back until its breaker closes.

## The flood-wait ceiling

`flood_sleep_threshold` (client only, default `60.0`) caps how long darkob
will wait out a server-imposed rate limit:

```python
client = Messenger(string_session="...", flood_sleep_threshold=120)
```

When the computed rate-limit delay exceeds the threshold, darkob logs an
error and **abandons that request** rather than sleeping for minutes. The
alternative — blocking a task for ten minutes — is worse for a bot that has
other work to do.

!!! note "The ceiling is not a timeout"
    `flood_sleep_threshold` compares against the *wait* darkob would have
    to sleep, not against request duration. Timeouts come from `timeout=`
    on the client.

## `SendQueue`: a durable outbox

Retries cover a request in flight. `SendQueue` covers a connection that is
gone for minutes:

```python
from darkob import Bot, SendQueue

bot = Bot(token="...")
queue = SendQueue(bot, path="outbox.json", max_size=1000, retry_delay=5.0)
queue.start()                                  # flush in the background

sent = await queue.put(event.chat_id, "report ready")
```

| Behaviour | Detail |
| --- | --- |
| `put(...)` returns `True` | The message went out immediately |
| `put(...)` returns `False` | It failed transiently and is now queued |
| Permanent errors | Raised at once; never queued |
| `path` | JSON file, written atomically and reloaded at construction |
| `max_size` | `QueueFull` is raised instead of growing without bound |
| `flush()` | Sends pending messages in order, returns how many went out |
| `drain()` | Removes and returns everything, persisting the empty queue |
| `pending` / `len(queue)` | How many messages are waiting |

Only transient failures are queued — `darkob.bot.exceptions.Network`,
`NetworkError`, `asyncio.TimeoutError`, `OSError`. A message rejected for a
bad chat id is a bug, not a network problem, so it is raised immediately;
during a flush the same failure is dropped rather than blocking everything
behind it.

The file is written with a temporary file plus `os.replace()`, so a crash
mid-write cannot leave a half-written outbox. Queued messages survive a
restart, and `stop()` keeps them.

## Putting it together

```python
from darkob import Bot, RateLimiter, Retry, SendQueue

bot = Bot(
    token="...",
    retry=Retry(attempts=4, backoff=0.5, jitter=0.5),
    rate_limiter=RateLimiter(rate=20, burst=5, per_chat_rate=3),
)
queue = SendQueue(bot, path="outbox.json")
queue.start()
```

The limiter keeps you under the ceiling, `Retry` bounds how hard a failure
is retried, and the queue absorbs the window where the network is gone
entirely.

## See also

- [Errors](../guides/errors.md)
- [Rate-limit safely](../how-to/rate-limit-safely.md)
- [Architecture](architecture.md)
- [Concurrency](concurrency.md)
- [Observe in production](../how-to/observe-in-production.md)

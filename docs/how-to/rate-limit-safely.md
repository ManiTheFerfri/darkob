# Rate-limit safely

Pick a limiter that keeps your bot under Rubika's ceiling instead of collecting `TOO_REQUESTS` errors.

## Two limiters, one interface

```python
from darkob import AdaptiveRateLimiter, RateLimiter

RateLimiter(rate=20, burst=5)                 # fixed ceiling
AdaptiveRateLimiter(rate=20, min_rate=2)      # self-tuning ceiling
```

Both are token buckets: `rate` tokens are added per second, the bucket
holds at most `burst` of them, and every API call takes one. When the
bucket is empty the caller waits — the limit is enforced *before* the
server has to.

`AdaptiveRateLimiter(...)` is exactly `RateLimiter(..., adaptive=True)`,
named separately so the behaviour is visible at the call site.

Pass the object to the client and you are done:

```python
bot = Bot(token="...", rate_limiter=RateLimiter(rate=20, burst=5))
client = Messenger(string_session="...", rate_limiter=AdaptiveRateLimiter(rate=20))
```

!!! note "One limiter per client"
    The limiter is shared by every request the client makes, including
    retries. Do not reuse one limiter object across two clients: its
    buckets belong to the event loop that first used them.

## The four knobs you will actually set

| Knob | Default | What it does |
| --- | --- | --- |
| `rate` | `20.0` | Tokens per second, i.e. requests per second |
| `burst` | `None` | Bucket capacity; `None` means `max(1.0, rate)` |
| `per_chat_rate` | `None` | A second bucket per conversation |
| `per_chat_burst` | `None` | Capacity of each per-conversation bucket |

Rates must be greater than zero, and `min_rate` may not exceed `rate`;
both are `ValueError` at construction rather than a silent misconfiguration.

```python
limiter = RateLimiter(rate=20, burst=5, per_chat_rate=3)
```

With `per_chat_rate`, one busy group cannot starve the others: each
conversation gets its own bucket, so a broadcast to a thousand chats is
paced per chat as well as globally. The buckets are capped at
`max_buckets` (4096 by default) and evicted oldest-first, so memory stays
bounded no matter how many chats you touch.

## The AIMD knobs

A fixed rate is a guess. Too low and you waste throughput; too high and
the server throttles you anyway. An adaptive limiter closes the loop with
additive increase / multiplicative decrease — the control law TCP
congestion control uses.

| Knob | Default | Meaning |
| --- | --- | --- |
| `min_rate` | `1.0` | Floor the effective rate can be reduced to |
| `decrease_factor` | `0.5` | Multiplier applied on every throttle |
| `increase_step` | `1.0` | Tokens per second added on recovery |
| `increase_interval` | `1.0` | Minimum seconds between two increases |
| `max_block` | `60.0` | Ceiling on a server-requested pause, in seconds |

```python
limiter = AdaptiveRateLimiter(
    rate=20,              # start optimistic: 20 requests/second
    per_chat_rate=3,      # never more than 3/second into one chat
    min_rate=2,           # never drop below 2/second
    decrease_factor=0.25, # a throttle costs 75% of the current rate
    increase_step=1.0,    # climb back 1/second ...
    increase_interval=2,  # ... at most every 2 seconds
    max_block=30,         # cap a Retry-After at 30 seconds
)
```

On a throttle the effective rate is multiplied by `decrease_factor`, never
below `min_rate`. On success it grows by `increase_step`, never above
`rate`, and at most once per `increase_interval` seconds. Per-chat bucket
rates scale with the global rate, so they shrink and recover with it.

## Who calls `on_throttle()` and `on_success()`

You do not. On the **Messenger/Shad** surface the client reports both
events for you, inside the request loop:

- an HTTP `429` or a `{"status": "TOO_REQUESTS"}` body calls
  `limiter.on_throttle(retry_after)` with the `Retry-After` header when
  the server sent one, which also pauses acquisition for up to
  `max_block` seconds for *every* caller;
- every successful response calls `limiter.on_success()`.

A plain `RateLimiter` has the same methods, and they do nothing: no rate
change, no pause, no error. That is the point of `adaptive=False` — enabling
it can never alter the behaviour of a bot that already worked.

!!! warning "The Bot surface does not feed the limiter"
    `darkob.Bot` acquires a token before each attempt, using the payload's
    `chat_id` (or `object_guid`) as the per-chat key, but it does not call
    `on_throttle()` or `on_success()` — its request path raises
    `TooRequests` straight to you. On a bot, an adaptive limiter therefore
    stays at its starting rate unless you report outcomes yourself:

    ```python
    from darkob.bot.exceptions import TooRequests

    try:
        await bot.send_message(chat_id, "report ready")
    except TooRequests:
        limiter.on_throttle()
    ```

## Reading the state

```python
limiter.current_rate    # effective rate now, tokens per second
limiter.blocked_for     # seconds of forced quiet left, 0.0 when free
limiter.stats()         # a dict, ready for a log line or a metric
```

`stats()` returns `rate`, `current_rate`, `min_rate`, `adaptive`,
`throttles`, `recoveries`, `acquired`, `blocked_for`, `chats_tracked` and
`tokens` (what is left in the global bucket). `limiter.reset()` returns to
the configured rate and clears the counters.

```python
@bot.on_start()
async def announce(bot):
    print("limiter:", limiter.stats())

@bot.on_shutdown()
async def report(bot):
    stats = limiter.stats()
    print(f"throttled {stats['throttles']}x, "
          f"ended at {stats['current_rate']:.1f}/s")
```

## Choosing

- **Start with a plain `RateLimiter`.** `rate=20, burst=5` is a safe
  default, and `per_chat_rate` fixes the most common real problem: one
  noisy group.
- **Switch to adaptive** when you do not know the ceiling, or when the
  ceiling moves — a shared bot, several deployments, or a platform that
  changes its tolerance. Keep `min_rate` high enough to stay useful.
- **Raise `max_block`** above `Retry-After` if you would rather wait than
  lose the message; lower it if a stalled request is worse than a dropped
  one.

## See also

- [Errors](../guides/errors.md)
- [Reliability](../explanation/reliability.md)
- [Observe in production](observe-in-production.md)
- [Bot vs Messenger vs Shad](../explanation/bot-vs-messenger-vs-shad.md)
- [Quickstart](../get-started/quickstart.md)

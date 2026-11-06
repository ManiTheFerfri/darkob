# Observe in production

Turn on darkob's in-process metrics, read them as a dict, and expose them to Prometheus without adding a metrics server dependency.

## Turn it on

```python
from darkob.metrics import enable_metrics, metrics

enable_metrics()          # off by default
bot.run()
```

`enable_metrics()` configures and enables the shared registry and returns
it. All arguments are keyword-only:

| Argument | Default | Meaning |
| --- | --- | --- |
| `prefix` | `"darkob"` | Prefix applied to every metric name when rendering |
| `histogram_capacity` | `512` | Samples kept per histogram for percentiles |
| `reset` | `True` | Clear anything recorded before enabling |

`disable_metrics()` turns instrumentation off again and keeps whatever was
already recorded.

!!! note "Import `metrics` from `darkob.metrics`"
    The registry instance is deliberately **not** re-exported from the
    package root: `from darkob import metrics` would be ambiguous with the
    module of the same name. Import the functions from the root, the
    instance from the module:

    ```python
    from darkob import enable_metrics          # function
    from darkob.metrics import metrics         # registry instance
    ```

## What gets recorded for you

| Metric | Kind | Recorded when |
| --- | --- | --- |
| `darkob.updates` | counter | An update is received |
| `darkob.update.seconds` | histogram | Dispatch of one update finishes |
| `darkob.handlers.skipped` | counter | A handler's filters did not match |
| `darkob.handlers.called` | counter | A handler passed its filters |
| `darkob.handlers.errors` | counter | A handler raised |
| `darkob.api.requests` | counter | An HTTP call is issued |
| `darkob.api.errors` | counter | An HTTP call failed |
| `darkob.api.retries` | counter | A retry follows a failure |
| `darkob.api.ratelimited` | counter | The server throttled a call |
| `darkob.api.seconds` | histogram | Latency of one HTTP call |
| `darkob.queue.pending` | gauge | **Not recorded automatically** — set it yourself |

!!! warning "Where the built-in counters actually fire"
    The instrumentation lives in the Messenger/Shad request loop and
    dispatch path. `darkob.Bot` does not record `darkob.api.*` or
    `darkob.updates` on its own request path, and nothing in the library
    writes `darkob.queue.pending`; the queue exposes `pending` instead, so
    record it on your own schedule:

    ```python
    metrics.set("darkob.queue.pending", queue.pending)
    ```

    Every counter, gauge and histogram you create yourself works the same
    way on both surfaces.

## Read a snapshot

```python
snapshot = metrics.snapshot()
```

```python
{
  "counters": {"darkob.api.requests": 1284},
  "gauges": {},
  "histograms": {
    "darkob.api.seconds": {
      "count": 1284, "sum": 23.5, "min": 0.004, "max": 2.1,
      "mean": 0.018, "p50": 0.012, "p95": 0.041, "p99": 0.5,
    }
  },
}
```

(Values shortened for readability.) `snapshot()` is plain JSON-safe data,
so `json.dumps(metrics.snapshot())` works as-is. Percentiles come from a
bounded ring buffer of the last `histogram_capacity` samples per histogram
— memory stays flat however long the bot runs, and the sort only happens
when you ask for a snapshot.

## Render the Prometheus text format

```python
print(metrics.render_prometheus())
```

```text
# TYPE darkob_api_requests counter
darkob_api_requests 1284
# TYPE darkob_api_seconds summary
darkob_api_seconds{quantile="0.5"} 0.012
darkob_api_seconds{quantile="0.95"} 0.041
darkob_api_seconds{quantile="0.99"} 0.5
darkob_api_seconds_count 1284
darkob_api_seconds_sum 23.5
```

Dots become underscores, the configured prefix is prepended once, counters
become `counter` lines, gauges `gauge` lines, and histograms become
`summary` metrics with `quantile` labels plus `_count` and `_sum`. Pass
`render_prometheus(prefix="mybot")` to change the prefix for one render.

## Scrape it with aiohttp

darkob's webhook server is created inside `bot.run()` and is not exposed,
so serve metrics on their own port:

```python title="metrics_server.py"
from aiohttp import web

from darkob.metrics import metrics


async def scrape(request):
    return web.Response(
        text=metrics.render_prometheus(),
        content_type="text/plain",
        charset="utf-8",
    )


app = web.Application()
app.router.add_get("/metrics", scrape)
web.run_app(app, host="127.0.0.1", port=9101)
```

```yaml title="prometheus.yml"
scrape_configs:
  - job_name: darkob
    static_configs:
      - targets: ["127.0.0.1:9101"]
```

Bind to `127.0.0.1` and let Prometheus reach it over a private network or
an authenticated proxy: metric names and label-less values are harmless,
but the endpoint still leaks your traffic volume.

## Record your own numbers

The same registry is public, so application metrics sit next to the
built-in ones:

```python
from darkob.metrics import metrics

metrics.increment("orders.created")
metrics.decrement("orders.queued")
metrics.set("workers.busy", 3)
metrics.adjust("workers.busy", -1)
metrics.observe("orders.total_seconds", 0.42)

with metrics.timer("orders.checkout"):
    await checkout()

@metrics.time_it("catalog.search")
async def search(query: str) -> list:
    ...
```

`time_it` handles sync and async callables, and uses
`module.qualname` when you pass no name.

!!! note "What 'off' actually costs"
    While the registry is disabled the library's own instrumentation costs
    one attribute read and a branch per hot-path call — it records nothing,
    which is why metrics are opt-in. Your own `metrics.increment(...)` calls
    are not guarded: they record whether or not you called
    `enable_metrics()` first.

## See also

- [Health checks](health-checks.md)
- [Rate-limit safely](rate-limit-safely.md)
- [Reliability](../explanation/reliability.md)
- [Architecture](../explanation/architecture.md)
- [Errors](../guides/errors.md)

# Health checks

Expose liveness and readiness probes so a container orchestrator restarts a wedged bot and stops routing traffic to one that cannot reach Rubika.

## Liveness versus readiness

A polling bot needs no health endpoint: if the process runs, it works. A
bot behind a webhook, in a container, or behind a load balancer does need
one, because "the process is up" and "the bot can do its job" are different
facts.

| Probe | Question | Failure means |
| --- | --- | --- |
| **liveness** | Is this process still functioning? | Restart it |
| **readiness** | Should traffic be sent here? | Stop routing, keep running |

Only **critical readiness** checks can make a service unready. A failing
non-critical check marks the report `degraded` and still answers `200`: a
missing optional dependency should not get your pod killed.

## Register checks

```python
from darkob.health import HealthRegistry, queue_backlog_check, tcp_check

health = HealthRegistry()                     # default per-check timeout: 5s
health.add("api", tcp_check("messenger.rubika.ir", 443), kind="readiness")
health.add("outbox", queue_backlog_check(queue, max_pending=500),
           kind="readiness", critical=False)
health.add("loop", lambda: True, kind="liveness")
```

`add(name, check, *, kind="readiness", critical=True, timeout=None)`
returns the check unchanged, so it doubles as a decorator:

```python
@health.add("db")
async def check_db() -> bool:
    return await pool.ping()
```

| Argument | Default | Meaning |
| --- | --- | --- |
| `name` | required | Identifier in the report |
| `check` | `None` | Callable; omit it to use `add` as a decorator |
| `kind` | `"readiness"` | `"readiness"` or `"liveness"` — anything else is a `ValueError` |
| `critical` | `True` | Whether a failing readiness check makes the service unready |
| `timeout` | `None` | Overrides the registry timeout for this check |

`remove(name)`, `clear()`, `names` and `len(health)` manage the registry.

## Writing a check

A check returns `True`, `False`, a string, or an awaitable of either. A
**string means "unhealthy"** and is used as the detail, which is the
cheapest way to say why:

```python
@health.add("quota")
async def quota_ok():
    left = await remaining_quota()
    return True if left > 100 else f"only {left} requests left"
```

darkob catches whatever a check raises and reports it as a failure
(`"TimeoutError: …"`), including timeouts, so one broken probe can never
take the endpoint down with it. Checks run concurrently.

!!! warning "Do not probe the API from a readiness check"
    A check that logs in or calls `getMe` spends your quota and can be
    throttled. Prefer a TCP connect, a queue depth, or a value your bot
    already tracks.

## The two ready-made checks

```python
from darkob.health import queue_backlog_check, tcp_check

tcp_check("messenger.rubika.ir", 443)          # port=443, timeout=2.0
queue_backlog_check(queue, max_pending=1000)   # accepts a SendQueue
```

`tcp_check(host, port=443, *, timeout=2.0)` opens a TCP connection and
closes it immediately: enough to separate "the network is gone" from "the
process is wedged", without authenticating.

`queue_backlog_check(queue, max_pending=1000)` reads `queue.pending`, and
falls back to `len(queue)` for any object without that attribute. A
`SendQueue` that keeps growing is the earliest sign that sends are failing.
Pair it with `critical=False`: a backlog should degrade, not restart.

## Read the report

```python
report = await health.report()          # or report("readiness") / report("liveness")
report.status        # "ok" | "degraded" | "down"
report.ok            # True when the service is usable
report.live, report.ready
report.http_status   # 200 or 503
report.to_dict()     # JSON-safe dict
report.to_json()     # compact JSON string
```

The body looks like this:

```json
{"status": "ok", "ok": true, "live": true, "ready": true, "duration": 0.004,
 "checks": [{"name": "api", "healthy": true, "detail": "ok",
             "kind": "readiness", "duration": 0.004}]}
```

`await health.ready()` and `await health.live()` are shortcuts returning a
single boolean.

| Situation | `status` | `ok` | HTTP |
| --- | --- | --- | --- |
| Everything passes | `ok` | `True` | 200 |
| A non-critical readiness check fails | `degraded` | `True` | 200 |
| A critical readiness check fails | `down` | `False` | 503 |
| A liveness check fails | `down` | `False` | 503 |

A liveness failure also sets `live=False`; readiness only affects `ready`.

## Serve it

### aiohttp

```python title="health_server.py"
from aiohttp import web

from darkob.health import HealthRegistry, queue_backlog_check

health = HealthRegistry()
health.add("outbox", queue_backlog_check(queue, 500), critical=False)

app = web.Application()
app.router.add_get("/healthz", health.aiohttp_handler())
app.router.add_get("/livez", health.aiohttp_handler("/livez"))

web.run_app(app, host="127.0.0.1", port=8081)
```

`aiohttp_handler(path=None)` answers with `request.path` by default, so
pass the path explicitly when you mount the handler somewhere outside the
standard names below.

### Any ASGI framework

The registry maps paths itself:

| Paths | Probe |
| --- | --- |
| `/health`, `/healthz`, `/health/ready`, `/ready`, `/readyz` | readiness |
| `/health/live`, `/live`, `/livez`, `/health/liveness` | liveness |

`health.asgi_app()` returns a self-contained ASGI application for those
paths — it answers `GET` and `HEAD`, refuses other methods with `405`, and
returns `404` for unknown paths. Hand it to any server that accepts an ASGI
app. If your framework's router wants a request handler instead, return
the report yourself — three lines that work anywhere aiohttp does:

```python
from aiohttp import web

async def healthz(request):
    report = await health.report()
    return web.Response(
        text=report.to_json(),
        status=report.http_status,
        content_type="application/json",
    )
```

## See also

- [Observe in production](observe-in-production.md)
- [Reliability](../explanation/reliability.md)
- [Errors](../guides/errors.md)
- [Architecture](../explanation/architecture.md)
- [Project layout](../guides/project-layout.md)

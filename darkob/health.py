"""Liveness and readiness endpoints for webhook-deployed bots.

A polling bot needs nothing here — if the process is up, it is working. A bot
deployed behind a webhook, a container orchestrator, or a load balancer does:
the platform will send traffic to a process that is running but cannot reach
Rubika, and will keep a wedged process alive.

:class:`HealthRegistry` collects named checks and exposes them as JSON::

    from darkob.health import HealthRegistry, tcp_check, queue_backlog_check

    health = HealthRegistry()
    health.add("api", tcp_check("messenger.rubika.ir", 443), kind="readiness")
    health.add("outbox", queue_backlog_check(queue, max_pending=500),
               kind="readiness", critical=False)

    # FastAPI / Starlette
    app.add_route("/healthz", health.asgi_app())

    # aiohttp
    app.router.add_get("/healthz", health.aiohttp_handler())

The response is ``200`` when the service is usable and ``503`` when it is not,
with a body like::

    {"status": "ok", "ok": true, "live": true, "ready": true,
     "checks": [{"name": "api", "healthy": true, "detail": "connected",
                 "kind": "readiness", "duration": 0.004}]}

Liveness versus readiness
-------------------------

A **liveness** failure means the process is wedged and should be restarted.
A **readiness** failure means it should stop receiving traffic but keep
running.

Only *critical* readiness checks make the service unready. A non-critical
check that fails marks the report ``degraded`` and still returns ``200``: a
missing optional dependency should not get your pod killed. This distinction
is the difference between a health endpoint that helps and one that turns a
minor outage into a restart loop.
"""

from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, List, Optional, Union

from .utils.concurrency import timeout_after

__all__ = [
    "HealthRegistry",
    "HealthReport",
    "HealthResult",
    "queue_backlog_check",
    "tcp_check",
]

#: What a check may return: a bool, a string describing a failure, or an
#: awaitable of either.
CheckValue = Union[bool, str, Awaitable[Union[bool, str]]]
CheckFn = Callable[[], CheckValue]

#: Paths that are treated as a readiness probe.
_READY_PATHS = frozenset(
    {"/health", "/healthz", "/health/ready", "/ready", "/readyz"}
)
#: Paths that are treated as a liveness probe.
_LIVE_PATHS = frozenset({"/health/live", "/live", "/livez", "/health/liveness"})


@dataclass(frozen=True)
class HealthResult:
    """The outcome of one named check."""

    name: str
    healthy: bool
    detail: str = ""
    kind: str = "readiness"
    duration: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """JSON-friendly representation."""
        return {
            "name": self.name,
            "healthy": self.healthy,
            "detail": self.detail,
            "kind": self.kind,
            "duration": round(self.duration, 6),
        }


@dataclass(frozen=True)
class HealthReport:
    """The aggregate outcome of a probe.

    ``ok`` is the answer an orchestrator cares about: ``True`` means "keep
    sending me traffic". A degraded report is still ``ok``.
    """

    status: str
    live: bool
    ready: bool
    ok: bool
    checks: List[HealthResult] = field(default_factory=list)
    duration: float = 0.0

    @property
    def http_status(self) -> int:
        """``200`` when usable, ``503`` when not."""
        return 200 if self.ok else 503

    def to_dict(self) -> Dict[str, Any]:
        """JSON-friendly representation."""
        return {
            "status": self.status,
            "ok": self.ok,
            "live": self.live,
            "ready": self.ready,
            "duration": round(self.duration, 6),
            "checks": [check.to_dict() for check in self.checks],
        }

    def to_json(self) -> str:
        """Serialised report body."""
        return json.dumps(self.to_dict(), separators=(",", ":"))


@dataclass
class _Registration:
    name: str
    check: CheckFn
    kind: str
    critical: bool
    timeout: Optional[float]


class HealthRegistry:
    """A named collection of health checks.

    Checks are plain callables returning a bool, or a string describing a
    failure, or an awaitable of either. Exceptions are caught and reported as
    an unhealthy check so one broken probe cannot take down the endpoint.
    """

    __slots__ = ("timeout", "_checks")

    def __init__(self, *, timeout: float = 5.0) -> None:
        if timeout <= 0:
            raise ValueError("timeout must be greater than 0.")
        self.timeout = timeout
        self._checks: Dict[str, _Registration] = {}

    # -- registration -----------------------------------------------------

    def add(
        self,
        name: str,
        check: Optional[CheckFn] = None,
        *,
        kind: str = "readiness",
        critical: bool = True,
        timeout: Optional[float] = None,
    ) -> Any:
        """Register *check* under *name*.

        Usable directly or as a decorator::

            health.add("db", check_db)
            health.add("db", check_db, critical=False, timeout=1.0)

            @health.add("db")
            async def check_db() -> bool:
                return await pool.ping()

        Examples:
            >>> from darkob.health import HealthRegistry
            >>> health = HealthRegistry()
            >>> _ = health.add("api", lambda: True)
            >>> health.names
            ['api']
        """
        if kind not in ("readiness", "liveness"):
            raise ValueError("kind must be 'readiness' or 'liveness'.")

        def register(func: CheckFn) -> CheckFn:
            self._checks[name] = _Registration(
                name=name,
                check=func,
                kind=kind,
                critical=critical,
                timeout=timeout,
            )
            return func

        if check is not None:
            register(check)
            return check
        return register

    def remove(self, name: str) -> bool:
        """Unregister a check. Returns ``True`` if it existed."""
        return self._checks.pop(name, None) is not None

    def clear(self) -> None:
        """Remove every check."""
        self._checks.clear()

    @property
    def names(self) -> List[str]:
        """Registered check names, in registration order."""
        return list(self._checks)

    def __len__(self) -> int:
        return len(self._checks)

    # -- running ----------------------------------------------------------

    async def report(self, kind: Optional[str] = None) -> HealthReport:
        """Run the checks and build a :class:`HealthReport`.

        Checks run *concurrently*, and one failing check never prevents the
        others from reporting — which is why this uses ``gather`` rather than
        structured concurrency: a ``TaskGroup`` cancels its siblings on the
        first failure, hiding the very information an operator needs.
        """
        started = time.perf_counter()
        selected = [
            registration
            for registration in self._checks.values()
            if kind is None or registration.kind == kind
        ]
        results = await asyncio.gather(
            *(self._run_one(registration) for registration in selected)
        )

        live = all(
            result.healthy for result in results if result.kind == "liveness"
        )
        ready = all(
            result.healthy
            for result, registration in zip(results, selected)
            if result.kind == "readiness" and registration.critical
        )
        degraded = any(
            not result.healthy
            for result, registration in zip(results, selected)
            if result.kind == "readiness" and not registration.critical
        )

        if not live or not ready:
            status = "down"
        elif degraded:
            status = "degraded"
        else:
            status = "ok"

        return HealthReport(
            status=status,
            live=live,
            ready=ready,
            ok=live and ready,
            checks=results,
            duration=time.perf_counter() - started,
        )

    async def _run_one(self, registration: _Registration) -> HealthResult:
        started = time.perf_counter()
        limit = registration.timeout or self.timeout
        healthy = False
        detail = ""
        try:
            with_timeout = timeout_after(limit)
            async with with_timeout:
                value = registration.check()
                if asyncio.iscoroutine(value) or isinstance(
                    value, asyncio.Future
                ):
                    value = await value
            if isinstance(value, str):
                healthy = False
                detail = value
            else:
                healthy = bool(value)
                detail = "ok" if healthy else ""
        except TimeoutError:
            healthy = False
            detail = f"timed out after {limit:g}s"
        except asyncio.CancelledError:
            raise
        except BaseException as error:  # noqa: BLE001 - probes must never raise
            healthy = False
            detail = f"{type(error).__name__}: {error}"

        return HealthResult(
            name=registration.name,
            healthy=healthy,
            detail=detail,
            kind=registration.kind,
            duration=time.perf_counter() - started,
        )

    async def ready(self) -> bool:
        """``True`` when every critical readiness check passes."""
        return (await self.report("readiness")).ready

    async def live(self) -> bool:
        """``True`` when every liveness check passes."""
        return (await self.report("liveness")).live

    # -- adapters ---------------------------------------------------------

    async def _respond(self, path: str) -> tuple:
        """Map a request path to a ``(status, body)`` pair."""
        if path in _LIVE_PATHS:
            report = await self.report("liveness")
        elif path in _READY_PATHS:
            report = await self.report("readiness")
        else:
            return 404, json.dumps({"status": "not_found"})
        return report.http_status, report.to_json()

    def asgi_app(self) -> Callable[..., Any]:
        """An ASGI application exposing the registry.

        Dependency-free: works with Starlette, FastAPI, Litestar, and anything
        else that speaks ASGI. Mount it directly::

            app.add_route("/healthz", health.asgi_app())
        """

        async def app(scope: Dict[str, Any], receive: Any, send: Any) -> None:
            if scope.get("type") != "http":
                raise RuntimeError("HealthRegistry.asgi_app handles HTTP only.")

            method = scope.get("method", "GET")
            path = scope.get("path", "/")
            if method not in ("GET", "HEAD"):
                status, body = 405, json.dumps({"status": "method_not_allowed"})
            else:
                status, body = await self._respond(path)

            payload = b"" if method == "HEAD" else body.encode("utf-8")
            headers = [
                (b"content-type", b"application/json; charset=utf-8"),
                (b"cache-control", b"no-store"),
                (b"content-length", str(len(payload)).encode("ascii")),
            ]
            await send(
                {"type": "http.response.start", "status": status, "headers": headers}
            )
            await send({"type": "http.response.body", "body": payload})

        return app

    def aiohttp_handler(self, path: Optional[str] = None) -> Callable[..., Any]:
        """An ``aiohttp`` request handler exposing the registry.

        Pass the route *path* if you mount the handler somewhere other than
        the standard ``/healthz`` family, since aiohttp would otherwise have
        to guess which probe was requested.
        """

        async def handler(request: Any) -> Any:
            from aiohttp import web

            target = path or request.path
            status, body = await self._respond(target)
            return web.Response(
                text=body,
                status=status,
                content_type="application/json",
                headers={"cache-control": "no-store"},
            )

        return handler


# ---------------------------------------------------------------------------
# Ready-made checks
# ---------------------------------------------------------------------------


def tcp_check(host: str, port: int = 443, *, timeout: float = 2.0) -> CheckFn:
    """A check that the *host*:*port* accepts a TCP connection.

    Enough to distinguish "the network is gone" from "the process is wedged",
    without authenticating or spending API quota::

        health.add("rubika", tcp_check("messenger.rubika.ir", 443))
    """

    async def check() -> bool:
        writer = None
        try:
            async with timeout_after(timeout):
                _, writer = await asyncio.open_connection(host, port)
            return True
        finally:
            if writer is not None:
                writer.close()

    check.__name__ = f"tcp_check({host}:{port})"
    return check


def queue_backlog_check(queue: Any, max_pending: int = 1000) -> CheckFn:
    """A check that an outbox has not grown past *max_pending*.

    Useful with :class:`darkob.SendQueue`: a growing backlog is the earliest
    signal that sends are failing, long before the queue overflows::

        health.add("outbox", queue_backlog_check(queue, 500), critical=False)
    """
    if max_pending < 1:
        raise ValueError("max_pending must be at least 1.")

    def check() -> bool:
        pending = getattr(queue, "pending", None)
        if pending is None:
            pending = len(queue)
        return pending <= max_pending

    check.__name__ = f"queue_backlog_check(max_pending={max_pending})"
    return check

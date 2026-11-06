"""Tests for ``darkob.health``."""

from __future__ import annotations

import json
import time

import pytest

from darkob.health import (
    HealthRegistry,
    HealthReport,
    queue_backlog_check,
    tcp_check,
)


async def call_asgi(app, path: str = "/healthz", method: str = "GET"):
    """Drive an ASGI app and return ``(status, parsed_body)``."""
    sent = []

    async def send(message):
        sent.append(message)

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    await app(
        {"type": "http", "method": method, "path": path, "headers": []},
        receive,
        send,
    )
    status = sent[0]["status"]
    body = sent[1]["body"]
    return status, json.loads(body or b"{}")


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


def test_register_with_add_and_decorator():
    registry = HealthRegistry()

    def always() -> bool:
        return True

    registry.add("plain", always)

    @registry.add("decorated")
    def decorated() -> bool:
        return True

    assert registry.names == ["plain", "decorated"]
    assert len(registry) == 2


def test_remove_and_clear():
    registry = HealthRegistry()
    registry.add("a", lambda: True)
    registry.add("b", lambda: True)

    assert registry.remove("a") is True
    assert registry.remove("a") is False
    assert registry.names == ["b"]

    registry.clear()
    assert len(registry) == 0


def test_invalid_kind_is_rejected():
    registry = HealthRegistry()
    with pytest.raises(ValueError):
        registry.add("x", lambda: True, kind="sometimes")


def test_invalid_timeout_is_rejected():
    with pytest.raises(ValueError):
        HealthRegistry(timeout=0)


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------


async def test_empty_registry_is_healthy():
    report = await HealthRegistry().report()

    assert report.ok is True
    assert report.status == "ok"
    assert report.http_status == 200


async def test_passing_checks_report_ok():
    registry = HealthRegistry()
    registry.add("a", lambda: True)

    report = await registry.report()

    assert report.ok is True
    assert report.checks[0].name == "a"
    assert report.checks[0].healthy is True


async def test_critical_readiness_failure_is_503():
    registry = HealthRegistry()
    registry.add("db", lambda: False)

    report = await registry.report("readiness")

    assert report.ok is False
    assert report.ready is False
    assert report.status == "down"
    assert report.http_status == 503


async def test_non_critical_failure_is_degraded_but_ok():
    registry = HealthRegistry()
    registry.add("db", lambda: True)
    registry.add("cache", lambda: False, critical=False)

    report = await registry.report("readiness")

    assert report.ok is True
    assert report.ready is True
    assert report.status == "degraded"
    assert report.http_status == 200


async def test_liveness_failure_marks_the_report_down():
    registry = HealthRegistry()
    registry.add("event_loop", lambda: False, kind="liveness")

    report = await registry.report("liveness")

    assert report.live is False
    assert report.ok is False
    assert report.status == "down"


async def test_async_checks_are_awaited():
    registry = HealthRegistry()

    @registry.add("async")
    async def check() -> bool:
        return True

    assert (await registry.report()).ok is True


async def test_a_string_return_is_a_failure_reason():
    registry = HealthRegistry()
    registry.add("db", lambda: "connection refused")

    report = await registry.report()

    assert report.ok is False
    assert report.checks[0].detail == "connection refused"


async def test_an_exception_is_caught_and_reported():
    registry = HealthRegistry()

    def broken() -> bool:
        raise RuntimeError("kaboom")

    registry.add("broken", broken)

    report = await registry.report()

    assert report.ok is False
    assert report.checks[0].healthy is False
    assert "kaboom" in report.checks[0].detail


async def test_a_slow_check_times_out_instead_of_hanging():
    registry = HealthRegistry(timeout=0.01)

    @registry.add("hang")
    async def hang() -> bool:
        import asyncio

        await asyncio.Future()  # never resolves
        return True

    started = time.perf_counter()
    report = await registry.report()
    elapsed = time.perf_counter() - started

    assert report.ok is False
    assert "timed out" in report.checks[0].detail
    assert elapsed < 2.0


async def test_per_check_timeout_overrides_the_registry_default():
    registry = HealthRegistry(timeout=30)

    @registry.add("hang", timeout=0.01)
    async def hang() -> bool:
        import asyncio

        await asyncio.Future()
        return True

    report = await registry.report()

    assert report.ok is False


async def test_ready_and_live_helpers():
    registry = HealthRegistry()
    registry.add("db", lambda: True)
    registry.add("loop", lambda: True, kind="liveness")

    assert await registry.ready() is True
    assert await registry.live() is True


async def test_report_is_json_serialisable():
    registry = HealthRegistry()
    registry.add("db", lambda: True)

    report = await registry.report()

    payload = json.loads(report.to_json())

    assert payload["status"] == "ok"
    assert payload["checks"][0]["name"] == "db"
    assert "duration" in payload


# ---------------------------------------------------------------------------
# ASGI adapter
# ---------------------------------------------------------------------------


async def test_asgi_ready_path_returns_200():
    registry = HealthRegistry()
    registry.add("db", lambda: True)

    status, body = await call_asgi(registry.asgi_app(), "/healthz")

    assert status == 200
    assert body["status"] == "ok"


@pytest.mark.parametrize("path", ["/ready", "/readyz", "/health/ready"])
async def test_all_readiness_aliases_are_served(path):
    registry = HealthRegistry()
    registry.add("db", lambda: True)

    status, _ = await call_asgi(registry.asgi_app(), path)

    assert status == 200


@pytest.mark.parametrize("path", ["/live", "/livez", "/health/live"])
async def test_all_liveness_aliases_are_served(path):
    registry = HealthRegistry()

    status, _ = await call_asgi(registry.asgi_app(), path)

    assert status == 200


async def test_asgi_unknown_path_is_404():
    status, body = await call_asgi(HealthRegistry().asgi_app(), "/nope")

    assert status == 404
    assert body["status"] == "not_found"


async def test_asgi_rejects_post():
    status, _ = await call_asgi(
        HealthRegistry().asgi_app(), "/healthz", method="POST"
    )

    assert status == 405


async def test_asgi_head_has_no_body():
    app = HealthRegistry().asgi_app()
    sent = []

    async def send(message):
        sent.append(message)

    async def receive():
        return {"type": "http.request", "body": b""}

    await app(
        {"type": "http", "method": "HEAD", "path": "/healthz", "headers": []},
        receive,
        send,
    )

    assert sent[0]["status"] == 200
    assert sent[1]["body"] == b""


async def test_asgi_reports_503_when_down():
    registry = HealthRegistry()
    registry.add("db", lambda: False)

    status, body = await call_asgi(registry.asgi_app(), "/healthz")

    assert status == 503
    assert body["ok"] is False


# ---------------------------------------------------------------------------
# Adapters and ready-made checks
# ---------------------------------------------------------------------------


def test_aiohttp_handler_is_a_coroutine_function():
    import inspect

    handler = HealthRegistry().aiohttp_handler()

    assert inspect.iscoroutinefunction(handler)


def test_tcp_check_has_a_useful_name():
    check = tcp_check("example.invalid", 443)

    assert check.__name__ == "tcp_check(example.invalid:443)"


def test_queue_backlog_check_uses_pending():
    class Queue:
        def __init__(self, pending):
            self.pending = pending

    assert queue_backlog_check(Queue(3), max_pending=5)() is True
    assert queue_backlog_check(Queue(9), max_pending=5)() is False


def test_queue_backlog_check_falls_back_to_len():
    assert queue_backlog_check([], max_pending=1)() is True
    assert queue_backlog_check([1, 2], max_pending=1)() is False


def test_queue_backlog_check_validates_the_limit():
    with pytest.raises(ValueError):
        queue_backlog_check([], max_pending=0)


def test_report_http_status_property():
    assert HealthReport(status="ok", live=True, ready=True, ok=True).http_status == 200
    assert HealthReport(status="down", live=False, ready=False, ok=False).http_status == 503

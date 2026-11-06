import asyncio
import inspect
import logging
import random
import time
from contextlib import asynccontextmanager
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

import aiohttp

import darkob
from ...types import Event
from ..exceptions import (NetworkError, StopHandler, ServerError)
from .configs import PLATFORMS
from ...circuit import CircuitBreaker


class _RateLimited(Exception):
    """Internal signal: the endpoint asked us to slow down."""


_CAPITALIZED: Dict[str, str] = {}


def capitalize(text: str) -> str:
    """``message_updates`` -> ``MessageUpdates``, memoised.

    Called once per incoming update; update type names come from a
    small fixed set, so the string work is pure waste after the
    first occurrence.
    """
    cached = _CAPITALIZED.get(text)
    if cached is None:
        cached = "".join(word.title() for word in text.split("_"))
        _CAPITALIZED[text] = cached
    return cached

class Api:
    HEADERS = {
        "content-type": "application/json",
        "connection": "keep-alive",
    }

    def __init__(self, client: "darkob.Client") -> None:
        self.client = client
        self.max_retries = client.max_retries
        self.logger = logging.getLogger(__name__)
        self.headers = self.HEADERS.copy()
        self.headers["user-agent"] = client.user_agent

        platform = client.DEFAULT_PLATFORM["platform"]
        original_key = client._original_platform
        config = PLATFORMS.get(original_key, {}).get('headers', {})

        if platform == "Web":
            self.headers.update(config)
        elif platform == "Android":
            self.headers.pop("origin", None)
            self.headers.pop("referer", None)
            self.headers.update(config)
        else:
            self.headers.update(config)

        # TLS verification is on by default; clients may opt out explicitly
        # via Client(verify_ssl=False) when a proxy cannot verify upstreams.
        verify_ssl = getattr(client, "verify_ssl", True)
        connector = aiohttp.TCPConnector(ssl=verify_ssl, limit=100)
        self.session = aiohttp.ClientSession(
            connector=connector,
            headers=self.headers,
            timeout=aiohttp.ClientTimeout(total=client.timeout),
        )

        self.api_url = None
        self.wss_url = None
        self.ws = None

        self.api_map: Dict[str, str] = {}
        self.api_priority: List[str] = []
        self._api_code_by_url: Dict[str, str] = {}

        # Handler dispatch index: update name -> matching (func, handler) pairs.
        # Rebuilt only when the handler set changes, instead of scanning every
        # registered handler for every incoming update.
        self._dispatch_index: Optional[Dict[str, List[Tuple[Callable, Any]]]] = None
        self._dispatch_sig: Optional[Tuple[int, int]] = None
        self._background_tasks: Set["asyncio.Task"] = set()

        # Pooled sessions for file servers; a new ClientSession per
        # transfer meant a fresh TLS handshake for every file.
        self._aux_sessions: Dict[str, aiohttp.ClientSession] = {}

        # One breaker per endpoint, so a dead data centre stops being
        # retried by every subsequent request.
        self._breakers: Dict[str, CircuitBreaker] = {}

        # Exponential moving average of each endpoint's latency, so
        # the fastest healthy node is tried first.
        self._latency: Dict[str, float] = {}

    @staticmethod
    def _normalize_url(url: Optional[str]) -> Optional[str]:
        if not url:
            return None
        return url.rstrip("/")

    @staticmethod
    def _ensure_trailing_slash(url: str) -> str:
        return url if not url or url.endswith("/") else f"{url}/"

    async def close(self) -> None:
        for session in self._aux_sessions.values():
            if not session.closed:
                await session.close()
        self._aux_sessions.clear()

        if self.session and not self.session.closed:
            await self.session.close()

    @asynccontextmanager
    async def aux_session(
        self, base_url: str, verify_ssl: bool = True
    ):
        """Yield a pooled session for an auxiliary host (file servers).

        One session is kept per base URL for the client's lifetime and
        closed by :meth:`close`, so repeated downloads reuse the
        existing connection instead of paying a new TLS handshake.
        """
        session = self._aux_sessions.get(base_url)
        if session is None or session.closed:
            session = aiohttp.ClientSession(
                base_url=base_url,
                connector=aiohttp.TCPConnector(ssl=verify_ssl),
            )
            self._aux_sessions[base_url] = session

        yield session

    async def get_dcs(self, max_retries: int = 3, backoff: float = 1.0) -> bool:
        platform = self.client._original_platform
        platform_config = PLATFORMS.get(platform, {})
        url = platform_config.get('get_dcs_url', 'https://getdcmess.iranlms.ir/')

        for attempt in range(max_retries):
            try:
                async with self.session.get(url, proxy=self.client.proxy) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    data = json_data.get("data", {})
                    api_list = data.get("API", {})
                    socket_list = data.get("socket", {})

                    self.api_map = {}
                    for code, endpoint in api_list.items():
                        if not endpoint:
                            continue
                        normalized_code = str(code)
                        normalized_endpoint = self._ensure_trailing_slash(endpoint.rstrip("/"))
                        self.api_map[normalized_code] = normalized_endpoint

                    self._api_code_by_url = {
                        self._normalize_url(url): code
                        for code, url in self.api_map.items()
                        if self._normalize_url(url)
                    }

                    preferred_codes = []
                    default_api_code = data.get("default_api")
                    if default_api_code is not None:
                        default_api_code = str(default_api_code)

                    default_apis = data.get("default_apis") or []
                    for code in default_apis:
                        code_str = str(code)
                        if code_str in self.api_map and code_str not in preferred_codes:
                            preferred_codes.append(code_str)

                    if (
                        default_api_code
                        and default_api_code in self.api_map
                        and default_api_code not in preferred_codes
                    ):
                        preferred_codes.insert(0, default_api_code)

                    if not preferred_codes:
                        preferred_codes = list(self.api_map.keys())

                    self.api_priority = preferred_codes
                    self.api_url = self.api_map.get(self.api_priority[0]) if self.api_priority else None

                    self.wss_url = socket_list.get(data.get("default_socket"))

                    if self.api_url and self.wss_url:
                        return True
                    else:
                        raise ServerError("Server returned incomplete data.")

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                self.logger.warning(
                    f"Data Centers unreachable (attempt {attempt + 1}/{max_retries}): {e}"
                )
                if attempt < max_retries - 1:
                    await asyncio.sleep(backoff * (2**attempt))

        raise NetworkError(
            "Could not reach Data Centers after multiple attempts."
        )

    def _endpoint_candidates(self) -> List[str]:
        """Ordered, de-duplicated list of endpoints to try."""
        candidates: List[str] = []
        seen = set()

        def add(url_str: Optional[str]) -> None:
            if not url_str:
                return
            normalized = url_str.rstrip("/")
            if normalized not in seen:
                seen.add(normalized)
                candidates.append(normalized)

        add(self.api_url)
        for code in self.api_priority:
            add(self.api_map.get(code))
        for endpoint in self.api_map.values():
            add(endpoint)

        # Healthy nodes first, then the fastest measured one. The
        # discovery order stays as the tie-break.
        order = {url: index for index, url in enumerate(candidates)}
        return sorted(
            candidates,
            key=lambda url: (
                self.breaker_for(url).is_open(),
                self._latency.get(url, float('inf')),
                order[url],
            ),
        )

    def record_latency(self, endpoint: str, seconds: float) -> None:
        """Fold one measurement into the endpoint's moving average."""
        milliseconds = seconds * 1000.0
        previous = self._latency.get(endpoint)
        self._latency[endpoint] = (
            milliseconds if previous is None
            else previous * 0.8 + milliseconds * 0.2
        )

    def breaker_for(self, endpoint: str) -> CircuitBreaker:
        """Return (creating if needed) the breaker for an endpoint."""
        breaker = self._breakers.get(endpoint)
        if breaker is None:
            breaker = CircuitBreaker()
            self._breakers[endpoint] = breaker
        return breaker

    def _promote_endpoint(self, candidate: str) -> None:
        """Remember which endpoint just answered so we start there next time."""
        code = self._api_code_by_url.get(candidate)
        if not code:
            return
        if code in self.api_priority:
            self.api_priority.remove(code)
        self.api_priority.insert(0, code)
        self.api_url = self.api_map.get(code, candidate)

    async def _http_request(
        self,
        data: Dict,
        max_retries: int = 3,
        backoff: float = 1.0,
    ) -> Optional[Dict]:
        call = asyncio.current_task()
        candidates = self._endpoint_candidates()
        if not candidates:
            self.logger.error("No API endpoints known; cannot send request.")
            return None

        # Skip endpoints whose circuit is open.
        healthy = [c for c in candidates if self.breaker_for(c).allows_request()]
        if not healthy:
            self.logger.error(
                "All %d endpoints are circuit-open; skipping request.",
                len(candidates),
            )
            return None
        candidates = healthy

        # `max_retries` is a budget for this request, NOT per endpoint.
        # The previous implementation nested `for endpoint: for attempt:`,
        # which could fire len(endpoints) * max_retries requests and stall
        # for minutes when the network was down.
        policy = getattr(self.client, 'retry', None)
        if policy is not None:
            attempts_budget = max(1, int(policy.attempts))
            backoff = policy.backoff
        else:
            attempts_budget = max(1, int(max_retries))
        attempts = 0
        last_error: Any = None

        while attempts < attempts_budget:
            limiter = getattr(self.client, 'rate_limiter', None)
            if limiter is not None:
                await limiter.acquire()

            if asyncio.current_task() is not call:
                return None

            candidate = candidates[attempts % len(candidates)]
            # Back off once per full pass over the candidate list.
            if policy is not None:
                delay = policy.delay(attempts + 1)
            else:
                delay = backoff * (1 + attempts // len(candidates))

            started = time.perf_counter()
            try:
                async with self.session.post(
                    candidate, json=data, proxy=self.client.proxy
                ) as response:
                    if response.status == 429:
                        raise _RateLimited()

                    response.raise_for_status()
                    payload = await response.json()

                    if (
                        isinstance(payload, dict)
                        and payload.get("status") == "TOO_REQUESTS"
                    ):
                        raise _RateLimited()

                    self._promote_endpoint(candidate)
                    self.breaker_for(candidate).record_success()
                    self.record_latency(
                        candidate, time.perf_counter() - started
                    )
                    return payload

            except _RateLimited:
                last_error = "rate limited by the server"
                self.breaker_for(candidate).record_failure()
                if policy is not None:
                    delay = policy.delay(attempts + 1, rate_limited=True)
                else:
                    delay = self._RATE_LIMIT_BACKOFF * (2 ** min(attempts, 4))

                threshold = getattr(self.client, 'flood_sleep_threshold', 0) or 0
                if threshold and delay > threshold:
                    self.logger.error(
                        'Rate limited with a %.1fs wait, above the %.1fs '
                        'flood threshold; giving up on this request.',
                        delay, threshold,
                    )
                    return None
            except Exception as exc:
                last_error = exc
                self.breaker_for(candidate).record_failure()

            attempts += 1
            if attempts < attempts_budget:
                self.logger.warning(
                    "Request failed (attempt %d/%d) on %s: %s",
                    attempts, attempts_budget, candidate, last_error,
                )
                # Jitter avoids thundering-herd retries across processes.
                await asyncio.sleep(delay * (0.5 + random.random()))

        self.logger.error(
            "Request failed after %d attempt(s) across %d endpoint(s): %s",
            attempts, len(candidates), last_error,
        )
        return None

    #: Base delay (seconds) applied when the server signals rate limiting.
    _RATE_LIMIT_BACKOFF = 5.0

    def _build_dispatch_index(self) -> Dict[str, List[Tuple[Callable, Any]]]:
        """Group handlers by the update name they handle, once."""
        index: Dict[str, List[Tuple[Callable, Any]]] = {}
        handlers = self.client.handlers

        for func, handler in handlers.items():
            # Handler classes were previously instantiated for every incoming
            # event; instantiate once here instead.
            if isinstance(handler, type):
                try:
                    handler = handler()
                except Exception:
                    self.logger.exception(
                        "Could not instantiate handler %r", handler
                    )
                    continue

            name = getattr(handler, "__name__", None)
            if not name:
                continue
            index.setdefault(name, []).append((func, handler))

        self._dispatch_index = index
        self._dispatch_sig = (len(handlers), id(handlers))
        return index

    def invalidate_dispatch_index(self) -> None:
        """Drop the cached index so the next update rebuilds it."""
        self._dispatch_index = None
        self._dispatch_sig = None

    def _handlers_for(self, update_name: str) -> List[Tuple[Callable, Any]]:
        handlers = self.client.handlers
        signature = (len(handlers), id(handlers))

        if self._dispatch_index is None or self._dispatch_sig != signature:
            return self._build_dispatch_index().get(update_name, [])

        return self._dispatch_index.get(update_name, [])

    def _spawn(self, coro) -> None:
        """Run a coroutine in the background, keeping a strong reference."""
        task = asyncio.create_task(coro)
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)
        task.add_done_callback(self._log_task_failure)

    def _log_task_failure(self, task: "asyncio.Task") -> None:
        """Surface exceptions from fire-and-forget handlers.

        Without this, a failing handler only produced a
        "Task exception was never retrieved" warning at GC time, with
        no handler name and no immediate signal.
        """
        if task.cancelled():
            return
        error = task.exception()
        if error is not None:
            self.logger.error(
                "Background handler failed: %s",
                error,
                exc_info=error,
            )

    async def _execute_handler(self, func: Callable, event: Event) -> None:
        if inspect.iscoroutinefunction(func):
            if self.client.stop_on_first_match:
                await func(event)
            else:
                self._spawn(func(event))
            return

        # Blocking handler: use the loop's bounded executor rather than
        # spawning a brand-new OS thread for every single event.
        if self.client.stop_on_first_match:
            await asyncio.to_thread(func, event)
        else:
            self._spawn(asyncio.to_thread(func, event))

    async def handle_update(self, name: str, event: dict) -> None:
        # A pending ask() consumes the update before dispatch. Checking the
        # waiter count first avoids building an Event for every update when
        # no conversation is in flight.
        conversations = getattr(self.client, "_conversations", None)
        if conversations is not None and conversations.pending():
            if await conversations.resolve(Event(event.copy())):
                return

        # The update name is resolved once, not once per registered handler.
        targets = self._handlers_for(capitalize(name))
        if not targets:
            return

        for func, handler in targets:
            try:
                event_obj = Event(event.copy())

                if not await handler(event=event_obj):
                    continue

                await self._execute_handler(func, event_obj)

                if self.client.stop_on_first_match:
                    break
            except StopHandler:
                break
            except Exception as exc:
                self.logger.error(
                    "Handler '%s' failed: %s",
                    name,
                    exc,
                    extra={"data": event},
                    exc_info=True,
                )

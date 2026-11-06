import asyncio
import json
import time

from ..utils.http import retry_after_seconds
from ..utils.json_backend import loads
import logging
import darkob
from ..data import Data
from ..metrics import metrics as _metrics
from .exceptions import (
    APIException, Network,
    Timeout, BadGateway,
    JSONDecode, ServerError,
    InvalidInput, InvalidAccess,
    TooRequests,
)

logger = logging.getLogger(__name__)

class Response(Data):
    pass

class Request:
    async def request(
        self: "darkob.Bot",
        method: str,
        endpoint: str,
        **kwargs
    ):
        """
        Send an HTTP request to the Bot API with automatic retry and error mapping.

        Parameters:
            method (str): HTTP method, e.g. "POST" or "GET" (case-insensitive).
            endpoint (str): API method name appended to `base_url`, e.g. "getMe".
            **kwargs: Extra arguments passed to `aiohttp.ClientSession.request`, such as `json=` or `data=`.

        Returns:
            Response: The parsed API response.
        """
        if not _metrics.enabled:
            return await self._request(method, endpoint, **kwargs)

        _metrics.increment("darkob.api.requests")
        started = time.perf_counter()
        try:
            return await self._request(method, endpoint, **kwargs)
        finally:
            _metrics.observe("darkob.api.seconds", time.perf_counter() - started)

    async def _request(
        self: "darkob.Bot",
        method: str,
        endpoint: str,
        **kwargs
    ):
        """The request itself: retries, error mapping, limiter feedback, hooks."""
        url = f"{self.base_url}/{endpoint}"
        session = await self._get_session()
        last_error = None
        tracked = _metrics.enabled

        policy = getattr(self, 'retry', None)
        attempts = (
            max(1, int(policy.attempts)) if policy is not None
            else max(1, int(self.max_retries))
        )

        limiter = getattr(self, 'rate_limiter', None)

        # Plugins get one chance to rewrite the body, before any attempt is
        # made — not once per retry, which would compound a rewrite.
        manager = getattr(self, 'plugin_manager', None)
        hooks = manager is not None and bool(manager.active)
        if hooks:
            body = kwargs.get('json')
            if isinstance(body, dict):
                kwargs['json'] = await manager.apply_before_request(endpoint, body)

        for attempt in range(attempts):
            # Reset per attempt: a stale value would make a later throttle
            # inherit an earlier server's delay.
            retry_after = None

            if limiter is not None:
                payload = kwargs.get('json') or {}
                key = None
                if isinstance(payload, dict):
                    key = payload.get('chat_id') or payload.get('object_guid')
                await limiter.acquire(key)

            try:
                async with session.request(method.upper(), url, **kwargs) as resp:
                    text = (await resp.text()).strip()

                    if resp.status == 502:
                        raise BadGateway(dev_message="Server returned 502")

                    if resp.status == 500:
                        raise ServerError(dev_message="Server returned error")

                    if resp.status == 429:
                        # Folded into TooRequests so the limiter, the metrics
                        # and the caller all see one kind of throttle.
                        retry_after = retry_after_seconds(resp)
                        raise TooRequests(
                            dev_message=f"HTTP 429: {text[:200]}"
                        )

                    if resp.status >= 400:
                        raise APIException(
                            status=f"HTTP_{resp.status}",
                            dev_message=f"HTTP {resp.status}: {text[:500]}"
                        )

                    try:
                        data = loads(text)
                    except json.JSONDecodeError as e:
                        raise JSONDecode(
                            dev_message=f"Failed to parse JSON response. Raw: {text[:200]}"
                        ) from e

                    if isinstance(data, dict):
                        api_status = data.get('status', '')
                        error_message = data.get('dev_message')

                        if api_status != 'OK':
                            if api_status == 'SERVER_ERROR':
                                raise ServerError(dev_message=error_message)
                            elif api_status == 'INVALID_INPUT':
                                raise InvalidInput(dev_message=error_message)
                            elif api_status == 'INVALID_ACCESS':
                                raise InvalidAccess(dev_message=error_message)
                            elif api_status == 'TOO_REQUESTS':
                                retry_after = retry_after_seconds(resp)
                                raise TooRequests(dev_message=error_message)
                            elif api_status == 'Timeout':
                                raise Timeout(dev_message=error_message)
                            else:
                                raise APIException(status=api_status, dev_message=error_message)

                    # Success. An adaptive limiter climbs back here, and a
                    # plugin gets to rewrite the payload before the caller
                    # sees it.
                    on_success = getattr(limiter, "on_success", None)
                    if on_success is not None:
                        on_success()
                    if hooks:
                        data = await manager.apply_after_response(endpoint, data)

                    return Response(data)

            except TooRequests as exc:
                # The server is asking us to slow down. Without this the rate
                # limiter only ever sees the local bucket and never learns.
                if tracked:
                    _metrics.increment("darkob.api.ratelimited")
                on_throttle = getattr(limiter, "on_throttle", None)
                if on_throttle is not None:
                    on_throttle(retry_after)

                if tracked:
                    _metrics.increment("darkob.api.errors")
                if hooks:
                    await manager.run_on_error(
                        exc, {"action": endpoint, "endpoint": url}
                    )
                raise

            except (BadGateway, ServerError, Timeout, asyncio.TimeoutError) as e:
                if isinstance(e, asyncio.TimeoutError):
                    e = Timeout(dev_message=f"Request timed out after {self.timeout}s")

                if tracked:
                    _metrics.increment("darkob.api.errors")
                if hooks:
                    await manager.run_on_error(
                        e, {"action": endpoint, "endpoint": url}
                    )

                if attempt < attempts - 1:
                    if tracked:
                        _metrics.increment("darkob.api.retries")
                    logger.warning(
                        f"Request failed - Attempt {attempt + 1}/{attempts}: {type(e).__name__}"
                    )
                    await asyncio.sleep(
                        policy.delay(attempt + 1) if policy is not None
                        else 2 ** attempt
                    )
                    continue
                raise e from None

            except (JSONDecode, InvalidInput, InvalidAccess, APIException) as e:
                if tracked:
                    _metrics.increment("darkob.api.errors")
                if hooks:
                    await manager.run_on_error(
                        e, {"action": endpoint, "endpoint": url}
                    )
                raise

            except Exception as e:
                last_error = e
                if tracked:
                    _metrics.increment("darkob.api.errors")
                if hooks:
                    await manager.run_on_error(
                        e, {"action": endpoint, "endpoint": url}
                    )
                logger.warning(f"Request failed - Attempt {attempt + 1}/{attempts}: {e}")
                if attempt < attempts - 1:
                    if tracked:
                        _metrics.increment("darkob.api.retries")
                    await asyncio.sleep(
                        policy.delay(attempt + 1) if policy is not None
                        else 2 ** attempt
                    )
                    continue

        if last_error:
            raise Network(
                dev_message=f"Request failed after {attempts} attempts."
            ) from last_error
        raise Network(
            dev_message=f"Failed to call {endpoint} after {attempts} attempts."
        )

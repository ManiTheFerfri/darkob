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

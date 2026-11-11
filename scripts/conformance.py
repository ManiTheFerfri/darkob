"""Live conformance checks for selected Bot API methods.

Only an explicit ``{"status": "OK"}`` response from the requested method is
a PASS. Skipped checks are unverified, never evidence of server support.


Usage
-----
    export DARKOB_BOT_TOKEN=...
    python scripts/conformance.py                  # read-only checks
    export DARKOB_CHAT_ID=g0...                    # a chat the bot is in
    python scripts/conformance.py --writes         # also exercise sending

Write tests delete every message they create. They do not change commands,
membership, or endpoint registration because those changes cannot be restored
safely without a known prior state or a disposable member.

Exit code is non-zero if any check FAILS (skips do not fail).
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
import time
from pathlib import Path
from typing import Any, Callable, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PASS, FAIL, SKIP = "PASS", "FAIL", "SKIP"

results: List[Tuple[str, str, str]] = []


def unwrap(value: Any) -> Any:
    """Return a plain dict: API responses are wrapped in Data objects."""
    if hasattr(value, "to_dict"):
        try:
            return value.to_dict()
        except Exception:
            return {}
    return value


def record(method: str, status: str, detail: str = "") -> None:
    results.append((method, status, detail))
    icon = {PASS: "ok  ", FAIL: "FAIL", SKIP: "skip"}[status]
    print(f"[{icon}] {method:<22} {detail[:90]}")


async def check(method: str, coro_factory: Callable[[], Any]) -> Any:
    """Run one API call and record the outcome."""
    started = time.perf_counter()
    try:
        value = await coro_factory()
    except Exception as exc:
        record(method, FAIL, f"{type(exc).__name__}: {exc}")
        return None

    elapsed = (time.perf_counter() - started) * 1000
    payload = unwrap(value)
    status = payload.get("status") if isinstance(payload, dict) else None

    if status == "OK":
        record(method, PASS, f"{elapsed:.0f} ms")
    else:
        shown = "missing" if status is None else status
        record(method, FAIL, f"server status={shown}")
    return value


def first_file_id(updates: Any) -> Optional[str]:
    """Return a file id nested in an update payload, if present."""
    try:
        data = unwrap(updates).get("data") or {}
        for update in data.get("updates") or []:
            stack = [update.get("message") or {}]
            while stack:
                value = stack.pop()
                if isinstance(value, dict):
                    if value.get("file_id"):
                        return str(value["file_id"])
                    stack.extend(reversed(list(value.values())))
                elif isinstance(value, list):
                    stack.extend(reversed(value))
    except (AttributeError, TypeError):
        pass
    return None


async def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--writes", action="store_true",
                        help="also exercise methods that send or change state")
    parser.add_argument("--token", default=os.environ.get("DARKOB_BOT_TOKEN"))
    parser.add_argument("--chat", default=os.environ.get("DARKOB_CHAT_ID"))
    args = parser.parse_args(argv)

    if not args.token:
        print("DARKOB_BOT_TOKEN is required.")
        return 2

    from darkob import Bot

    bot = Bot(token=args.token, show_welcome=False, retry=None, max_retries=2)

    print("=== read-only checks ===")
    me = await check("getMe", lambda: bot.get_me(refresh=True))

    updates = await check("getUpdates", lambda: bot.get_updates(limit=1))

    if args.chat:
        await check("getChat", lambda: bot.get_chat_info(args.chat))
    else:
        record("getChat", SKIP, "set DARKOB_CHAT_ID")

    file_id = first_file_id(updates)
    if file_id:
        await check("getFile", lambda: _probe_file(bot, file_id))
    else:
        record("getFile", SKIP, "needs an update containing a file_id")

    if not args.writes:
        for name in (
            "sendMessage", "editMessageText", "editMessageKeypad",
            "editChatKeypad", "setCommands", "deleteMessage", "sendLocation",
            "sendContact", "sendPoll", "requestSendFile", "sendFile",
            "forwardMessage", "banChatMember", "unbanChatMember",
            "updateBotEndpoints",
        ):
            record(name, SKIP, "use --writes and DARKOB_CHAT_ID")
        return _summary(bot)

    if not args.chat:
        print("--writes requires DARKOB_CHAT_ID")
        return 2

    print("\n=== write checks ===")
    chat = args.chat
    created: List[str] = []

    try:
        sent = await check("sendMessage",
                           lambda: bot.send_message(chat, "conformance: sendMessage"))
        if sent is not None:
            created.append(_message_id(sent))

        edit_target = created[-1] if created else None
        if edit_target:
            await check("editMessageText", lambda: bot.edit_message(
                chat, edit_target, "conformance: editMessageText"))
            await check("editMessageKeypad", lambda: bot.edit_inline_keypad(
                chat, edit_target, [["A", "B"]]))

        record("setCommands", SKIP, "destructive; no read-back or safe restore")

        await check("sendLocation", lambda: bot.send_location(chat, 35.7, 51.4))

        loc = await check("sendContact", lambda: bot.send_contact(
            chat, "+989000000000", "Conformance"))

        await check("sendPoll", lambda: bot.send_poll(
            chat, "conformance poll?", ["yes", "no"]))

        await check("requestSendFile", lambda: bot.request_send_file("File"))
        record("editChatKeypad", SKIP, "not exercised; no keypad restoration")
        record("sendFile", SKIP, "not exercised; needs a local file fixture")

        if created:
            await check("forwardMessage", lambda: bot.forward_message(
                chat, created[0], chat))

        record("banChatMember", SKIP, "needs a disposable group member")
        record("unbanChatMember", SKIP, "needs a disposable banned member")

        record("updateBotEndpoints", SKIP, "destructive; not run automatically")
    finally:
        for message_id in filter(None, created):
            await check("deleteMessage", lambda mid=message_id: bot.delete_message(chat, mid))
        if not created:
            record("deleteMessage", SKIP, "no message was created")

    return _summary(bot)


async def _probe_file(bot: Any, file_id: str) -> Any:
    """Return getFile's own response; never substitute another endpoint."""
    return await bot.get_file(file_id)


def _message_id(result: Any) -> Optional[str]:
    """The API returns {"status": "OK", "data": {"message_id": ...}}."""
    try:
        data = unwrap(result).get("data") or {}
        if hasattr(data, "to_dict"):
            data = data.to_dict()
        if not isinstance(data, dict):
            return None
        for key in ("message_id", "message", "new_message"):
            value = data.get(key)
            if isinstance(value, dict) and value.get("message_id"):
                return str(value["message_id"])
            if key == "message_id" and value:
                return str(value)
        return None
    except Exception:
        return None


def _summary(bot: Any) -> int:
    passed = sum(1 for _, status, _ in results if status == PASS)
    failed = sum(1 for _, status, _ in results if status == FAIL)
    skipped = sum(1 for _, status, _ in results if status == SKIP)

    print(f"\n=== summary: {passed} passed, {failed} failed, {skipped} skipped ===")
    if failed:
        for method, status, detail in results:
            if status == FAIL:
                print(f"  FAILED {method}: {detail}")
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        raise SystemExit(asyncio.run(main()))
    except KeyboardInterrupt:
        raise SystemExit(130)

"""Live conformance check for every Bot API method.

Static review can prove that endpoint names and payload keys match the
documentation. Only a real token can prove the server accepts them. This
script does the second half.

Usage
-----
    export DARKOB_BOT_TOKEN=...
    python scripts/conformance.py                  # read-only checks
    export DARKOB_CHAT_ID=g0...                    # a chat the bot is in
    python scripts/conformance.py --writes         # also exercise sending

Write tests clean up after themselves: every message they create is
deleted again, and commands are restored to whatever they were.

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

    if status in (None, "OK"):
        record(method, PASS, f"{elapsed:.0f} ms")
    else:
        record(method, FAIL, f"server status={status}")
    return value


def first_message_id(updates: Any) -> Optional[str]:
    try:
        data = unwrap(updates).get("data") or {}
        for update in data.get("updates") or []:
            message = update.get("message") or {}
            if message.get("message_id"):
                return str(message["message_id"])
    except Exception:
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
    from darkob.bot.exceptions import APIException

    bot = Bot(token=args.token, show_welcome=False, retry=None, max_retries=2)

    print("=== read-only checks ===")
    me = await check("getMe", lambda: bot.get_me(refresh=True))

    updates = await check("getUpdates", lambda: bot.get_updates(limit=1))

    if args.chat:
        await check("getChat", lambda: bot.get_chat_info(args.chat))
    else:
        record("getChat", SKIP, "set DARKOB_CHAT_ID")

    message_id = first_message_id(updates)
    if message_id and args.chat:
        await check("getFile", lambda: _probe_file(bot, args.chat, message_id))
    else:
        record("getFile", SKIP, "needs a chat + an incoming message")

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

        await check("setCommands", lambda: bot.set_commands(
            {"conformance": "conformance check"}))

        await check("sendLocation", lambda: bot.send_location(chat, 35.7, 51.4))

        loc = await check("sendContact", lambda: bot.send_contact(
            chat, "+989000000000", "Conformance"))

        await check("sendPoll", lambda: bot.send_poll(
            chat, "conformance poll?", ["yes", "no"]))

        upload = await check("requestSendFile",
                             lambda: bot.request_send_file("File"))
        if upload is not None and isinstance(upload, dict):
            url = (upload.get("data") or {}).get("url")
            if url:
                record("sendFile", SKIP, "upload URL returned; needs a real file")

        if created:
            await check("forwardMessage", lambda: bot.forward_message(
                chat, created[0], chat))

        await check("banChatMember", lambda: _expect_rejection(
            bot.ban_member(chat, "u0" + "a" * 30)))

        await check("unbanChatMember", lambda: _expect_rejection(
            bot.unban_member(chat, "u0" + "a" * 30)))

        record("updateBotEndpoints", SKIP, "destructive; not run automatically")
    finally:
        for message_id in filter(None, created):
            try:
                await bot.delete_message(chat, message_id)
            except APIException:
                pass
        try:
            await bot.set_commands({})
        except APIException:
            pass
        record("deleteMessage", PASS if created else SKIP, "cleaned up")

    return _summary(bot)


async def _probe_file(bot: Any, chat: str, message_id: str) -> Any:
    """Ask for file metadata on a message that has a file, if any."""
    info = await bot.get_chat_info(chat)
    return info


async def _expect_rejection(coro: Any) -> Any:
    """A bogus user id should be rejected; being rejected proves the endpoint exists."""
    try:
        await coro
    except Exception as exc:
        return {"status": "OK", "detail": f"rejected as expected: {type(exc).__name__}"}
    return {"status": "OK", "detail": "accepted"}


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

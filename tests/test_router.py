"""Tests for composable routers."""

from __future__ import annotations

import pytest

from darkob import Bot, Router

from conftest import VALID_TOKEN


def make_bot() -> Bot:
    return Bot(token=VALID_TOKEN, show_welcome=False)


def registered(bot: Bot):
    return bot._registry._handlers


def test_decorators_record_routes_without_a_bot():
    router = Router("events")

    @router.message()
    async def on_message(bot, event):
        return None

    assert len(router.routes) == 1
    assert router.routes[0].kind == "on_message"
    assert router.routes[0].handler is on_message


def test_router_len_includes_children():
    parent = Router()
    child = Router()

    @child.message()
    async def handler(bot, event):
        return None

    parent.include_router(child)

    assert len(parent) == 1
    assert parent.children == (child,)


def test_apply_registers_on_the_bot():
    bot = make_bot()
    router = Router()

    @router.message()
    async def handler(bot, event):
        return None

    count = router.apply(bot)

    assert count == 1
    assert len(registered(bot)) == 1
    assert registered(bot)[0][1] is handler


def test_nested_routers_register_all_handlers():
    bot = make_bot()
    root = Router("root")
    admin = Router("admin")
    user = Router("user")

    @admin.command("ban")
    async def ban(bot, event):
        return None

    @user.message()
    async def say(bot, event):
        return None

    root.include_router(admin)
    root.include_router(user)

    assert root.apply(bot) == 2
    assert len(registered(bot)) == 2


def test_command_routes_carry_message_and_command_constraints():
    bot = make_bot()
    router = Router()

    @router.command("start")
    async def start(bot, event):
        return None

    router.apply(bot)

    constraints, handler = registered(bot)[0]
    assert handler is start
    # IsMessage + Command
    assert len(constraints) == 2


def test_bot_include_router_returns_the_router():
    bot = make_bot()
    router = Router()

    @router.update()
    async def handler(bot, event):
        return None

    assert bot.include_router(router) is router
    assert len(registered(bot)) == 1


def test_include_router_rejects_self_reference():
    router = Router()

    with pytest.raises(ValueError):
        router.include_router(router)


def test_include_router_rejects_non_router():
    bot = make_bot()

    with pytest.raises(TypeError):
        bot.include_router(object())


def test_including_the_same_child_twice_is_idempotent():
    parent = Router()
    child = Router()

    @child.message()
    async def handler(bot, event):
        return None

    parent.include_router(child)
    parent.include_router(child)

    assert parent.children == (child,)
    assert len(parent) == 1

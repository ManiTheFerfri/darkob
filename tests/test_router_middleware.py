"""Tests for router-scoped middleware."""

from __future__ import annotations

from darkob import Bot, Router

from conftest import VALID_TOKEN


def make_bot(**kwargs) -> Bot:
    return Bot(token=VALID_TOKEN, show_welcome=False, **kwargs)


def registered(bot: Bot):
    return bot._registry._handlers


async def test_router_middleware_wraps_its_handlers():
    bot = make_bot()
    order = []
    router = Router("r")

    @router.middleware()
    async def log(bot, event, call_next):
        order.append("before")
        await call_next()
        order.append("after")

    @router.command("ping")
    async def ping(bot, event):
        order.append("handler")

    bot.include_router(router)

    constraints, handler = registered(bot)[0]
    await handler(bot, {})

    assert order == ["before", "handler", "after"]


async def test_router_middleware_can_short_circuit():
    bot = make_bot()
    seen = []
    router = Router("r")

    @router.middleware()
    async def block(bot, event, call_next):
        seen.append("blocked")
        return None

    @router.message()
    async def handler(bot, event):
        seen.append("handler")

    bot.include_router(router)

    _, wrapped = registered(bot)[0]
    await wrapped(bot, {})

    assert seen == ["blocked"]


async def test_multiple_middlewares_run_in_registration_order():
    bot = make_bot()
    order = []
    router = Router("r")

    @router.middleware()
    async def first(bot, event, call_next):
        order.append("first-in")
        await call_next()
        order.append("first-out")

    @router.middleware()
    async def second(bot, event, call_next):
        order.append("second-in")
        await call_next()
        order.append("second-out")

    @router.message()
    async def handler(bot, event):
        order.append("handler")

    bot.include_router(router)

    _, wrapped = registered(bot)[0]
    await wrapped(bot, {})

    assert order == [
        "first-in",
        "second-in",
        "handler",
        "second-out",
        "first-out",
    ]


async def test_middleware_is_scoped_to_its_router():
    bot = make_bot()
    seen = []

    wrapped_router = Router("wrapped")
    plain_router = Router("plain")

    @wrapped_router.middleware()
    async def mw(bot, event, call_next):
        seen.append("mw")
        await call_next()

    @wrapped_router.message()
    async def wrapped_handler(bot, event):
        pass

    @plain_router.message()
    async def plain_handler(bot, event):
        pass

    bot.include_router(wrapped_router)
    bot.include_router(plain_router)

    for constraint, handler in registered(bot):
        await handler(bot, {})

    # Only one of the two handlers ran middleware.
    assert seen == ["mw"]


async def test_wrapped_handler_keeps_its_name():
    bot = make_bot()
    router = Router("r")

    @router.middleware()
    async def mw(bot, event, call_next):
        await call_next()

    @router.command("hello")
    async def hello(bot, event):
        pass

    bot.include_router(router)

    _, wrapped = registered(bot)[0]

    assert wrapped.__name__ == "hello"


async def test_router_without_middleware_registers_the_original_handler():
    bot = make_bot()
    router = Router("r")

    @router.message()
    async def handler(bot, event):
        pass

    bot.include_router(router)

    _, registered_handler = registered(bot)[0]

    assert registered_handler is handler


def test_middleware_decorator_returns_the_function():
    router = Router("r")

    @router.middleware()
    async def mw(bot, event, call_next):
        await call_next()

    assert callable(mw)
    assert len(router._middlewares) == 1

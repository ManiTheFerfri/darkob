"""Composable routers for grouping handlers into reusable modules.

A :class:`Router` collects handler decorators without needing a bot
instance, then registers everything in one go::

    from darkob import Router

    router = Router()

    @router.command("start")
    async def start(bot, event):
        await bot.send_message(event.chat_id, "hi")

    bot.include_router(router)

Routers nest, so a large bot can be split into feature modules that are
included from a single place::

    root = Router()
    root.include_router(admin_router)
    root.include_router(user_router)
    bot.include_router(root)

Routes are replayed through the bot's own decorators, so the constraints,
ordering and semantics are identical to declaring the handlers inline.
"""

from __future__ import annotations

import functools
from typing import Any, Callable, List, Optional, Tuple

__all__ = ["Router", "Route"]


class Route:
    """A single recorded handler declaration."""

    __slots__ = ("kind", "args", "kwargs", "handler")

    def __init__(
        self,
        kind: str,
        args: Tuple[Any, ...],
        kwargs: dict,
        handler: Callable,
    ) -> None:
        self.kind = kind
        self.args = args
        self.kwargs = kwargs
        self.handler = handler

    def __repr__(self) -> str:
        return f"Route(kind={self.kind!r}, handler={self.handler!r})"


class Router:
    """Groups handlers so they can be registered on a bot all at once."""

    __slots__ = ("name", "_routes", "_children", "_middlewares")

    def __init__(self, name: Optional[str] = None) -> None:
        self.name = name or f"router-{id(self):x}"
        self._routes: List[Route] = []
        self._children: List["Router"] = []
        self._middlewares: List[Callable] = []

    # -- introspection ----------------------------------------------------

    @property
    def routes(self) -> Tuple[Route, ...]:
        """The routes declared directly on this router."""
        return tuple(self._routes)

    @property
    def children(self) -> Tuple["Router", ...]:
        """Nested routers included in this one."""
        return tuple(self._children)

    def __len__(self) -> int:
        return len(self._routes) + sum(len(child) for child in self._children)

    def __repr__(self) -> str:
        return f"Router(name={self.name!r}, routes={len(self._routes)})"

    # -- declaration helpers ---------------------------------------------

    def _decorator(
        self, kind: str, args: Tuple[Any, ...], kwargs: dict
    ) -> Callable[[Callable], Callable]:
        def register(handler: Callable) -> Callable:
            self._routes.append(Route(kind, args, kwargs, handler))
            return handler

        return register

    def update(self, *constraints: Any) -> Callable[[Callable], Callable]:
        """Mirror of ``bot.on_update``."""
        return self._decorator("on_update", constraints, {})

    def message(self, *constraints: Any) -> Callable[[Callable], Callable]:
        """Mirror of ``bot.on_message``."""
        return self._decorator("on_message", constraints, {})

    def new_message(self, *constraints: Any) -> Callable[[Callable], Callable]:
        """Mirror of ``bot.on_new_message``."""
        return self._decorator("on_new_message", constraints, {})

    def edit_message(self, *constraints: Any) -> Callable[[Callable], Callable]:
        """Mirror of ``bot.on_edit_message``."""
        return self._decorator("on_edit_message", constraints, {})

    def delete_message(self, *constraints: Any) -> Callable[[Callable], Callable]:
        """Mirror of ``bot.on_delete_message``."""
        return self._decorator("on_delete_message", constraints, {})

    def callback(self, *constraints: Any) -> Callable[[Callable], Callable]:
        """Mirror of ``bot.on_callback``."""
        return self._decorator("on_callback", constraints, {})

    def command(
        self,
        name: Any = None,
        *constraints: Any,
        prefixes: Optional[List[str]] = None,
    ) -> Callable[[Callable], Callable]:
        """Mirror of ``bot.on_command``."""
        args = (name,) + constraints if name is not None else constraints
        kwargs = {"prefixes": prefixes} if prefixes is not None else {}
        return self._decorator("on_command", args, kwargs)

    def event_data(self, *constraints: Any) -> Callable[[Callable], Callable]:
        """Mirror of ``bot.on_event_data``."""
        return self._decorator("on_event_data", constraints, {})

    def middleware(self) -> Callable[[Callable], Callable]:
        """Wrap every handler in this router with a middleware.

        Middleware is called as ``middleware(bot, event, call_next)``;
        ``await call_next()`` continues the chain.
        """
        def register(func: Callable) -> Callable:
            self._middlewares.append(func)
            return func

        return register

    def _wrap(self, handler: Callable) -> Callable:
        """Apply this router's middleware chain around a handler."""
        if not self._middlewares:
            return handler

        chain = list(self._middlewares)

        async def wrapped(bot, event):
            async def run(index: int):
                if index >= len(chain):
                    return await handler(bot, event)

                middleware = chain[index]
                return await middleware(
                    bot, event, lambda: run(index + 1)
                )

            return await run(0)

        functools.update_wrapper(wrapped, handler)
        return wrapped

    # -- composition ------------------------------------------------------

    def include_router(self, router: "Router") -> "Router":
        """Nest ``router`` inside this one and return it."""
        if router is self:
            raise ValueError("A router cannot include itself.")
        if router in self._children:
            return router
        self._children.append(router)
        return router

    def apply(self, bot: Any) -> int:
        """Register every route (recursively) on ``bot``.

        Returns the number of handlers registered.
        """
        registered = 0

        for route in self._routes:
            decorator = getattr(bot, route.kind)
            decorator(*route.args, **route.kwargs)(self._wrap(route.handler))
            registered += 1

        for child in self._children:
            registered += child.apply(bot)

        return registered

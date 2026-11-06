"""Plugin development kit.

darkob's plugin system has two halves: lifecycle management (discovery,
dependencies, config, enable/disable) and **pipeline hooks** (a plugin
observing or rewriting traffic). Both live here, so a plugin author has one
import::

    from darkob.plugin import Plugin, PluginMeta

    class AntiSpam(Plugin):
        meta = PluginMeta(
            name="anti-spam",
            version="1.0.0",
            description="Drops messages matching a blocklist.",
            dependencies=(),
        )

        async def setup(self) -> None:
            self.blocked = set(self.get_config("words", []))

        async def on_update(self, event):
            if event.text.lower() in self.blocked:
                return True          # consume: no handler will see it
            return None              # let dispatch continue

Enable it on a bot::

    bot.plugin_manager.register_plugin(AntiSpam)
    await bot.plugin_manager.enable("anti-spam")

The four hooks
--------------

``on_update(event)``
    Runs for every incoming update, before any handler. Return ``True`` to
    consume it.

``before_request(action, data)``
    Runs before an API call is posted. Return a dict to replace the body —
    the place to inject headers, rewrite parameters, or veto a call.

``after_response(action, data)``
    Runs with a successful response payload. Return a replacement.

``on_error(error, context)``
    Runs when a request or handler fails. The place to report to an error
    tracker.

Hooks are no-ops in the base class, so a plugin that only implements
``setup()``/``teardown()`` keeps working untouched. A plugin that raises
inside a hook is logged and skipped rather than crashing the bot; set
``PluginManager(..., strict_hooks=True)`` to make hook failures propagate —
the right choice for a security plugin that must fail closed.

Testing a plugin
----------------

:class:`PluginTester` runs a plugin against a fake bot, with no network::

    from darkob.plugin import PluginTester

    async def test_anti_spam_consumes_blocked_words():
        async with PluginTester(AntiSpam) as tester:
            assert await tester.on_update(make_message("buy crypto")) is True
            assert await tester.on_update(make_message("hello")) is False
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, Type

from .bot.plugin import (
    Plugin,
    PluginDefinitionError,
    PluginLoadError,
    PluginManager,
    PluginMeta,
    create_plugin,
)
from .testing import FakeBot, FakeEvent, make_message

__all__ = [
    "Plugin",
    "PluginMeta",
    "PluginManager",
    "PluginLoadError",
    "PluginDefinitionError",
    "PluginTester",
    "create_plugin",
    "message",
    "HOOKS",
]

#: Every hook the pipeline calls, in the order they fire for one round trip.
HOOKS: Tuple[str, ...] = ("on_update", "before_request", "after_response", "on_error")


class PluginTester:
    """Drive a plugin's lifecycle and hooks without a real bot.

    Enables each plugin class against a :class:`~darkob.testing.FakeBot` and
    exposes the hook methods the client would call, so a plugin can be tested
    the same way it runs in production::

        tester = PluginTester(MyPlugin, config={"key": "value"})
        await tester.start()
        assert await tester.on_update(event) is None
        await tester.stop()

    Also usable as an async context manager, which enables on entry and
    disables on exit.
    """

    __slots__ = ("bot", "manager", "_registered", "_configs")

    def __init__(
        self,
        *plugin_classes: Type[Plugin],
        bot: Any = None,
        strict_hooks: bool = False,
        config: Optional[Dict[str, Dict[str, Any]]] = None,
    ) -> None:
        self.bot = bot if bot is not None else FakeBot()
        self.manager = PluginManager(
            self.bot,
            auto_discover=False,
            plugins_dir=None,
            strict_hooks=strict_hooks,
        )
        self._registered: List[str] = []
        self._configs: Dict[str, Dict[str, Any]] = {}

        for plugin_class in plugin_classes:
            identifier = self.manager.register_plugin(plugin_class)
            self._registered.append(identifier)
            if config and identifier in config:
                self._configs[identifier] = config[identifier]
                self.manager.set_config(identifier, config[identifier])

    # -- lifecycle --------------------------------------------------------

    async def start(self) -> "PluginTester":
        """Enable every registered plugin, in registration order."""
        for identifier in self._registered:
            if not self.manager.is_enabled(identifier):
                await self.manager.enable(identifier)
        return self

    async def stop(self) -> None:
        """Disable every enabled plugin."""
        await self.manager.disable_all()

    async def __aenter__(self) -> "PluginTester":
        return await self.start()

    async def __aexit__(self, *exc_info: Any) -> bool:
        await self.stop()
        return False

    # -- hook drivers -----------------------------------------------------

    async def on_update(self, event: Any) -> bool:
        """Run ``on_update`` across the enabled plugins."""
        return await self.manager.run_on_update(event)

    async def before_request(
        self, action: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run ``before_request`` and return the (possibly rewritten) body."""
        return await self.manager.apply_before_request(action, data)

    async def after_response(self, action: str, data: Any) -> Any:
        """Run ``after_response`` and return the (possibly rewritten) payload."""
        return await self.manager.apply_after_response(action, data)

    async def on_error(
        self, error: BaseException, context: Optional[Dict[str, Any]] = None
    ) -> None:
        """Run ``on_error`` across the enabled plugins."""
        await self.manager.run_on_error(error, context)

    # -- introspection ----------------------------------------------------

    def plugin(self, identifier: str) -> Optional[Plugin]:
        """The live instance of an enabled plugin."""
        return self.manager.get_plugin(identifier)

    @property
    def enabled(self) -> List[str]:
        """Identifiers of the enabled plugins, in enable order."""
        return self.manager.enabled_plugins

    @property
    def active(self) -> int:
        """How many plugins are enabled."""
        return self.manager.active

    def __repr__(self) -> str:
        return (
            f"PluginTester(enabled={self.manager.enabled_plugins}, "
            f"bot={type(self.bot).__name__})"
        )


def message(text: str = "", **kwargs: Any) -> FakeEvent:
    """Shortcut for :func:`darkob.testing.make_message`."""
    return make_message(text=text, **kwargs)

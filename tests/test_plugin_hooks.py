"""Tests for the plugin development kit and its pipeline hooks."""

from __future__ import annotations

import logging
from types import SimpleNamespace

import pytest

from darkob.bot.plugin import PluginManager
from darkob.client.core.api import Api
from darkob.plugin import HOOKS, Plugin, PluginMeta, PluginTester
from darkob.testing import make_message


class Recorder(Plugin):
    """A plugin that records every hook it is given."""

    meta = PluginMeta(name="recorder")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates = []
        self.requests = []
        self.responses = []
        self.errors = []
        self.consume = False

    async def setup(self) -> None:
        await super().setup()
        self.started = True

    async def teardown(self) -> None:
        await super().teardown()
        self.started = False

    async def on_update(self, event):
        self.updates.append(event)
        return True if self.consume else None

    async def before_request(self, action, data):
        self.requests.append((action, data))
        return {"rewritten": True}

    async def after_response(self, action, data):
        self.responses.append((action, data))
        return {"status": "REWRITTEN"}

    async def on_error(self, error, context):
        self.errors.append((error, context))


class Minimal(Plugin):
    """A plugin that only implements the lifecycle, not the hooks."""

    meta = PluginMeta(name="minimal")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.started = False

    async def setup(self) -> None:
        self.started = True


def test_hooks_are_noops_on_the_base_class():
    plugin = Plugin(bot=None)

    for hook in HOOKS:
        assert hasattr(plugin, hook)

    assert HOOKS == (
        "on_update",
        "before_request",
        "after_response",
        "on_error",
    )


async def test_base_hooks_return_nothing():
    plugin = Plugin(bot=None)

    assert await plugin.on_update(None) is None
    assert await plugin.before_request("x", {}) is None
    assert await plugin.after_response("x", {}) is None
    assert await plugin.on_error(ValueError("x"), {}) is None


# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------


async def test_tester_enables_and_disables_plugins():
    async with PluginTester(Recorder) as tester:
        assert tester.enabled == ["recorder"]
        assert tester.active == 1
        instance = tester.plugin("recorder")
        assert instance is not None
        assert instance.started is True

    assert tester.enabled == []


async def test_tester_config_is_applied():
    class Configured(Recorder):
        meta = PluginMeta(name="configured", default_config={"limit": 1})

    async with PluginTester(Configured, config={"configured": {"limit": 9}}) as tester:
        instance = tester.plugin("configured")

        assert instance.get_config("limit") == 9


def test_repr_is_useful():
    tester = PluginTester(Recorder)

    assert "recorder" not in repr(tester)  # not enabled yet
    assert "FakeBot" in repr(tester)


# ---------------------------------------------------------------------------
# Hook dispatch
# ---------------------------------------------------------------------------


async def test_on_update_can_consume_an_event():
    async with PluginTester(Recorder) as tester:
        tester.plugin("recorder").consume = True

        assert await tester.on_update(make_message("hi")) is True


async def test_on_update_returns_false_when_nothing_consumes():
    async with PluginTester(Recorder) as tester:
        tester.plugin("recorder").consume = False

        assert await tester.on_update(make_message("hi")) is False


async def test_before_request_rewrites_the_body():
    async with PluginTester(Recorder) as tester:
        result = await tester.before_request("sendMessage", {"method": "sendMessage"})

    assert result == {"rewritten": True}


async def test_before_request_chains_across_plugins():
    class Adder(Plugin):
        meta = PluginMeta(name="adder")

        async def before_request(self, action, data):
            return {"steps": data.get("steps", []) + ["adder"]}

    class Doubler(Plugin):
        meta = PluginMeta(name="doubler")

        async def before_request(self, action, data):
            return {"steps": data.get("steps", []) + ["doubler"]}

    async with PluginTester(Adder, Doubler) as tester:
        result = await tester.before_request("x", {})

    assert result == {"steps": ["adder", "doubler"]}


async def test_after_response_rewrites_the_payload():
    async with PluginTester(Recorder) as tester:
        result = await tester.after_response("getMe", {"status": "OK"})

    assert result == {"status": "REWRITTEN"}


async def test_on_error_reaches_every_plugin():
    async with PluginTester(Recorder) as tester:
        instance = tester.plugin("recorder")
        await tester.on_error(ValueError("nope"), {"action": "getMe"})

        assert len(instance.errors) == 1


# ---------------------------------------------------------------------------
# Failure isolation
# ---------------------------------------------------------------------------


class Broken(Plugin):
    meta = PluginMeta(name="broken")

    async def on_update(self, event):
        raise RuntimeError("hook exploded")

    async def before_request(self, action, data):
        raise RuntimeError("hook exploded")

    async def after_response(self, action, data):
        raise RuntimeError("hook exploded")

    async def on_error(self, error, context):
        raise RuntimeError("hook exploded")


async def test_a_broken_hook_does_not_break_the_bot(caplog):
    with caplog.at_level(logging.ERROR):
        async with PluginTester(Broken) as tester:
            assert await tester.on_update(make_message("hi")) is False
            assert await tester.before_request("x", {"a": 1}) == {"a": 1}
            assert await tester.after_response("x", {"b": 2}) == {"b": 2}
            await tester.on_error(ValueError("y"))

    assert "hook exploded" in caplog.text


async def test_strict_hooks_propagates():
    with pytest.raises(RuntimeError):
        async with PluginTester(Broken, strict_hooks=True) as tester:
            await tester.on_update(make_message("hi"))


async def test_a_non_dict_before_request_result_is_ignored():
    class Bad(Plugin):
        meta = PluginMeta(name="bad")

        async def before_request(self, action, data):
            return "not a dict"

    async with PluginTester(Bad) as tester:
        assert await tester.before_request("x", {"keep": 1}) == {"keep": 1}


# ---------------------------------------------------------------------------
# The fast path
# ---------------------------------------------------------------------------


async def test_plugins_that_do_not_override_a_hook_are_skipped():
    manager = PluginManager(
        bot=SimpleNamespace(), auto_discover=False, plugins_dir=None
    )
    manager.register_plugin(Minimal)
    await manager.enable("minimal")

    assert manager.active == 1
    assert manager._hook_plugins("on_update") == []
    assert await manager.run_on_update(make_message("hi")) is False


async def test_active_is_zero_without_plugins():
    manager = PluginManager(
        bot=SimpleNamespace(), auto_discover=False, plugins_dir=None
    )

    assert manager.active == 0
    assert await manager.run_on_update(make_message("hi")) is False


# ---------------------------------------------------------------------------
# Client integration
# ---------------------------------------------------------------------------


class CountingHandler:
    __name__ = "NewMessage"

    def __init__(self) -> None:
        self.calls = 0

    async def __call__(self, *, event):
        self.calls += 1
        return True


async def on_message(event):
    return None


def make_client(manager=None, handler=None):
    return SimpleNamespace(
        DEFAULT_PLATFORM={"platform": "PWA"},
        _original_platform="pwa",
        user_agent="test",
        max_retries=1,
        timeout=5,
        verify_ssl=False,
        proxy=None,
        stop_on_first_match=True,
        handlers={on_message: handler or CountingHandler()},
        _conversations=None,
        plugin_manager=manager,
    )


async def test_a_consuming_plugin_stops_dispatch():
    handler = CountingHandler()
    client = make_client(handler=handler)
    manager = PluginManager(client, auto_discover=False, plugins_dir=None)
    manager.register_plugin(Recorder)
    await manager.enable("recorder")
    manager.get_plugin("recorder").consume = True
    client.plugin_manager = manager

    api = Api(client)
    real = api.session
    try:
        await api.handle_update("new_message", {"text": "hi"})
    finally:
        await real.close()

    assert handler.calls == 0


async def test_a_non_consuming_plugin_lets_dispatch_continue():
    handler = CountingHandler()
    client = make_client(handler=handler)
    manager = PluginManager(client, auto_discover=False, plugins_dir=None)
    manager.register_plugin(Recorder)
    await manager.enable("recorder")
    client.plugin_manager = manager

    api = Api(client)
    real = api.session
    try:
        await api.handle_update("new_message", {"text": "hi"})
    finally:
        await real.close()

    assert handler.calls == 1


async def test_a_client_without_plugins_still_dispatches():
    handler = CountingHandler()
    api = Api(make_client(manager=None, handler=handler))
    real = api.session
    try:
        await api.handle_update("new_message", {"text": "hi"})
    finally:
        await real.close()

    assert handler.calls == 1

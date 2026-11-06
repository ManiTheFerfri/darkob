# Write a plugin

Package cross-cutting behaviour — filtering, rewriting, error reporting — as a `Plugin` with a lifecycle instead of another handler.

## A plugin is a class and some metadata

```python title="plugins/anti_spam.py"
from darkob.plugin import Plugin, PluginMeta


class AntiSpam(Plugin):
    meta = PluginMeta(
        name="anti-spam",
        version="1.0.0",
        description="Drops messages that contain blocked words.",
        dependencies=(),
        default_config={"words": ["buy crypto"]},
    )

    async def setup(self) -> None:
        self.blocked = {w.lower() for w in self.get_config("words", [])}

    async def on_update(self, event):
        text = (event.text or "").lower()
        if any(word in text for word in self.blocked):
            return True      # consume: no handler sees this update
        return None          # let dispatch continue
```

`PluginMeta` is a frozen dataclass:

| Field | Default | Purpose |
| --- | --- | --- |
| `name` | required | Identifier, lowercased on registration |
| `version` | `"1.0.0"` | Reported by `get_plugin_info` |
| `description` | `""` | Human-readable summary |
| `author` | `"Unknown"` | Reported by `get_plugin_info` |
| `homepage` | `None` | Reported by `get_plugin_info` |
| `dependencies` | `()` | Plugin names enabled before this one |
| `required_permissions` | `()` | Declarative only — **not** enforced by the manager |
| `default_config` | `{}` | Merged under the config you pass in |
| `enabled_by_default` | `False` | Picked up by `enable_defaults()` |

Without a `name`, the identifier falls back to the lowercased class name;
`register_plugin(MyPlugin, name="custom")` overrides both.

## Lifecycle and configuration

```python
async def setup(self) -> None:      # called by enable()
    ...

async def teardown(self) -> None:   # called by disable()
    ...

def configure(self, config: dict) -> dict:   # validate/rewrite config
    return config

self.get_config("words", [])        # one value
self.update_config({"words": []})   # merge over the defaults
self.is_ready                       # True between setup and teardown
```

A plugin receives its config at construction. `set_config()` on the manager
applies to a live instance too.

## The four hooks

| Hook | Signature | Return value |
| --- | --- | --- |
| `on_update` | `(event)` | `True` consumes the update; `None`/`False` continues |
| `before_request` | `(action, data)` | A dict replaces the request body; `None` keeps it |
| `after_response` | `(action, data)` | A replacement payload; `None` keeps it |
| `on_error` | `(error, context)` | Ignored |

Every hook is a no-op in the base class, so a plugin that only implements
`setup()`/`teardown()` keeps working. At dispatch, only the hooks a plugin
actually **overrides** are called, in the order the plugins were enabled.

```python title="plugins/audit.py"
class Audit(Plugin):
    meta = PluginMeta(name="audit")

    def __init__(self, bot, *, config=None):
        super().__init__(bot, config=config)
        self.seen = []

    async def before_request(self, action, data):
        if action == "sendMessage":
            return {**data, "disable_notification": True}
        return None                           # keep the original body

    async def after_response(self, action, data):
        self.seen.append(action)
        return None                           # keep the payload

    async def on_error(self, error, context):
        print("failed:", type(error).__name__, context.get("action"))
```

!!! warning "`before_request` must return a dict"
    Anything else is reported to the hook-failure path and ignored, and the
    original body is sent, so a typo in a rewrite hook cannot silently
    corrupt every request — but it also means the failure is quiet unless
    you watch the logs.

## Register and enable

```python
from plugins.anti_spam import AntiSpam

bot = Bot(token="YOUR_BOT_TOKEN")

identifier = bot.plugin_manager.register_plugin(AntiSpam)   # "anti-spam"
plugin = await bot.plugin_manager.enable(identifier)        # instance
```

`Bot(...)` creates the manager for you, so registration is one call.

!!! note "Where the hooks actually fire"
    The four hooks are called from the client's request and dispatch loop
    (`Messenger` / `Shad`). The `PluginManager` on a `Bot` handles the whole
    lifecycle — registration, dependencies, config, enable/disable, reload —
    and is what `PluginTester` drives, but `darkob.Bot`'s own update
    dispatch and its Bot-API request path do not currently call the hooks.

`register_plugin` returns the normalised identifier and raises
`PluginDefinitionError` for a class that does not subclass `Plugin`, an
empty name, or a duplicate.

`enable()` returns the live instance and, on the way, enables the plugin's
`dependencies` first. A failure in `setup()` raises `PluginLoadError` and
leaves the plugin disabled; a circular dependency raises `PluginLoadError`
too.

```python
bot.plugin_manager.is_registered("anti-spam")   # True
bot.plugin_manager.is_enabled("anti-spam")      # True
bot.plugin_manager.enabled_plugins              # ["anti-spam"]
bot.plugin_manager.get_plugin("anti-spam")      # the instance
await bot.plugin_manager.disable("anti-spam")   # teardown, returns bool
await bot.plugin_manager.disable_all()
await bot.plugin_manager.reload("anti-spam")    # re-executes the file
```

`disable()` refuses while another enabled plugin depends on this one, and
returns `False` instead of raising.

## Failure isolation

A plugin that raises inside a hook is logged and skipped; the bot keeps
running. Turn that off when a plugin must fail closed — a security filter
that breaks should stop traffic, not vanish:

```python
from darkob.plugin import PluginManager

manager = PluginManager(bot, auto_discover=False, strict_hooks=True)
manager.register_plugin(AntiSpam)
await manager.enable("anti-spam")
```

With `strict_hooks=True` the hook's exception propagates out of
`run_on_update`, `apply_before_request`, `apply_after_response` or
`run_on_error` instead of being swallowed.

!!! note "`PluginTester` accepts the same flag"
    `PluginTester(MyPlugin, strict_hooks=True)` wires the strict manager for
    you, which is the easiest way to assert that a hook *does* raise.

## Test it with `PluginTester`

`PluginTester` registers, enables and drives plugins against a
`FakeBot` — no token, no network:

```python title="tests/test_anti_spam.py"
from darkob.plugin import PluginTester
from darkob.testing import make_message
from plugins.anti_spam import AntiSpam


async def test_blocked_word_is_consumed():
    async with PluginTester(AntiSpam) as tester:
        assert await tester.on_update(make_message("buy crypto now")) is True
        assert await tester.on_update(make_message("hello")) is False


async def test_config_comes_from_the_meta_default():
    tester = PluginTester(AntiSpam)
    await tester.start()
    assert tester.plugin("anti-spam").blocked == {"buy crypto"}
    await tester.stop()
```

`PluginTester` can also drive the other three hooks — `before_request`,
`after_response`, `on_error` — plus `enabled` and `active`. Pass
`config={"anti-spam": {"words": ["spam"]}}` to override the defaults before
`setup()` runs.

## Discovery

`PluginManager(bot)` auto-discovers by default: it imports every `*.py` in
the `plugins/` directory next to your bot and every entry point registered
under the `rubika.plugins` group. Pass `auto_discover=False` (or
`plugins_dir=None`) to keep enabling explicit, which is what a test or a
small bot usually wants.

## See also

- [Handlers](../guides/handlers.md)
- [Errors](../guides/errors.md)
- [Architecture](../explanation/architecture.md)
- [Testing without a token](../tutorials/testing-without-a-token.md)
- [Project layout](../guides/project-layout.md)

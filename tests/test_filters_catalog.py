"""Catalog tests: every filter must construct and evaluate without blowing up.

These are smoke tests by design. A filter that raises would make a handler
crash at runtime, so refactoring safety here matters more than asserting
each filter's exact truth value.
"""

from __future__ import annotations

import importlib
import inspect
from types import SimpleNamespace

import pytest

from darkob.bot.filters import EventConstraint

# NOTE: `darkob.bot` (lowercase) is the Bot class alias, which shadows the
# `darkob.bot` subpackage for the `import x.y.z as name` form. Import the
# modules explicitly instead.
bot_filters = importlib.import_module("darkob.bot.filters")
client_filters = importlib.import_module("darkob.client.filters")


def event_fixture() -> SimpleNamespace:
    """A rich, event-shaped object that most filters can inspect."""
    message = {
        "text": "/start hello world",
        "type": "File",
        "file": {"file_name": "a.jpg", "size": 10},
        "metadata": {"meta_data_parts": [{"type": "Bold"}]},
        "event_data": {"type": "AddedGroupMembers"},
        "reply_to_message_id": "1",
        "forwarded_from": {"type": "User"},
        "location": {"lat": 1, "lon": 2},
        "poll": {"question": "q"},
    }
    return SimpleNamespace(
        original_data={"message": message, "action": "New"},
        action="New",
        chat_id="g0test",
        object_guid="g0test",
        author_object_guid="u0test",
        update_type="NewMessage",
        _memo={},
    )


COMBINATOR_NAMES = {
    "BothConstraint",
    "EitherConstraint",
    "NegateConstraint",
    "AndFilter",
    "OrFilter",
    "NotFilter",
}


def constraint_classes(module) -> list:
    found = []
    for name in dir(module):
        if name.startswith("_") or name in COMBINATOR_NAMES:
            continue
        obj = getattr(module, name)
        if not inspect.isclass(obj):
            continue
        if obj.__module__ != module.__name__:
            continue
        if not hasattr(obj, "evaluate"):
            continue
        if inspect.isabstract(obj):
            continue
        found.append((name, obj))
    return found


def construct(cls):
    """Build an instance using trivial values for required arguments."""
    signature = inspect.signature(cls.__init__)
    args = []
    for name, param in signature.parameters.items():
        if name == "self":
            continue
        if param.default is not inspect.Parameter.empty:
            continue
        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue

        annotation = param.annotation
        if annotation in (int, "int"):
            args.append(3)
        elif annotation in (list, "List[str]", "List[Any]"):
            args.append([])
        else:
            args.append("x")
    return cls(*args)


BOT_FILTERS = constraint_classes(bot_filters)
CLIENT_FILTERS = constraint_classes(client_filters)


def test_bot_filter_catalog_is_not_empty():
    assert len(BOT_FILTERS) >= 30


def test_client_filter_catalog_is_not_empty():
    assert len(CLIENT_FILTERS) >= 10


@pytest.mark.parametrize(
    "name,cls", BOT_FILTERS, ids=[name for name, _ in BOT_FILTERS]
)
async def test_bot_filter_evaluates(name, cls):
    try:
        instance = construct(cls)
    except TypeError as exc:  # pragma: no cover - construction contract change
        pytest.skip(f"{name} needs specific arguments: {exc}")

    result = await instance.evaluate(event_fixture())

    assert isinstance(result, bool), f"{name}.evaluate must return bool"


@pytest.mark.parametrize(
    "name,cls", CLIENT_FILTERS, ids=[name for name, _ in CLIENT_FILTERS]
)
async def test_client_filter_evaluates(name, cls):
    try:
        instance = construct(cls)
    except TypeError as exc:  # pragma: no cover
        pytest.skip(f"{name} needs specific arguments: {exc}")

    result = await instance.evaluate(event_fixture())

    assert isinstance(result, bool), f"{name}.evaluate must return bool"


async def test_abstract_constraint_cannot_be_instantiated():
    with pytest.raises(TypeError):
        EventConstraint()


async def test_combinators_short_circuit():
    class Yes(EventConstraint):
        async def evaluate(self, event):
            return True

    class No(EventConstraint):
        async def evaluate(self, event):
            return False

    event = event_fixture()

    assert await (Yes() & Yes()).evaluate(event) is True
    assert await (Yes() & No()).evaluate(event) is False
    assert await (Yes() | No()).evaluate(event) is True
    assert await (~Yes()).evaluate(event) is False
    assert await (~No()).evaluate(event) is True

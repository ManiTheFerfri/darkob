"""Tests for inline conversations (ask) and declarative states."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from darkob.converse import ConversationManager, NoReply, ask

_REAL_SLEEP = asyncio.sleep  # captured before the autouse fixture patches it


async def tick() -> None:
    """Yield to the event loop for one iteration."""
    await _REAL_SLEEP(0)
from darkob.fsm import FSMContext, MemoryStorage, StateFilter
from darkob.states import State, StatesGroup


def event(chat_id: str = "g1", text: str = "hello") -> SimpleNamespace:
    return SimpleNamespace(chat_id=chat_id, text=text)


class FakeOwner:
    def __init__(self) -> None:
        self._conversations = ConversationManager()
        self.sent = []

    async def send_message(
        self, chat_id, text, inline_keypad=None, chat_keypad=None
    ):
        # Mirrors the real Bot/Client signature so keyword forwarding can be
        # asserted rather than guessed.
        kwargs = {}
        if inline_keypad is not None:
            kwargs["inline_keypad"] = inline_keypad
        if chat_keypad is not None:
            kwargs["chat_keypad"] = chat_keypad
        self.sent.append((chat_id, text, kwargs))
        return {"status": "OK"}


# ---------------------------------------------------------------------------
# ConversationManager
# ---------------------------------------------------------------------------


async def test_resolve_hands_the_event_to_the_waiter():
    manager = ConversationManager()
    waiter = manager.register("g1")

    assert await manager.resolve(event("g1")) is True
    assert waiter.future.result().text == "hello"


async def test_resolve_ignores_other_chats():
    manager = ConversationManager()
    waiter = manager.register("g1")

    assert await manager.resolve(event("g2")) is False
    assert not waiter.future.done()


async def test_resolve_respects_filters():
    manager = ConversationManager()
    waiter = manager.register("g1", [lambda ev: ev.text.startswith("/")])

    assert await manager.resolve(event("g1", "hello")) is False
    assert await manager.resolve(event("g1", "/start")) is True
    assert waiter.future.result().text == "/start"


async def test_first_matching_waiter_wins():
    manager = ConversationManager()
    first = manager.register("g1")
    second = manager.register("g1")

    await manager.resolve(event("g1"))

    assert first.future.done(), "the oldest waiter is served first"
    assert not second.future.done()
    assert manager.pending("g1") == 1


async def test_pending_counts():
    manager = ConversationManager()
    manager.register("g1")
    manager.register("g1")
    manager.register("g2")

    assert manager.pending() == 3
    assert manager.pending("g1") == 2


async def test_cancel_all_cancels_every_waiter():
    manager = ConversationManager()
    waiter = manager.register("g1")

    manager.cancel_all()

    assert manager.pending() == 0
    assert waiter.future.cancelled()


async def test_event_without_a_chat_is_ignored():
    manager = ConversationManager()

    assert await manager.resolve(SimpleNamespace()) is False


# ---------------------------------------------------------------------------
# ask()
# ---------------------------------------------------------------------------


async def test_ask_returns_the_next_reply():
    owner = FakeOwner()

    task = asyncio.create_task(ask(owner, "g1", "your name?"))
    await tick()

    assert owner.sent == [("g1", "your name?", {})]

    reply = event("g1", "Ada")
    await owner._conversations.resolve(reply)

    assert await task is reply


async def test_ask_times_out_without_a_reply():
    owner = FakeOwner()

    with pytest.raises(NoReply):
        await ask(owner, "g1", "anyone?", timeout=0.01)

    assert owner._conversations.pending() == 0, "a timed-out waiter is removed"


async def test_ask_without_text_only_waits():
    owner = FakeOwner()

    task = asyncio.create_task(ask(owner, "g1", timeout=5))
    await tick()

    assert owner.sent == []
    await owner._conversations.resolve(event("g1", "spontaneous"))
    assert (await task).text == "spontaneous"


async def test_ask_forwards_keypads_when_supported():
    owner = FakeOwner()

    task = asyncio.create_task(
        ask(owner, "g1", "pick", inline_keypad="KB", timeout=5)
    )
    await tick()

    assert owner.sent[0][2] == {"inline_keypad": "KB"}
    owner._conversations.cancel_all()
    task.cancel()
    with pytest.raises((asyncio.CancelledError, NoReply)):
        await task


async def test_ask_without_a_registry_raises():
    class Bare:
        async def send_message(self, *a, **k):
            return None

    with pytest.raises(RuntimeError):
        await ask(Bare(), "g1", "hi")


# ---------------------------------------------------------------------------
# States
# ---------------------------------------------------------------------------


def test_state_is_a_string():
    class Form(StatesGroup):
        name = State()

    assert isinstance(Form.name, str)
    assert Form.name == "Form.name"


def test_states_are_namespaced_per_group():
    class Form(StatesGroup):
        name = State()

    class Survey(StatesGroup):
        name = State()

    assert Form.name != Survey.name
    assert str(Form.name) == "Form.name"
    assert str(Survey.name) == "Survey.name"


def test_states_and_values():
    class Form(StatesGroup):
        name = State()
        email = State()

    assert set(Form.values()) == {"Form.name", "Form.email"}
    assert {k: str(v) for k, v in Form.states().items()} == {
        "name": "Form.name",
        "email": "Form.email",
    }
    assert len(list(Form.all())) == 2


async def test_state_works_with_the_fsm():
    storage = MemoryStorage()
    ctx = FSMContext(storage, key="chat")

    class Form(StatesGroup):
        name = State()

    await ctx.set_state(Form.name)

    assert await ctx.get_state() == "Form.name"
    assert await StateFilter(storage, Form.name).evaluate(SimpleNamespace(chat_id="chat"))


def test_repr_is_readable():
    assert "Form.name" in repr(State("name", "Form"))

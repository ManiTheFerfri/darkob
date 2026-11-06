"""Declarative conversation states.

Plain strings work, but a class keeps the names together, typo-free and
greppable::

    from darkob import State, StatesGroup

    class Form(StatesGroup):
        name = State()
        email = State()

    await ctx.set_state(Form.name)          # stored as "Form.name"

``State`` is a ``str`` subclass, so it flows through every existing FSM
helper, ``StateFilter`` and storage backend without changes.
"""

from __future__ import annotations

from typing import Any, Dict, Iterator

__all__ = ["State", "StatesGroup"]


class State(str):
    """A named conversation state. Compares equal to its string form."""

    name: str
    owner: str

    def __new__(cls, name: str = "", owner: str = "") -> "State":
        value = f"{owner}.{name}" if owner else name
        instance = super().__new__(cls, value)
        instance.name = name  # type: ignore[attr-defined]
        instance.owner = owner  # type: ignore[attr-defined]
        return instance

    def __repr__(self) -> str:
        return f"State({str(self)!r})"


class StatesGroup:
    """Base class collecting ``State`` attributes into a namespace."""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        owner = cls.__name__
        for attribute, value in list(vars(cls).items()):
            if isinstance(value, State) and not value.owner:
                # The attribute name is the state name; State() alone cannot
                # know it because it is created before the class exists.
                setattr(cls, attribute, State(attribute, owner))

    @classmethod
    def states(cls) -> Dict[str, State]:
        """Every declared state, keyed by attribute name."""
        return {
            name: value
            for name, value in vars(cls).items()
            if isinstance(value, State)
        }

    @classmethod
    def all(cls) -> Iterator[State]:
        """Iterate the declared states."""
        return iter(cls.states().values())

    @classmethod
    def values(cls) -> Iterator[str]:
        """Iterate the wire strings of the declared states."""
        return iter(str(value) for value in cls.states().values())

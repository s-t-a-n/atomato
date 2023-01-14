from functools import total_ordering
from typing import SupportsInt
from typing import Type
from typing import Union

from .atomic_integer import AtomicInteger


StateType = Union[int]


@total_ordering
class AtomicState:
    """AtomicState allows to store a state in a threadsafe way."""

    _state: AtomicInteger
    _StateType: Type[StateType]

    def __init__(self, default_state: StateType, state_type: Type[StateType]):
        """Construct an `AtomicState`.

        Args:
            default_state: Default state that the AtomicState will be set to.
            state_type: Type that the AtomicState will wrap.
                        This type should be a type that supports integer conversion.
        """
        self._state = AtomicInteger(int(default_state))
        self._StateType = state_type

    def set(self, state: SupportsInt) -> StateType:
        """Set AtomicState to `state`.

        Args:
            state: State that the AtomicState will be set to (should support conversion to `int`)

        Returns:
            StateType: Return new state.
        """
        self._state.set(int(state))
        return self.state

    @property
    def state(self) -> StateType:
        """Return state of AtomicState.

        Returns:
            StateType: Return state.
        """
        return self._StateType(self._state.value)

    @property
    def tracker(self) -> "AtomicStateTracker":
        """Return `StateTracker` which only allows tracking the state.

        Returns:
            AtomicStateTracker: Return `StateTracker`.
        """
        return AtomicStateTracker(self)

    def __eq__(self, other: object) -> bool:
        if not hasattr(other, "__int__"):
            return NotImplemented
        return self._state == int(other)

    def __lt__(self, other: SupportsInt) -> bool:
        return int(self._state) < int(other)

    def __int__(self) -> int:
        return int(self._state)

    def __str__(self) -> str:
        return str(self._StateType(self.state))

    def __repr__(self) -> str:
        return f"AtomicState({str(self)})"


class AtomicStateTracker:
    """Encapsulation class for AtomicState that allows only tracking the state (disallowing setting it)."""

    _state: AtomicState

    def __init__(self, atomic_state: AtomicState):
        """Construct an `AtomicStateTracker`.

        Args:
            atomic_state: `AtomicState` that the AtomicStateTracker will track.
        """
        self._state = atomic_state

    @property
    def state(self) -> StateType:
        """Return state of AtomicStateTracker.

        Returns:
            StateType: Return state.
        """
        return self._state.state

    def __str__(self) -> str:
        return str(self.state)

    def __repr__(self) -> str:
        return f"AtomicStateTracker({str(self)})"

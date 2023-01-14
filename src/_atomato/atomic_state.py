from functools import total_ordering
from typing import Optional
from typing import SupportsInt
from typing import Type
from typing import Union

from .atomic_integer import AtomicInteger


StateType = Union[int, SupportsInt]


@total_ordering
class AtomicState:
    """AtomicState allows to store a state in a threadsafe way."""

    _state: AtomicInteger
    _StateType: Type[StateType]

    def __init__(
        self, default_state: StateType, state_type: Optional[Type[StateType]] = None
    ):
        """Construct an `AtomicState`.

        Args:
            default_state: Default state that the AtomicState will be set to.
            state_type: Integer convertible type that the AtomicState will wrap.
                        if left default (None), it will take the type of `default_state`
        """
        self._state = AtomicInteger(int(default_state))
        self._StateType = state_type if state_type else type(default_state)

    def set(self, state: StateType) -> StateType:
        """Set AtomicState to `state`.

        Args:
            state: State that the AtomicState will be set to (should support conversion to `int`)

        Returns:
            StateType: Return state after setting.
        """
        self._state.set(int(state))
        return self.state

    def reset(self) -> StateType:
        """Reset value of AtomicState to `default_state`.

        Returns:
            StateType: Return state after resetting.
        """
        self._state.reset()
        return self.state

    @property
    def state(self) -> StateType:
        """Return state of AtomicState.

        Returns:
            StateType: Return state.
        """
        return self._StateType(self._state.value)  # type: ignore

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

    def __lt__(self, other: StateType) -> bool:
        return int(self._state) < int(other)

    def __int__(self) -> int:
        return int(self._state)

    def __str__(self) -> str:
        return str(self.state)

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

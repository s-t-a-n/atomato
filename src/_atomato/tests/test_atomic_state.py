# type: ignore

from enum import Enum

import pytest

from atomato import AtomicState


def test_atomic_state_basics():
    class State(int, Enum):
        A = 0
        B = 1
        C = 2

    s = AtomicState(default_state=State.A)
    assert s.state == State.A

    assert str(s) == "State.A"
    assert repr(s) == "AtomicState(State.A)"

    assert int(s) == int(State.A)

    assert s == State.A
    assert State.B > s
    assert s < State.B

    s.set(State.B)
    assert s.state == State.B
    assert State.C > s
    assert State.A < s < State.C

    s.reset()
    assert s.state == State.A

    assert AtomicState(State.A) == AtomicState(State.A)
    assert AtomicState(State.A) < AtomicState(State.B)
    assert AtomicState(State.B) > AtomicState(State.A)

    s = AtomicState(State.A)
    assert str(s) == "State.A"
    assert repr(s) == "AtomicState(State.A)"


def test_atomic_state_type():
    class StateA(int, Enum):
        A = 0
        B = 1
        C = 2

    class StateB(int, Enum):
        A = 3
        B = 4
        C = 5

    s = AtomicState(default_state=StateA.A, state_type=StateB)

    with pytest.raises(ValueError) as excinfo:
        s.set(StateA.B)
    assert f"{StateA.B} is not a valid test_atomic_state_type.<locals>.StateB" in str(
        excinfo.value
    )


def test_custom_state():
    class State:
        v: int

        def __init__(self, v: int):
            self.v = v

        def __int__(self):
            return self.v

        def __eq__(self, other):
            return self.v == other

    s = AtomicState(State(0))
    assert s.state == 0
    assert type(s.state) is State
    assert type(s.reset()) is State
    assert AtomicState(State(1)) == 1


def test_atomic_state_tracker():
    class State(int, Enum):
        A = 0
        B = 1
        C = 2

    s = AtomicState(State.A)
    t = s.tracker

    assert t.state == State.A
    assert not hasattr(t, "set")
    assert str(t) == "State.A"
    assert repr(t) == "AtomicStateTracker(State.A)"

    s.set(State.B)
    assert t.state == State.B


def test_atomic_state_unqualified_inputs():
    class State(int, Enum):
        A = 0
        B = 1
        C = 2

    s = AtomicState(State.A)

    assert (s == object()) is False

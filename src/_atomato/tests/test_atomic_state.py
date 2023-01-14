# type: ignore

from enum import Enum

import pytest

from atomato import AtomicState


def test_atomic_state_basics():
    class State(int, Enum):
        A = (0,)
        B = (1,)
        C = 2

    s = AtomicState(default_state=State.A, state_type=State)
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
    # assert State.A < s < State.C


def test_atomic_state_tracker():
    class State(int, Enum):
        A = (0,)
        B = (1,)
        C = 2

    s = AtomicState(default_state=State.A, state_type=State)
    t = s.tracker

    assert t.state == State.A
    assert not hasattr(t, "set")
    assert str(t) == "State.A"
    assert repr(t) == "AtomicStateTracker(State.A)"

    s.set(State.B)
    assert t.state == State.B


def test_atomic_state_unqualified_inputs():
    class State(int, Enum):
        A = (0,)
        B = (1,)
        C = 2

    s = AtomicState(default_state=State.A, state_type=State)

    assert (s == object()) is False

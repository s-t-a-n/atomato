# type: ignore

from threading import Thread
from time import sleep

import pytest

from atomato import AtomicCounter


# def test_atomic_counter_bare_basics():
#
#     ctr = AtomicCounter()
#     ctr.inc(5)
#
#     ctr.wait_above(4)
#     ctr.wait_equal(5)
#     ctr.wait_below(6)


def test_atomic_counter_basics():
    ctr = AtomicCounter()

    assert ctr.value == 0
    ctr.inc()
    assert ctr.value == 1
    ctr.dec()
    assert ctr.value == 0

    from threading import Event

    rising_edge = Event()
    falling_edge = Event()

    def count_func(ctr: AtomicCounter):
        rising_edge.wait()
        for i in range(10):
            ctr.inc()
        falling_edge.wait()
        for i in range(10):
            ctr.dec()

    ctr = AtomicCounter()

    t1 = Thread(target=count_func, daemon=True, args=[ctr])
    t1.start()

    rising_edge.set()

    assert ctr.wait_above(0) is True
    assert ctr.wait_above(5) is True
    assert ctr.wait_equal(10) is True
    assert ctr.wait_below(11) is True

    falling_edge.set()

    assert ctr.wait_below(10) is True
    assert ctr.wait_below(2) is True
    assert ctr.wait_equal(0) is True
    assert ctr.value == 0

    ctr = AtomicCounter(1)
    assert ctr.value == 1

    assert ctr == 1
    assert ctr > 0
    assert ctr < 2

    assert AtomicCounter(1) == AtomicCounter(1)
    assert AtomicCounter(1) < AtomicCounter(2)
    assert AtomicCounter(2) > AtomicCounter(1)

    assert (ctr == object()) is False

    # test negative argument to `.inc()`
    ctr = AtomicCounter(0)
    assert ctr.inc(-1) == -1

    i = AtomicCounter(0)
    assert str(i) == "0"
    assert repr(i) == "AtomicCounter(0)"


def test_atomic_counter_wait_timeout():
    ctr = AtomicCounter()

    assert ctr.wait_above(0, timeout=0.0001) is False
    assert ctr.wait_below(-1, timeout=0.0001) is False
    assert ctr.wait_equal(1, timeout=0.0001) is False

    assert ctr.wait_equal(0) is True
    assert ctr.wait_below(1) is True
    assert ctr.wait_above(-1) is True


@pytest.mark.parametrize("default_value", [0, 1])
@pytest.mark.parametrize("allow_below_default", [True, False])
def test_atomic_counter_below_zero(allow_below_default: bool, default_value: int):
    # test `allow_below_zero` arg defaults to True
    ctr = AtomicCounter(default_value)
    assert ctr.dec() == default_value - 1

    ctr.reset()

    ctr.inc()
    assert ctr.reset() == default_value

    # test `allow_below_zero` arg when False
    ctr = AtomicCounter(default_value, allow_below_default=allow_below_default)
    if allow_below_default:
        assert ctr.dec() == default_value - 1
    else:
        assert ctr.dec() == default_value


def test_atomic_counter_lock():
    ctr = AtomicCounter()

    def concurrent(c: AtomicCounter):
        while c.value < 1:
            if not c._av._condition.acquire(blocking=False):
                c.inc()
            else:
                c._av._condition.release()

    def concurrent_with_context(c: AtomicCounter):
        while c.value < 1:
            with c:
                pass
                # sleep(0.0001)

    t1 = Thread(target=concurrent, args=[ctr])
    t1.start()
    t2 = Thread(target=concurrent_with_context, args=[ctr])
    t2.start()

    ctr.wait_above(0)
    assert ctr > 0

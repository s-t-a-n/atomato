# type: ignore

from threading import Thread
from time import sleep

import pytest

from atomatics import AtomicCounter


def test_atomic_counter_basics():
    ctr = AtomicCounter()

    assert ctr.value == 0
    ctr.inc()
    assert ctr.value == 1
    ctr.dec()
    assert ctr.value == 0

    def count_func(ctr: AtomicCounter):
        for i in range(10):
            sleep(0.001)
            ctr.inc()
        for i in range(10):
            sleep(0.001)
            ctr.dec()

    ctr = AtomicCounter()

    t1 = Thread(target=count_func, daemon=True, args=[ctr])
    t2 = Thread(target=count_func, daemon=True, args=[ctr])

    t1.start()
    t2.start()

    assert ctr.wait_above(1) is True
    assert ctr.wait_below(2) is True
    assert ctr.wait_equal(0) is True

    assert ctr.value == 0

    ctr = AtomicCounter(1)
    assert ctr.value == 1

    assert ctr == 1
    assert ctr > 0
    assert ctr < 2

    assert (ctr == object()) is False


def test_atomic_counter_wait_timeout():
    ctr = AtomicCounter()

    assert ctr.wait_above(0, timeout=0.01) is False
    assert ctr.wait_below(-1, timeout=0.01) is False
    assert ctr.wait_equal(1, timeout=0.01) is False

    assert ctr.wait_equal(0) is True
    assert ctr.wait_below(1) is True
    assert ctr.wait_above(-1) is True


@pytest.mark.parametrize("default_value", [0, 1])
@pytest.mark.parametrize("allow_below_default", [True, False])
def test_atomic_counter_below_zero(allow_below_default: bool, default_value: int):
    # test `allow_below_zero` arg defaults to True
    ctr = AtomicCounter(default_value)

    ctr.inc()
    assert ctr.reset() == default_value

    assert ctr.dec() == default_value - 1

    # test `allow_below_zero` arg when False
    ctr = AtomicCounter(default_value, allow_below_default=allow_below_default)
    if allow_below_default:
        assert ctr.dec() == default_value - 1
    else:
        assert ctr.dec() == default_value


def test_atomic_counter_lock():
    ctr = AtomicCounter()

    from time import sleep

    def concurrent(c: AtomicCounter):
        while c.value < 1:
            if not c._lock.acquire(blocking=False):
                c.inc()
            else:
                c._lock.release()

    def concurrent_with_context(c: AtomicCounter):
        while c.value < 1:
            with c:
                sleep(0.0001)

    t1 = Thread(target=concurrent, args=[ctr])
    t1.start()
    t2 = Thread(target=concurrent_with_context, args=[ctr])
    t2.start()

    ctr.wait_above(0)

    assert ctr > 0
    assert not t1.is_alive()
    assert not t2.is_alive()

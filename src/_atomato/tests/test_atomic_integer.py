# type: ignore

from atomato import AtomicInteger


def test_atomic_integer_basics():
    i = AtomicInteger(0)
    assert i == 0
    assert i.value == 0

    i = AtomicInteger(1)
    assert i == 1
    assert i.value == 1

    i = AtomicInteger(0)
    i.inc()
    assert i.value == 1

    i = AtomicInteger(0)
    assert i == 0
    i.set(2)
    assert i == 2

    assert AtomicInteger(1) == AtomicInteger(1)
    assert AtomicInteger(1) < AtomicInteger(2)
    assert AtomicInteger(2) > AtomicInteger(1)

    i = AtomicInteger(0)
    assert str(i) == "0"
    assert repr(i) == "AtomicInteger(0)"

# type: ignore
import pytest

from atomato import AtomicNumber


def test_atomic_integer_basics():
    i = AtomicNumber(0)
    assert i == 0
    assert i.value == 0

    i = AtomicNumber(1)
    assert i == 1
    assert i.value == 1

    assert type(AtomicNumber(0).value) == int
    assert type(AtomicNumber(0.0).value) == float
    # i.inc()
    # assert i.value == 1

    class MyNumber:
        def __int__(self):
            return 2

        def __float__(self):
            return 2.5

    assert type(AtomicNumber(MyNumber).value) == MyNumber
    assert int(AtomicNumber(MyNumber).value) == 2
    assert float(AtomicNumber(MyNumber).value) == 2.5

    class MyInt:
        def __int__(self):
            return 2

    with pytest.raises(TypeError) as excinfo:
        float(AtomicNumber(MyInt()))
    assert "float() argument must be a string or a real number, not 'MyInt'" in str(
        excinfo.value
    )

    i = AtomicNumber(0)
    assert i == 0
    i.set(2)
    assert i == 2

    assert AtomicNumber(1) == AtomicNumber(1)
    assert AtomicNumber(1) < AtomicNumber(2)
    assert AtomicNumber(2) > AtomicNumber(1)

    i = AtomicNumber(0)
    assert str(i) == "0"
    assert repr(i) == "AtomicNumber(0)"

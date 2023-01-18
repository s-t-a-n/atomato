from functools import total_ordering
from threading import Condition
from typing import Callable
from typing import Generic
from typing import Optional
from typing import TypeVar


T = TypeVar("T")


@total_ordering
class AtomicVariable(Generic[T]):
    """AtomicVariable allows to synchronize access for an underlying variable."""

    _condition: Condition
    _value: T

    def __init__(self, instance: T):
        """Construct an `AtomicVariable` for `instance`.

        Args:
            instance: instance that will be encapsulated in `AtomicVariable`.
        """
        self._condition = Condition()
        self._value = instance

    @property
    def value(self) -> T:
        """Return value of AtomicVariable.

        Returns:
            T: value of AtomicVariable
        """
        with self._condition:
            return self._value

    def wait_for(
        self, predicate: Callable[[T], bool], timeout: Optional[float] = None
    ) -> bool:
        """Wait for a value of an AtomicVariable by passing a `predicate`.

        Args:
            predicate: Function or lambda that takes a `T` and returns True if the predicate holds true.
            timeout: Wait time until predicate holds true or the passed `timeout` expired.

        Returns:
            bool: True if predicate is true. False if `timeout` has expired.

        Example:
            class MyClass:
                _v: int = 0

                def value(self) -> int:
                    return self._v


            a = AtomicVariable(MyClass())
            vb = a.wait_for(lambda mc: mc.value == 0)
            assert vb is True

            vb = a.wait_for(lambda mc: mc.value == 1, timeout=0.1)
            assert vb is False
        """
        with self._condition:
            return self._condition.wait_for(
                predicate=lambda: predicate(self._value), timeout=timeout
            )

    def set_by(self, setter: Callable[[T], None]) -> T:
        """Set value of AtomicVariable by using a passed function.

        Args:
            setter: Function or lambda that takes a `T` and uses its members to set a value.

        Returns:
            T: Value of AtomicVariable after setting it.

        Example:
            class MyClass:
                _v: object
                def set(self, v):
                    self._v = v

            a = AtomicVariable(int(0))
            v = a.set_by(lambda mc: mc.set(1))
            assert v == 1
        """
        with self._condition:
            setter(self._value)
            self._condition.notify_all()
            return self.value

    def set(self, value: T) -> T:
        """Set value of AtomicVariable.

        Args:
            value: Value that the AtomicInteger will be set to.

        Returns:
            T: Value of AtomicVariable after setting it.
        """
        with self._condition:
            self._value = value
            self._condition.notify_all()
            return self.value

    def __eq__(self, other: object) -> bool:
        return self.value == other

    def __lt__(self, other: T) -> bool:
        return self.value < other  # type: ignore

    def __int__(self) -> int:
        return int(self.value)  # type: ignore

    def __enter__(self) -> None:
        self._condition.acquire()

    def __exit__(self, etype, value, traceback) -> None:  # type: ignore
        self._condition.release()

    def __str__(self) -> str:
        return f"{self.value}"

    def __repr__(self) -> str:
        return f"AtomicVariable({str(self)})"

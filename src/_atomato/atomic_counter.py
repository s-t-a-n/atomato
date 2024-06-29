# class AtomicCounter:
#     pass

from functools import total_ordering

# from typing import Generic
# from typing import TypeVar
from typing import Callable
from typing import Dict
from typing import Generic
from typing import Optional
from typing import Protocol
from typing import SupportsFloat
from typing import SupportsInt
from typing import Type
from typing import TypeAlias
from typing import TypeVar
from typing import Union

from .atomic_number import AtomicNumber
from .protocols import ComparableNumber
from .protocols import Number
from .protocols import SupportComparison
from .protocols import SupportsComparableNumbers


# T = TypeVar("T", int, SupportsInt, float, SupportsFloat, SupportsOrdering)


T = TypeVar("T", bound=Number)


class AtomicCounter(Generic[T]):
    """AtomicCounter allows to count up and down in a threadsafe way."""

    _an: AtomicNumber[T]
    _default_value: T
    _allow_below_default: bool

    def __init__(
        self,
        default_value: T = 0,  # type: ignore
        allow_below_default: bool = True,
    ):
        """Construct an `AtomicCounter`.

        Args:
            default_value: Default value that the AtomicCounter will be set to.
            allow_below_default: If True allow decreasing the value below the default.
                                 If False, the lowest value will always be the default value.
        """
        # self._type = type(default_value)
        self._an = AtomicNumber(default_value)
        self._default_value = default_value
        self._allow_below_default = allow_below_default

    def _wait(self, predicate: str, d: Number, timeout: Optional[float]) -> bool:
        m: Dict[str, Callable[[Number, Number], bool]] = {
            "==": lambda x, y: bool(x == y),
            ">": lambda x, y: bool(x > y),
            "<": lambda x, y: bool(x < y),
            ">=": lambda x, y: bool(x >= y),
            "<=": lambda x, y: bool(x <= y),
        }
        assert predicate in m.keys(), f"predicate {predicate} not found in {m.keys()}"
        return bool(
            self._an.wait_for(predicate=lambda v: m[predicate](v, d), timeout=timeout)
        )

    def _set(self, d: Number) -> Number:
        with self._an:
            v: Number = (
                d
                if self._allow_below_default or d >= self._default_value
                else self._default_value
            )
            return self._an.set(v)

    def inc(self, d: Number = 1) -> Number:
        """Increase value of AtomicCounter by `d`.

        Args:
            d: Value with which to increase the AtomicCounter

        Returns:
            int: value after increasing by `d`
        """
        return self._set(self.value + d)

    def dec(self, d: Number = 1) -> Number:
        """Decrease value of AtomicCounter by `d`.

        Args:
            d: Value with which to decrease the AtomicCounter

        Returns:
            int: value after decreasing by `d`
        """
        return self._set(self.value - d)

    def reset(self) -> Number:
        """Reset value of AtomicCounter to `default_value` (0 if not specified to constructor).

        Returns:
            int: value after resetting to `default value`
        """
        return self._set(self._default_value)

    @property
    def value(self) -> Number:
        """Return value of AtomicCounter.

        Returns:
            int: value of AtomicCounter
        """
        return self._an.value

    def wait_equal(self, d: Number, timeout: Optional[float] = None) -> bool:
        """Wait until AtomicCounter has a value of `d` or if `timeout` expired.

        Args:
            d: Value to compare with
            timeout: Wait until `timeout` expired.
                     If `timeout` is None then blocks until condition is True (default: None)

        Returns:
            bool: Return True if AtomicCounter's value is equal to `d`, False if the timeout expired.
        """
        return self._wait(d=d, predicate="==", timeout=timeout)

    def wait_below(self, d: Number, timeout: Optional[float] = None) -> bool:
        """Wait until AtomicCounter has a value lower than `d` or if `timeout` expired.

        Args:
            d: Value to compare with
            timeout: Wait until `timeout` expired.
                    If `timeout` is None then blocks until condition is True (default: None)

        Returns:
            bool: Return True if AtomicCounter's value is below `d`, False if the timeout expired.
        """
        return self._wait(d=d, predicate="<", timeout=timeout)

    def wait_above(self, d: Number, timeout: Optional[float] = None) -> bool:
        """Wait until AtomicCounter has a value higher than `d` or if `timeout` expired.

        Args:
            d: Value to compare with
            timeout: Wait until `timeout` expired.
                     If `timeout` is None then blocks until condition is True (default: None)

        Returns:
            bool: Return True if AtomicCounter's value is above `d`, False if the timeout expired.
        """
        return self._wait(d=d, predicate=">", timeout=timeout)

    def __eq__(self, other: object) -> bool:
        if not hasattr(other, "__int__"):
            return NotImplemented
        return bool(self.value == other)

    def __lt__(self, other: Number) -> bool:
        return bool(self.value < other)

    def __ge__(self, other: Number) -> bool:
        return bool(self.value >= other)

    def __le__(self, other: Number) -> bool:
        return bool(self.value <= other)

    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def __enter__(self) -> None:
        self._an._condition.acquire()

    def __exit__(self, etype, value, traceback) -> None:  # type: ignore
        self._an._condition.release()

    def __str__(self) -> str:
        return f"{self.value}"

    def __repr__(self) -> str:
        return f"AtomicCounter({str(self)})"


# a = AtomicCounter(default_value=2)
# a.inc()
# assert a == 3


a: Number = 5.0
b: Number = 6
assert a < b

c: Number = 5
d: Number = 6
assert c - d

assert a < b

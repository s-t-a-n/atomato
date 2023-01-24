from functools import total_ordering

# from typing import Generic
# from typing import TypeVar
from typing import Callable
from typing import Dict
from typing import Optional
from typing import SupportsFloat
from typing import SupportsInt
from typing import Type
from typing import TypeAlias
from typing import Union

from .atomic_object import AtomicObject


# T =  IntOrFloat
# IntOrFloat: TypeAlias = IntOrFloat
IntOrFloat: TypeAlias = Union[int, SupportsInt, float, SupportsFloat]


@total_ordering
class AtomicCounter(SupportsInt, SupportsFloat):
    """AtomicCounter allows to count up and down in a threadsafe way."""

    _type: Type[IntOrFloat]
    _ao: AtomicObject[IntOrFloat]
    _default_value: IntOrFloat
    _allow_below_default: bool

    def __init__(
        self,
        default_value: int | float = 0,
        allow_below_default: bool = True,
    ):
        """Construct an `AtomicCounter`.

        Args:
            default_value: Default value that the AtomicCounter will be set to.
            allow_below_default: If True allow decreasing the value below the default.
                                 If False, the lowest value will always be the default value.
        """
        self._type = type(default_value)
        self._ao = AtomicObject(self._type(default_value))
        self._default_value = default_value
        self._allow_below_default = allow_below_default

    def _wait(self, predicate: str, d: IntOrFloat, timeout: Optional[float]) -> bool:
        m: Dict[str, Callable[[IntOrFloat, IntOrFloat], bool]] = {
            "==": lambda x, y: x == y,
            ">": lambda x, y: x > y,
            "<": lambda x, y: x < y,
            ">=": lambda x, y: x >= y,
            "<=": lambda x, y: x <= y,
        }
        assert predicate in m.keys(), f"predicate {predicate} not found in {m.keys()}"

        return self._ao.wait_for(
            predicate=lambda v: m[predicate](v, self._type(d)), timeout=timeout
        )

    def _set(self, d: IntOrFloat = 1) -> IntOrFloat:
        with self._ao:
            v = (
                self._type(d)
                if self._allow_below_default or self._type(d) >= self._default_value
                else self._default_value
            )
            self._ao.set(v)
            return v

    def inc(self, d: IntOrFloat = 1) -> IntOrFloat:
        """Increase value of AtomicCounter by `d`.

        Args:
            d: Value with which to increase the AtomicCounter

        Returns:
            int: value after increasing by `d`
        """
        return self._set(self.value + self._type(d))

    def dec(self, d: IntOrFloat = 1) -> IntOrFloat:
        """Decrease value of AtomicCounter by `d`.

        Args:
            d: Value with which to decrease the AtomicCounter

        Returns:
            int: value after decreasing by `d`
        """
        return self._set(self.value - self._type(d))

    def reset(self) -> IntOrFloat:
        """Reset value of AtomicCounter to `default_value` (0 if not specified to constructor).

        Returns:
            int: value after resetting to `default value`
        """
        return self._set(self._default_value)

    @property
    def value(self) -> IntOrFloat:
        """Return value of AtomicCounter.

        Returns:
            int: value of AtomicCounter
        """
        return self._ao.value

    def wait_equal(self, d: IntOrFloat, timeout: Optional[float] = None) -> bool:
        """Wait until AtomicCounter has a value of `d` or if `timeout` expired.

        Args:
            d: Value to compare with
            timeout: Wait until `timeout` expired.
                     If `timeout` is None then blocks until condition is True (default: None)

        Returns:
            bool: Return True if AtomicCounter's value is equal to `d`, False if the timeout expired.
        """
        return self._wait(d=d, predicate="==", timeout=timeout)

    def wait_below(self, d: IntOrFloat, timeout: Optional[float] = None) -> bool:
        """Wait until AtomicCounter has a value lower than `d` or if `timeout` expired.

        Args:
            d: Value to compare with
            timeout: Wait until `timeout` expired.
                    If `timeout` is None then blocks until condition is True (default: None)

        Returns:
            bool: Return True if AtomicCounter's value is below `d`, False if the timeout expired.
        """
        return self._wait(d=d, predicate="<", timeout=timeout)

    def wait_above(self, d: IntOrFloat, timeout: Optional[float] = None) -> bool:
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
        return self.value == self._type(other)  # type: ignore

    def __lt__(self, other: IntOrFloat) -> bool:
        return self._type(self.value) < self._type(other)

    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def __enter__(self) -> None:
        self._ao._condition.acquire()

    def __exit__(self, etype, value, traceback) -> None:  # type: ignore
        self._ao._condition.release()

    def __str__(self) -> str:
        return f"{self.value}"

    def __repr__(self) -> str:
        return f"AtomicCounter({str(self)})"

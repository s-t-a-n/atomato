from functools import total_ordering
from typing import Callable
from typing import Dict
from typing import Optional
from typing import SupportsInt
from typing import Union

from .atomic_object import AtomicObject


@total_ordering
class AtomicCounter:
    """AtomicCounter allows to count up and down in a threadsafe way."""

    _ao: AtomicObject[int]
    _default_value: int
    _allow_below_default: bool

    def __init__(
        self,
        default_value: Union[int, SupportsInt] = 0,
        allow_below_default: bool = True,
    ):
        """Construct an `AtomicCounter`.

        Args:
            default_value: Default value that the AtomicCounter will be set to.
            allow_below_default: If True allow decreasing the value below the default.
                                 If False, the lowest value will always be the default value.
        """
        self._ao = AtomicObject(int(default_value))
        self._default_value = int(default_value)
        self._allow_below_default = allow_below_default

    def _wait(
        self, predicate: str, d: Union[int, SupportsInt], timeout: Optional[float]
    ) -> bool:
        m: Dict[str, Callable[[int, int], bool]] = {
            "==": lambda x, y: x == y,
            ">": lambda x, y: x > y,
            "<": lambda x, y: x < y,
            ">=": lambda x, y: x >= y,
            "<=": lambda x, y: x <= y,
        }
        assert predicate in m.keys(), f"predicate {predicate} not found in {m.keys()}"

        return self._ao.wait_for(
            predicate=lambda v: m[predicate](v, int(d)), timeout=timeout
        )

    def _set(self, d: Union[int, SupportsInt] = 1) -> int:
        with self._ao:
            v = (
                int(d)
                if self._allow_below_default or int(d) >= self._default_value
                else self._default_value
            )
            self._ao.set(v)
            return v

    def inc(self, d: Union[int, SupportsInt] = 1) -> int:
        """Increase value of AtomicCounter by `d`.

        Args:
            d: Value with which to increase the AtomicCounter

        Returns:
            int: value after increasing by `d`
        """
        return self._set(self.value + int(d))

    def dec(self, d: Union[int, SupportsInt] = 1) -> int:
        """Decrease value of AtomicCounter by `d`.

        Args:
            d: Value with which to decrease the AtomicCounter

        Returns:
            int: value after decreasing by `d`
        """
        return self._set(self.value - int(d))

    def reset(self) -> int:
        """Reset value of AtomicCounter to `default_value` (0 if not specified to constructor).

        Returns:
            int: value after resetting to `default value`
        """
        return self._set(self._default_value)

    @property
    def value(self) -> int:
        """Return value of AtomicCounter.

        Returns:
            int: value of AtomicCounter
        """
        return self._ao.value

    def wait_equal(
        self, d: Union[int, SupportsInt], timeout: Optional[float] = None
    ) -> bool:
        """Wait until AtomicCounter has a value of `d` or if `timeout` expired.

        Args:
            d: Value to compare with
            timeout: Wait until `timeout` expired.
                     If `timeout` is None then blocks until condition is True (default: None)

        Returns:
            bool: Return True if AtomicCounter's value is equal to `d`, False if the timeout expired.
        """
        return self._wait(d=d, predicate="==", timeout=timeout)

    def wait_below(
        self, d: Union[int, SupportsInt], timeout: Optional[float] = None
    ) -> bool:
        """Wait until AtomicCounter has a value lower than `d` or if `timeout` expired.

        Args:
            d: Value to compare with
            timeout: Wait until `timeout` expired.
                    If `timeout` is None then blocks until condition is True (default: None)

        Returns:
            bool: Return True if AtomicCounter's value is below `d`, False if the timeout expired.
        """
        return self._wait(d=d, predicate="<", timeout=timeout)

    def wait_above(
        self, d: Union[int, SupportsInt], timeout: Optional[float] = None
    ) -> bool:
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
        return self.value == int(other)

    def __lt__(self, other: Union[int, SupportsInt]) -> bool:
        return int(self.value) < int(other)

    def __int__(self) -> int:
        return int(self.value)

    def __enter__(self) -> None:
        self._ao._condition.acquire()

    def __exit__(self, etype, value, traceback) -> None:  # type: ignore
        self._ao._condition.release()

    def __str__(self) -> str:
        return f"{self.value}"

    def __repr__(self) -> str:
        return f"AtomicCounter({str(self)})"

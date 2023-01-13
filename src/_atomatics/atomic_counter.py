from functools import total_ordering
from threading import Event
from threading import RLock
from time import time
from typing import Optional
from typing import SupportsInt


@total_ordering
class AtomicCounter:
    """AtomicCounter allows to count up and down in a threadsafe way."""

    _value: int
    _default_value: int
    _allow_below_default: bool

    _lock: RLock
    _event: Event

    def __init__(
        self, default_value: int | SupportsInt = 0, allow_below_default: bool = True
    ):
        """Construct an `AtomicCounter`.

        Args:
            default_value: Default value that the AtomicCounter will be set to.
            allow_below_default: If True allow decreasing the value below the default.
                                 If False, the lowest value will always be the default value.
        """
        self._value = int(default_value)
        self._default_value = int(default_value)
        self._allow_below_default = allow_below_default

        self._lock = RLock()
        self._event = Event()

    def _signal(self) -> None:
        self._event.set()
        self._event.clear()

    def _wait(self, op: str, d: int | SupportsInt, timeout: Optional[float]) -> bool:
        start = time()
        while timeout is None or timeout > 0:
            if any(
                [
                    op == "=" and self.value == int(d),
                    op == ">" and self.value > int(d),
                    op == "<" and self.value < int(d),
                ]
            ):
                return True
            timeout = timeout - (time() - start) if timeout else None
            self._event.wait(timeout)
        return False

    def inc(self, d: int | SupportsInt = 1) -> int:
        """Increase value of AtomicCounter by `d`.

        Args:
            d: Value with which to increase the AtomicCounter

        Returns:
            int: value after increasing by `d`
        """
        with self._lock:
            self._value += int(d)
            self._signal()
            return self._value

    def dec(self, d: int = 1) -> int:
        """Decrease value of AtomicCounter by `d`.

        Args:
            d: Value with which to decrease the AtomicCounter

        Returns:
            int: value after decreasing by `d`
        """
        return (
            self.inc(-d)
            if self._allow_below_default or self.value - d >= self._default_value
            else self.reset()
        )

    def reset(self) -> int:
        """Reset value of AtomicCounter to `default_value` (0 if not specified to constructor).

        Returns:
            int: value after resetting to `default value`
        """
        with self._lock:
            self._value = self._default_value
            return self._value

    @property
    def value(self) -> int:
        """Return value of AtomicCounter.

        Returns:
            int: value of AtomicCounter
        """
        with self._lock:
            return self._value

    def wait_equal(self, d: int | SupportsInt, timeout: Optional[float] = None) -> bool:
        """Wait until AtomicCounter has a value of `d` or if `timeout` expired.

        Args:
            d: Value to compare with
            timeout: Wait until `timeout` expired.
                     If `timeout` is None then blocks until condition is True (default: None)

        Returns:
            bool: Return True if AtomicCounter's value is equal to `d`, False if the timeout expired.
        """
        return self._wait(d=d, op="=", timeout=timeout)

    def wait_below(self, d: int | SupportsInt, timeout: Optional[float] = None) -> bool:
        """Wait until AtomicCounter has a value lower than `d` or if `timeout` expired.

        Args:
            d: Value to compare with
            timeout: Wait until `timeout` expired.
                    If `timeout` is None then blocks until condition is True (default: None)

        Returns:
            bool: Return True if AtomicCounter's value is below `d`, False if the timeout expired.
        """
        return self._wait(d=d, op="<", timeout=timeout)

    def wait_above(self, d: int | SupportsInt, timeout: Optional[float] = None) -> bool:
        """Wait until AtomicCounter has a value higher than `d` or if `timeout` expired.

        Args:
            d: Value to compare with
            timeout: Wait until `timeout` expired.
                     If `timeout` is None then blocks until condition is True (default: None)

        Returns:
            bool: Return True if AtomicCounter's value is above `d`, False if the timeout expired.
        """
        return self._wait(d=d, op=">", timeout=timeout)

    def __eq__(self, other: object) -> bool:
        if not hasattr(other, "__int__"):
            return NotImplemented
        return self.value == int(other)

    def __lt__(self, other: int | SupportsInt) -> bool:
        return int(self.value) < int(other)

    def __int__(self) -> int:
        return int(self.value)

    def __enter__(self) -> None:
        self._lock.acquire()

    def __exit__(self, etype, value, traceback) -> None:  # type: ignore
        self._lock.release()

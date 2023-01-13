from typing import SupportsInt

from .atomic_counter import AtomicCounter


class AtomicInteger(AtomicCounter):
    """AtomicState allows to store an integer in a threadsafe way."""

    def __init__(self, default_value: int | SupportsInt = 0):
        """Construct an `AtomicInteger`.

        Args:
            default_value: Default value that the AtomicInteger will be set to.
        """
        super().__init__(default_value)

    def set(self, d: int | SupportsInt = 0) -> int:
        """Set AtomicInteger to `d`.

        Args:
            d: Value that the AtomicInteger will be set to (should support conversion to `int`)

        Returns:
            int: Return new value.
        """
        with self._lock:
            self._value = int(d)
            return self._value

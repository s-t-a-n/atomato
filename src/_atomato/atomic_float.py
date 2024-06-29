# from typing import SupportsInt
# from typing import Union
#
# from .atomic_counter import AtomicCounter
#
#
# class AtomicFloat(AtomicCounter):
#     """AtomicFloat allows to store an integer in a threadsafe way."""
#
#     def __init__(self, default_value: float = 0.0):
#         """Construct an `AtomicFloat`.
#
#         Args:
#             default_value: Default value that the AtomicFloat will be set to.
#         """
#         super().__init__(default_value, allow_below_default=True)
#
#     def set(self, d: float = 0.0) -> float:
#         """Set AtomicFloat to `d`.
#
#         Args:
#             d: Value that the AtomicFloat will be set to (should support conversion to `int`)
#
#         Returns:
#             int: Return new value.
#         """
#         return float(self._set(d=float(d)))
#
#     def __str__(self) -> str:
#         return f"{self.value}"
#
#     def __repr__(self) -> str:
#         return f"AtomicFloat({str(self)})"

from typing import Generic
from typing import SupportsAbs
from typing import SupportsComplex
from typing import SupportsFloat
from typing import SupportsInt
from typing import TypeAlias
from typing import TypeVar
from typing import Union

from .atomic_object import AtomicObject
from .protocols import ComparableNumber
from .protocols import SupportComparison
from .protocols import SupportsComparableNumbers
from .protocols import SupportsNumbers


# AnyNumber = Union[int, float]
# AnySupportableNumber = Union[SupportsInt, SupportsFloat]
# AnyNumberOrSupportable = Union[AnyNumber | AnySupportableNumber]
# T = TypeVar('T',  int, float, complex)


T = TypeVar("T", bound=ComparableNumber)


class AtomicNumber(AtomicObject[T], SupportsNumbers):
    """ """

    def __float__(self) -> float:
        return float(self.value)

    def __repr__(self) -> str:
        return f"AtomicNumber({str(self.value)})"

    def __eq__(self, other: object) -> bool:
        if not hasattr(other, "__int__"):
            return NotImplemented
        return bool(self.value == other)

    def __lt__(self, other: ComparableNumber) -> bool:
        return bool(self.value < other)  # type: ignore

    def __ge__(self, other: ComparableNumber) -> bool:
        return bool(self.value >= other)  # type: ignore

    def __le__(self, other: ComparableNumber) -> bool:
        return bool(self.value <= other)  # type: ignore

    def __add__(self, other) -> bool:  # type: ignore
        pass

    def __sub__(self, other) -> bool:  # type: ignore
        pass

    def __mul__(self, other) -> bool:  # type: ignore
        pass


a: AtomicNumber[int] = AtomicNumber(5)

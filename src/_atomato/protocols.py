from abc import ABCMeta
from abc import abstractmethod
from typing import Any
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
from typing import runtime_checkable


# AnyNumber: TypeAlias = Union[int, SupportsInt, float, SupportsFloat]

# ComparableNumber: TypeAlias = Union['SupportsComparableNumbers', int, float]


# https://stackoverflow.com/a/68373816/18775667
@runtime_checkable
class SupportComparison(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other) -> bool:  # type: ignore
        pass

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        pass

    @abstractmethod
    def __ge__(self, other) -> bool:  # type: ignore
        pass

    @abstractmethod
    def __le__(self, other) -> bool:  # type: ignore
        pass


@runtime_checkable
class SupportArithmetics(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __add__(self, other) -> bool:  # type: ignore
        pass

    @abstractmethod
    def __sub__(self, other) -> bool:  # type: ignore
        pass

    @abstractmethod
    def __mul__(self, other) -> bool:  # type: ignore
        pass


# SupportsOrdering = TypeVar("SupportsOrdering", bound=Comparable)


class SupportsComparableNumbers(
    SupportsFloat, SupportComparison, Protocol, metaclass=ABCMeta
):
    pass


class SupportsNumbers(
    SupportsFloat, SupportComparison, SupportArithmetics, Protocol, metaclass=ABCMeta
):
    pass


ComparableNumber: TypeAlias = Union[int, float, SupportsComparableNumbers]
Number: TypeAlias = Union[int, float, SupportsNumbers]


a: ComparableNumber = 1
b: ComparableNumber = 1.5

# T = TypeVar("T", int, SupportsInt, float, SupportsFloat)


# class AtomicCounter(SupportsInt, SupportsFloat, SupportsOrdering):
#     def __lt__(self: 'SupportsOrdering', other: 'SupportsOrdering') -> bool:
#         return True
#
#     def __eq__(self: 'SupportsOrdering', other: object) -> bool:
#         return True
#
#     def __ge__(self: 'SupportsOrdering', other: 'SupportsOrdering') -> bool:
#         return True
#
#     def __le__(self: 'SupportsOrdering', other: 'SupportsOrdering') -> bool:
#         return True

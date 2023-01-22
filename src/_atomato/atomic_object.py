from functools import total_ordering
from inspect import isclass
from threading import Condition
from typing import Any
from typing import Callable
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union


T = TypeVar("T")


@total_ordering
class AtomicObject(Generic[T]):
    """AtomicObject allows to synchronize access for an underlying variable."""

    _condition: Condition
    _object: T

    def __init__(
        self, obj: Union[T, Type[T]], *args: List[Any], **kwargs: Dict[str, Any]
    ):
        """Construct an `AtomicObject` for `instance` by inline creating .

        Example:
            AtomicObject(MyClass(foo="a bit bar, but not too much"))

        Args:
            obj: instance that will be encapsulated in `AtomicObject`.
        """
        self._condition = Condition()
        self._object = obj(*args, **kwargs) if isclass(obj) else obj

    @property
    def value(self) -> T:
        """Return value of AtomicObject.

        Returns:
            T: value of AtomicObject
        """
        with self._condition:
            return self._object

    def wait_for(
        self, predicate: Callable[[T], bool], timeout: Optional[float] = None
    ) -> bool:
        """Wait for a value of an AtomicObject by passing a `predicate`.

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


            a = AtomicObject(MyClass())
            vb = a.wait_for(lambda mc: mc.value == 0)
            assert vb is True

            vb = a.wait_for(lambda mc: mc.value == 1, timeout=0.1)
            assert vb is False
        """
        with self._condition:
            return self._condition.wait_for(
                predicate=lambda: predicate(self._object), timeout=timeout
            )

    def set_by(self, setter: Callable[[T], None]) -> T:
        """Set value of AtomicObject by using a passed function.

        Args:
            setter: Function or lambda that takes a `T` and uses its members to set a value.

        Returns:
            T: Value of AtomicObject after setting it.

        Example:
            class MyClass:
                _v: object
                def set(self, v):
                    self._v = v

            a = AtomicObject(int(0))
            v = a.set_by(lambda mc: mc.set(1))
            assert v == 1
        """
        with self._condition:
            setter(self._object)
            self._condition.notify_all()
            return self.value

    def set(self, value: T) -> T:
        """Set value of AtomicObject.

        Args:
            value: Value that the AtomicInteger will be set to.

        Returns:
            T: Value of AtomicObject after setting it.
        """
        with self._condition:
            self._object = value
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
        return f"AtomicObject({str(self)})"

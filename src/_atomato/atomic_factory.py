# import asyncio
# from functools import total_ordering
# from threading import Condition
# from threading import Event
# from threading import RLock
# from time import time
# from typing import Callable
# from typing import Optional
# from typing import SupportsInt
# from typing import Union
# from typing import *
#
# from threading import current_thread, Thread
#
# from _atomato.atomic_counter import AtomicCounter
#
# T = TypeVar('T')
# class AtomicFactory(Generic[T]):
#     """"""
#     _type: Type[T]
#     _instances: Dict[int, T]
#     _lock: RLock
#     _unsafe_dict: bool = False
#
#     def __init__(self, type: Type[T], unsafe_dict: bool = False) -> None:
#         self._type = type
#         self._instances = {}
#         self._lock = RLock()
#         self._unsafe_dict = unsafe_dict
#
#     def thread_instance(self, *args, **kwargs) -> T:
#         thread_id = current_thread()
#
#         if self._unsafe_dict:
#             self._lock.acquire()
#
#         if not thread_id in self._instances.keys():
#             self._instances[thread_id] = self._type(*args, **kwargs)
#
#         if self._unsafe_dict:
#             with self._lock:
#                 return self._instances[thread_id]
#         return self._instances[thread_id]
#
#     def call_all_instances(self, f: Callable[[T], None]) -> None:
#         if self._unsafe_dict:
#             self._lock.acquire()
#
#         for instance in self._instances.values():
#             # print(f"calling instance: {instance}")
#             f(instance)
#
#         if self._unsafe_dict:
#             self._lock.release()
#
#
#
# # af = AtomicFactory(AtomicCounter)
# #
# # ac1 = af.thread_instance()
# # ac2 = af.thread_instance()
# # assert ac1 == ac2
# #
# # af = AtomicFactory(AtomicCounter)
# # ac1 = af.thread_instance(1)
# # assert ac1.value == 1
# #
# # ac_main_thread = af.thread_instance()
# #
# # def main(af: AtomicFactory[AtomicCounter]):
# #     ac = af.thread_instance()
# #     assert type(ac) is AtomicCounter
# #     assert af.thread_instance() == ac
# #
# #     ac.wait_equal(d=1)
# #
# # af = AtomicFactory(AtomicCounter)
# # [t.start() for t in [Thread(target=main, args=[af]) for _ in range(10)]]
# #
# # af.call_all_instances(f=lambda c: c.inc())
# #
# # for instance in af._instances.values():
# #     assert instance.value == 1
# # exit(0)

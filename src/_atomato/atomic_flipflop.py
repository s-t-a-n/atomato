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
# # from _atomato.singletons import ThreadedSingleton
#
# get_locked = AtomicCounter()
# set_locked = AtomicCounter()
#
# class FlipFlop():
#     event: Event
#     on_blocked_event: Event
#     get_lock: RLock
#     set_lock: RLock
#
#     def __init__(self):
#         self.event = Event()
#         self.on_blocked_event = Event()
#         self.get_lock = RLock()
#         self.set_lock = RLock()
#         self.set()
#
#     def set(self):
#         with self.set_lock:
#             set_locked.inc()
#             if not self.get_lock.acquire(blocking=False):
#                 self.on_blocked_event.set()
#             else:
#                 self.get_lock.release()
#             self.event.set()
#
#
#     def wait(self):
#         is_done = False
#
#         while not is_done:
#             with self.get_lock:
#                 get_locked.inc()
#                 self.event.wait()
#                 is_done = True
#
#                 with self.set_lock:
#                     set_locked.inc()
#                     if self.on_blocked_event.is_set():
#                         self.on_blocked_event.clear()
#                         self.event.set()
#                         return
#                     else:
#                         self.event.clear()
#
#
#
#
# from .atomic_factory import AtomicFactory
#
#
# class AtomicFlipFlop:
#     """AtomicFlipFlop allows to synchronize get and set requests."""
#
#     # _map: Dict[int, FlipFlop]
#     # _map_lock: RLock
#     _factory: AtomicFactory[FlipFlop]
#
#     def __init__(self):
#         self._factory = AtomicFactory(FlipFlop, unsafe_dict=True)
#
#     def _flipflop(self) -> FlipFlop:
#         return self._factory.thread_instance()
#
#         # t = current_thread()
#         #
#         # with self._map_lock:
#         #     if t not in self._map.keys():
#         #         print(f"cachemiss: creating FlipFlop for thread {t}")
#         #         self._map[t] = FlipFlop()
#         #     return self._map[t]
#
#     def wait(self):
#         flipflop = self._flipflop()
#         flipflop.wait()
#
#     def set(self):
#         # with self._map_lock:
#
#         self._factory.call_all_instances(lambda f: f.set())
#         # for flipflop in self._map.values():
#         #     flipflop.set()
#
#
# # class AtomicFlipFlop:
# #     """AtomicFlipFlop allows to synchronize get and set requests."""
# #
# #     _condition: Condition
# #
# #     def __init__(self):
# #         self._condition = Condition()
# #
# #     # def _flipflop(self) -> FlipFlop:
# #     #     return self._factory.thread_instance()
# #
# #         # t = current_thread()
# #         #
# #         # with self._map_lock:
# #         #     if t not in self._map.keys():
# #         #         print(f"cachemiss: creating FlipFlop for thread {t}")
# #         #         self._map[t] = FlipFlop()
# #         #     return self._map[t]
# #
# #     def get(self, predicate: Callable[[], Any]):
# #         with self._condition:
# #             print("wait")
# #             self._condition.wait()
# #             return predicate()
# #             print("unlock")
# #
# #     def wait(self):
# #         with self._condition:
# #             print("wait")
# #             self._condition.wait()
# #             print("unlock")
# #
# #     def set(self):
# #         # with self._map_lock:
# #         with self._condition:
# #             self._condition.notify_all()
# #
# #         # self._factory.call_all_instances(lambda f: f.set())
# #         # for flipflop in self._map.values():
# #         #     flipflop.set()

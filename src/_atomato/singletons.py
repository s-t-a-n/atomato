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
#
#
#
#
#
# # from weakref import WeakValueDictionary
# # https://stackoverflow.com/a/43620075
#
#
# # https://stackoverflow.com/a/6798042
# class Singleton(type):
#     """Singleton that allows continual reconstruction of a single instance unique to the process"""
#
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super().__call__(*args, **kwargs)
#         return cls._instances[cls]
#
#
# class FinalSingleton(type):
#     """Singleton that allows a single construction of a single instance unique to the process"""
#
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super().__call__(*args, **kwargs)
#             return cls._instances[cls]
#         else:
#             raise RuntimeError(
#                 "FinalSingleton does not allow multiple construction attempts."
#             )
#
# class ThreadedSingleton(type):
#     """Singleton that allows continual reconstruction of a single instance unique to the thread.
#
#         Attention:
#             This implementation relies on Python's dictionary operations being atomic. Locking is drastically
#             reduced by locking only on a missing instance (i.e. the first time).
#             For cross interpreter guaranteed thread safety, pass in a lock.
#     """
#     _singleton_lock: RLock = RLock()
#     _instances: Dict[int, Dict[Type, Any]] = {}
#
#     def __call__(cls, unsafe_dict: bool = False, *args, **kwargs):
#         thread_id = current_thread()
#
#         if unsafe_dict:
#             cls._singleton_lock.acquire()
#
#         if thread_id not in cls._instances:
#             cls._instances[thread_id] = {}
#
#         if cls not in cls._instances[thread_id]:
#             cls._instances[thread_id][cls] = super().__call__(*args, **kwargs)
#             print(f"registering instance {cls._instances[thread_id][cls]} for {cls} and thread {thread_id}")
#
#         if unsafe_dict:
#             with cls._singleton_lock:
#                 return cls._instances[thread_id][cls]
#
#         return cls._instances[thread_id][cls]
#
#     def call_all_instances(cls, f: Callable[[Type], None], unsafe_dict: bool = False):
#         if unsafe_dict:
#             cls._singleton_lock.acquire()
#
#         for t in cls._instances.keys():
#             if cls in cls._instances[t]:
#                 f(cls._instances[t][cls])
#
#
#         if unsafe_dict:
#             cls._singleton_lock.release()
#
# #
# # lock = RLock()
# #
# #
# # class MyThreadedSingleton(metaclass=ThreadedSingleton):
# #
# #     value: int
# #
# #     def __init__(self):
# #         self.value = 0
# #
# #     def set(self):
# #         print("set")
#
#
# # v_orig = MyThreadedSingleton()
# #
# #
# # def main():
# #     v = MyThreadedSingleton()
# #     assert v != v_orig
# #     v.value = 1
# #     v2 = MyThreadedSingleton()
# #     assert v == v2
# #     assert v.value == v2.value
# #
# #     return 0
# #
# # [t.start() for t in [Thread(target=main) for _ in range(10)]]
# #
# # MyThreadedSingleton.call_all_instances(lambda f: f.set())
# #
# # exit(0)

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
# from atomato import AtomicCounter
# from _atomato.atomic_flipflop import AtomicFlipFlop
# # read_back = AtomicCounter(0)
#
#
#
# def consumer(flipflop: AtomicFlipFlop, ctr: AtomicCounter, times_checked: AtomicCounter, s: Event, e: Event, f: Event):
#     while not f.is_set():
#         s.wait()
#         while True:
#             # sleep(0.01)
#             flipflop.wait()
#             times_checked.inc()
#             if ctr > 4:
#                 break
#         e.set()
#         # print(v.v)
#     # print("consumer finished")
#
#
#
# def producer(flipflop: AtomicFlipFlop, ctr: AtomicCounter, s: Event, e:Event, f: Event):
#     while not f.is_set():
#         while True:
#             n = ctr.inc()
#             flipflop.set()
#             if  n > 4:
#                 break
#
#
# from random import uniform
# from time import  sleep
#
# # print(f"it should take {iterations * timeout} seconds")
# print("start!")
# from time import time
#
#
# total_total_time  = 0
# def run_test(iterations: int, tcount: int):
#     start = Event()
#     end = Event()
#     final = Event()
#
#     ctr= AtomicCounter()
#     times_checked = AtomicCounter()
#     flipflop = AtomicFlipFlop()
#
#     thread_creation_start = time()
#     consumers = []
#     end_events = []
#     for i in range(tcount):
#         ev = Event()
#         consumers.append(Thread(target=consumer, args=[flipflop, ctr, times_checked, start, ev, final]))
#         end_events.append(ev)
#
#     producer_end_event = Event()
#     for t in consumers + [Thread(target=producer, args=[flipflop, ctr, start,producer_end_event, final])]:
#         t.start()
#
#     # sleep(0.01)
#     total_sleep_time = 0
#     total_time = 0
#     for it in range(iterations):
#
#         ctr.reset()
#         start_time = time()
#         start.set()
#         start.clear()
#
#         for e in end_events:
#             e.wait()
#             e.clear()
#         total_time += time() - start_time
#         producer_end_event.set()
#         producer_end_event.clear()
#     global total_total_time
#     total_total_time += total_time
#
#         # sleep(0.0001)
#     from _atomato.atomic_flipflop import get_locked
#     from _atomato.atomic_flipflop import set_locked
#
#     print(f"it took {total_time} for {iterations} iterations: {iterations/total_time} iterations/s (tcount:{tcount}, get_locked:{get_locked.value}, set_locked:{set_locked.value}, times_checked: {times_checked})")
#
#     final.set()
#     start.set()
#     end.set()
#
#     get_locked.reset()
#     set_locked.reset()
#     # sleep(0.01)
#     # assert all([not t.is_alive() for t in consumers])
#
# def run_test_repeated(iterations: int, tcount: int, repetition: int = 1):
#     for i in range(repetition):
#         run_test(iterations=iterations, tcount=tcount)
#     print(f"total time: {total_total_time}, averaging {total_total_time / repetition} s/test")
#
# # sleep(0.01)
# # run_test(iterations=10000, tcount=10)
# # run_test(iterations=10000, tcount=10)
# # run_test(iterations=10000, tcount=10)
# run_test_repeated(iterations=1000, tcount=10, repetition=10000)
#
#
#
# print("")

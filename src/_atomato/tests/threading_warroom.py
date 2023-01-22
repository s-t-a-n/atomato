# from threading import Event, RLock, Condition, Thread
# from queue import Queue
# from typing import *
# from time import time
# from time import sleep
# from random import uniform
#
# from _atomato.atomic_variable import AtomicObject
#
# from _atomato.atomic_counter import AtomicCounter
#
# g_ctr = AtomicCounter()
# g_avar = AtomicObject(variable=g_ctr)
#
# upper_limit = 100
#
#
# def producer(a: AtomicObject[AtomicCounter]):
#     for i in range(upper_limit):
#         # sleep(uniform(0, 0.001))
#
#         a.set_by(setter=lambda c: c.inc(1))
#
#
# def consumer(a: AtomicObject[AtomicCounter], consumer_finished: Event):
#     # print("wait")
#     # sleep(uniform(0, 0.001))
#
#     a.wait_for(lambda c: c >= upper_limit)
#     assert a >= upper_limit
#     # a.wait_above(value=5)
#     consumer_finished.set()
#     # print("above 5")
#
#
# def iteratively_test(tcount: int, iterations: int) -> bool:
#     total_time = 0
#     for i in range(iterations):
#         consumer_finished_events = []
#         consumers_threads = []
#         for _ in range(tcount):
#             e = Event()
#             consumers_threads.append(Thread(target=consumer, args=[g_avar, e]))
#             consumer_finished_events.append(e)
#         producer_thread = Thread(target=producer, args=[g_avar])
#         iteration_time_start = time()
#
#         for t in consumers_threads + [producer_thread]:
#             t.start()
#
#         for e in consumer_finished_events:
#             if not e.wait(timeout=0.1):
#                 return False
#         iteration_time = time() - iteration_time_start
#         total_time += iteration_time
#     print(f"it took {total_time} for {tcount} threads, {iterations} iterations")
#     return True
#
#
# test_repetition = 10000
# for i in range(test_repetition):
#     if not iteratively_test(tcount=10, iterations=1000):
#         raise RuntimeError("test timed out")

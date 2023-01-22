# type: ignore
import pytest

from atomato import AtomicObject


def test_atomic_variables_basics():
    a = AtomicObject(int())
    assert a.value == 0
    assert a == 0

    a.set(1)
    assert a == 1
    assert 0 < a < 2
    a.wait_for(predicate=lambda x: x == 1)

    with a:
        a.set(value=2)
        assert a == 2

    assert AtomicObject(float(1.1)) == 1.1

    from atomato import AtomicCounter

    assert AtomicObject(AtomicCounter(1)).set_by(setter=lambda ac: ac.inc()) == 2

    class MyClass:
        pass

    with pytest.raises(TypeError) as excinfo:
        int(AtomicObject(MyClass()))
    assert (
        "int() argument must be a string, a bytes-like object or a real number, not 'MyClass'"
        in str(excinfo.value)
    )

    # test construction methods
    assert AtomicObject(int(1)) == AtomicObject(int, 1)

    assert str(AtomicObject(int())) == "0"
    assert repr(AtomicObject(int())) == "AtomicObject(0)"


def test_atomic_variables_concurrency():
    from threading import Event
    from threading import Thread
    from time import time

    upper_limit = 100

    def consumer(
        a: AtomicObject[int],
        consumer_start: Event,
        consumer_finished: Event,
    ):
        consumer_start.wait()
        a.wait_for(lambda c: c >= upper_limit)
        assert a >= upper_limit
        consumer_finished.set()

    def producer(a: AtomicObject[int]):
        for i in range(upper_limit):
            a.set(a.value + 1)

    a = AtomicObject(int())
    thread_count = 2
    consumer_start_event = Event()
    consumer_finished_events = []
    consumers_threads = []
    for _ in range(thread_count):
        consumer_stop_event = Event()
        consumers_threads.append(
            Thread(target=consumer, args=[a, consumer_start_event, consumer_stop_event])
        )
        consumer_finished_events.append(consumer_stop_event)
    producer_thread = Thread(target=producer, args=[a])

    for t in consumers_threads + [producer_thread]:
        t.start()

    iteration_time_start = time()
    consumer_start_event.set()

    for e in consumer_finished_events:
        if not e.wait(timeout=0.001):  # pragma: no cover
            raise TimeoutError("consumer did not return in time")

    iteration_time = time() - iteration_time_start
    assert iteration_time < 0.001

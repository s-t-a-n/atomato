# type: ignore
import pytest

from atomato import AtomicVariable


def test_atomic_variables_basics():
    a = AtomicVariable(int())
    assert a.value == 0
    assert a == 0

    a.set(1)
    assert a == 1
    assert 0 < a < 2
    a.wait_for(predicate=lambda x: x == 1)

    with a:
        a.set(value=2)
        assert a == 2

    assert AtomicVariable(float(1.1)) == 1.1

    class MyClass:
        pass

    with pytest.raises(TypeError) as excinfo:
        int(AtomicVariable(MyClass()))
    assert (
        "int() argument must be a string, a bytes-like object or a real number, not 'MyClass'"
        in str(excinfo.value)
    )

    assert str(AtomicVariable(int())) == "0"
    assert repr(AtomicVariable(int())) == "AtomicVariable(0)"


def test_atomic_variables_concurrency():
    from threading import Event
    from threading import Thread
    from time import time

    from atomato import AtomicCounter

    upper_limit = 100

    def consumer(
        a: AtomicVariable[AtomicCounter],
        consumer_start: Event,
        consumer_finished: Event,
    ):
        consumer_start.wait()
        a.wait_for(lambda c: c >= upper_limit)
        assert a >= upper_limit
        consumer_finished.set()

    def producer(a: AtomicVariable[AtomicCounter]):
        for i in range(upper_limit):
            a.set_by(setter=lambda c: c.inc(1))

    ctr = AtomicCounter()
    a = AtomicVariable(ctr)
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

    assert ctr == upper_limit

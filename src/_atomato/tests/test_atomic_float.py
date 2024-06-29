# # type: ignore
#
# from atomato import AtomicFloat
#
#
# def test_atomic_float_basics():
#     i = AtomicFloat(0.0)
#     assert i == 0.0
#     assert i.value == 0.0
#
#     i = AtomicFloat(1.2)
#     assert i == 1.2
#     assert i.value == 1.2
#
#     i = AtomicFloat(0)
#     i.inc()
#     assert i.value == 1.0
#
#     i = AtomicFloat(0)
#     assert i == 0
#     i.set(2.5)
#     assert i == 2.5
#
#     assert AtomicFloat(1.5) == AtomicFloat(1.5)
#     assert AtomicFloat(1.5) < AtomicFloat(2.5)
#     assert AtomicFloat(2.5) > AtomicFloat(1.5)
#
#     i = AtomicFloat(0.5)
#     assert str(i) == "0.5"
#     assert repr(i) == "AtomicFloat(0.5)"

import gc

from kare.curry import curry


def test_function(x, y, z):
    return x + y


fn = curry(test_function)
fn2 = fn(1)(2)
# print(locals())
# print(globals())
# for obj in gc.get_objects():
#     print(obj)

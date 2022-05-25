import pytest

from kare import __version__
from kare.curry import curry


def test_version():
    assert __version__ == "0.0.0"


class TestCurry:
    def test_returns_the_same_function_if_nullary_function_is_passed(self):
        def nullary_function():
            return 1

        fn = curry(nullary_function)
        assert fn is nullary_function

    def test_returns_the_same_function_if_unary_function_is_passed(self):
        def unary_function(x: int) -> int:
            return x + 1

        fn = curry(unary_function)
        assert fn is unary_function

    def test_binary_function_is_partially_applied_if_a_single_argument_is_passed(self):
        def binary_function(x: int, y: int) -> int:
            return x + y

        fn = curry(binary_function)

        assert fn(1)(2) == 3

    def test_bound_function_call_fails_if_more_than_one_argument_is_passed(self):
        def ternary_function(x: int, y: int, z: int) -> int:
            return x + y + z

        with pytest.raises(TypeError):
            assert curry(ternary_function)(1)(2, 3) == 6

    def test_passing_function_with_kw_arguments_raises_an_exception(self):
        def kw_function(*, x, y):
            return x

        def kwargs_function(x, y, **kwargs):
            return x

        with pytest.raises(TypeError):
            curry(kw_function)
        with pytest.raises(TypeError):
            curry(kwargs_function)

    def test_multiple_curried_functions_in_same_scope(self):
        def binary_function(x: int, y: int) -> int:
            return x + y

        def another_binary_function(x: int, y: int, z: int) -> int:
            return x + y + z

        fn1 = curry(binary_function)
        fn2 = curry(another_binary_function)

        assert fn1(1)(2) == 3
        assert fn1(2)(2) == 4
        assert fn2(2)(2)(3) == 7
        assert fn2(3)(7)(8) == 18

    def test_can_curry_function_using_decorator(self):
        @curry
        def binary_function(x: int, y: int) -> int:
            return x + y

        add_three = binary_function(3)
        assert add_three(1) == 4

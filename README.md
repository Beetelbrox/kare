# kare
Minimal implementation of [Function Currying](https://en.wikipedia.org/wiki/Currying) for python (ab)using function closures.

## Usage
You can curry any callable by applying the `curry` function to it:
```python
from kare import curry

def my_sum(x: int, y: int) -> int:
    return x + y

my_curried_sum = curry(my_sum)
```
The resulting curried function will take a single argument and return a new curried function with the first argument of the original function bound to the passed value:
```python
sum_two = my_curried_sum(2)
sum_three = my_curried_sum(3)
```
Once all the arguments in the original function has been provided it is evaluated using the arguments passed to the curried function:
```python
my_sum(2)(3)    # == my_sum(2, 3)
my_sum(5)(3)    # == my_sum(5, 3)
```
It supports functions with multiple positional arguments. To indicate that the function should be evaluated just call it with no args:
```python
def variadic_sum(*args: int) -> int:
    return sum(args)

fn = curry(variadic_sum)

ten = fn(4)(2)(1)(1)(1)(1)

ten()   # == 10
```
The definition of currying requires the curried function to receive arguments in the same order as the original function. To satisfy that requirement we've don't allow the use of keyword arguments of any kind:
```python
def kwargs_adder(*, x: int, y: int) -> int:
    return x + y

def variadic_kwargs_adder(*, x: int, y: int) -> int:
    return x + y

curry(kwargs_adder)             # THIS WILL RAISE AN EXCEPTION
curry(variadic_kwargs_adder)    # THIS WILL RAISE AN EXCEPTION
```

If you need to do partial applications on keywords use `functools.partial` as usual:
```python
from functools import partial

partial(kwargs_adder, x=1)
```
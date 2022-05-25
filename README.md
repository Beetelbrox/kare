# kare
Minimal implementation of [Function Currying](https://en.wikipedia.org/wiki/Currying) for python. 

## Usage
You can curry any callable by applying the `curry` function to it:
```python
from kare import curry

def my_sum(x: int, y: int, z: int) -> int:
    return x + y + z

curried_sum = curry(my_sum)
```

Curried functions take a single argument and return either a new function that takes a single argument or the result of applying all the arguments passed so far to the original function:
```python
sum_two = curried_sum(2)
sum_five = sum_two(3)
sum_five(1) # == 6, equivalent to my_sum(2, 3, 1)
```

If you chain multiple calls together for a more succint notation:
```python
sum_five = curried_sum(2)(3)
```

The `curry` function also works as a decorator:
```python
@curry
def my_curried_sum(x: int, y: int, z: int) -> int:
    return x + y + z

add_six = my_curried_sum(2)(4)
```

Currently we only support functions with positional and specified number of arguments. The following:
```python
@curry  # This wil raise an exception
def variadic_positional_function(*args):
    ...

@curry # This wil raise an exception
def variadic_positional_function(*, x: int, y: int):
    ...

@curry # This wil raise an exception
def variadic_positional_function(x: int, y: int, **kwargs):
    ...

```

If you need to do partial application on keyword arguments you can use `functools`' `partial` as usual.
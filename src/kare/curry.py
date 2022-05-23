from inspect import Parameter, signature
from typing import Callable, Tuple


def is_curried(fn: Callable) -> bool:
    return hasattr(fn, "__currying__")


def _is_variadic(fn: Callable) -> bool:
    return any(
        param.kind == Parameter.VAR_POSITIONAL
        for param in signature(fn).parameters.values()
    )


def _register_curry(curried: Callable, original: Callable) -> Callable:
    curried.__currying__ = original
    return curried


def _is_binding_complete(fn: Callable, bindings: Tuple) -> bool:
    return len(bindings) == len(signature(fn).parameters) - 1


def _curry_function(fn: Callable, bindings: Tuple = ()) -> Callable:
    if _is_variadic(fn):
        return _register_curry(
            lambda x=None: fn(*bindings)
            if x is None
            else _curry_function(fn, (*bindings, x)),
            fn,
        )
    if _is_binding_complete(fn, bindings):
        return _register_curry(lambda x: fn(*bindings, x), fn)
    return _register_curry(lambda x: _curry_function(fn, (*bindings, x)), fn)


def _has_keyword_args(fn: Callable) -> bool:
    return any(
        param.kind in (Parameter.VAR_KEYWORD, Parameter.KEYWORD_ONLY)
        for param in signature(fn).parameters.values()
    )


def _should_bypass_currying(fn: Callable) -> bool:
    if not _is_variadic(fn) and len(signature(fn).parameters) < 2:
        return True
    return is_curried(fn)


def curry(fn: Callable) -> Callable:
    if _should_bypass_currying(fn):
        return fn
    if _has_keyword_args(fn):
        raise TypeError("Currying functions with keyword-only args is not supported")
    return _curry_function(fn)


def uncurry(fn: Callable):
    if is_curried(fn):
        return fn.__currying__
    raise TypeError("Not a curried function")

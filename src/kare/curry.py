from inspect import Parameter, Signature, signature
from typing import Callable, Optional, Tuple


def _has_keyword_args(signature: Signature):
    return any(
        param.kind in (Parameter.VAR_KEYWORD, Parameter.KEYWORD_ONLY)
        for param in signature.parameters.values()
    )


def _is_variadic(signature: Signature) -> bool:
    return any(
        param.kind == Parameter.VAR_POSITIONAL
        for param in signature.parameters.values()
    )


def _register_curry(curried: Callable, original: Callable) -> Callable:
    curried.__currying__ = original
    return curried


def _curry_function(fn, bindings=()):
    sig = signature(fn)
    if _is_variadic(sig):
        return _register_curry(
            lambda x=None: fn(*bindings)
            if x is None
            else _curry_function(fn, (*bindings, x)),
            fn,
        )
    if len(bindings) == len(sig.parameters) - 1:
        return _register_curry(lambda x: fn(*bindings, x), fn)
    return _register_curry(lambda x: _curry_function(fn, (*bindings, x)), fn)


def curry(fn: Callable):
    sig = signature(fn)
    if len(sig.parameters) < 2:
        return fn
    if _has_keyword_args(sig):
        raise TypeError("Currying functions with keyword-only args is not supported")
    return _curry_function(fn)


def uncurry(fn: Callable):
    if hasattr(fn, "__currying__"):
        return fn.__currying__
    raise TypeError("Not a curried function")

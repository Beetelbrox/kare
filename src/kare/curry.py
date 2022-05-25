from inspect import Parameter, signature
from typing import Callable, Tuple

_INVALID_ARITIES = (
    Parameter.VAR_KEYWORD,
    Parameter.KEYWORD_ONLY,
    Parameter.VAR_POSITIONAL,
)


class CurriedFunction:

    __slots__ = ["_fn", "_bindings"]

    def __init__(self, fn: Callable, bindings: Tuple = ()):
        self._fn = fn
        self._bindings = bindings

    def __call__(self, x):
        sig = signature(self._fn)
        bindings = (*self._bindings, x)
        if len(bindings) == len(sig.parameters):
            return self._fn(*bindings)
        return CurriedFunction(self._fn, bindings)


def is_curried(fn: Callable) -> bool:
    return isinstance(fn, CurriedFunction)


def _has_invalid_arity(fn: Callable) -> bool:
    return any(
        param.kind in _INVALID_ARITIES for param in signature(fn).parameters.values()
    )


def _should_bypass_currying(fn: Callable) -> bool:
    return len(signature(fn).parameters) < 2 or is_curried(fn)


def curry(fn: Callable) -> Callable:
    if _should_bypass_currying(fn):
        return fn
    if _has_invalid_arity(fn):
        raise TypeError(
            "Currying functions with *args or keyword-only args is not supported"
        )
    return CurriedFunction(fn)

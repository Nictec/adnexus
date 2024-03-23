import inspect
from functools import wraps
from typing import Callable

from xdi.callables import InjectedCallable, InjectedAsyncCallable


def inject(fn: Callable):
    """
    Decorator for marking a callable as injectable
    :param fn: Callable to decorate
    :return: InjectedCallable[fn]
    """
    if inspect.iscoroutinefunction(fn):
        return InjectedAsyncCallable(fn)

    return InjectedCallable(fn)

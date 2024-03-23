import inspect
from functools import wraps
from typing import Callable

from xdi.callables import InjectedCallable, InjectedAsyncCallable
from xdi.exceptions import XDIError


def inject(fn: Callable):
    """
    Decorator for marking a callable as injectable
    :param fn: Callable to decorate
    :return: InjectedCallable[fn]
    """
    if inspect.iscoroutinefunction(fn):
        return InjectedAsyncCallable(fn)
    elif inspect.isfunction(fn):
        return InjectedCallable(fn)
    else:
        raise XDIError("Currently XDI only supports functions and coroutines as a injection root!")

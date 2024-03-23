import inspect
from typing import Callable, Type, Any

from xdi.callables import InjectedCallable, InjectedAsyncCallable, InjectedClass
from xdi.exceptions import XDIError


def inject(fn: Callable | Type[Any]):
    """
    Decorator for marking a callable as injectable
    :param fn: Callable to decorate
    :return: InjectedCallable[fn]
    """
    if inspect.iscoroutinefunction(fn):
        return InjectedAsyncCallable(fn)
    elif inspect.isfunction(fn):
        return InjectedCallable(fn)
    elif inspect.isclass(fn):
        return InjectedClass(fn)
    else:
        raise TypeError(f"{fn} is not a injectable object")

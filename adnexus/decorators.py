import inspect
from typing import Callable, Type, Any

from adnexus.wrappers import InjectedCallable, InjectedAsyncCallable, InjectedClass


def inject(wrapped: Callable | Type[Any]):
    """
    Decorator for marking a callable as injectable
    :param wrapped: Callable or Class to decorate
    :return: InjectedCallable[fn]
    """
    if inspect.iscoroutinefunction(wrapped):
        return InjectedAsyncCallable(wrapped)
    elif inspect.isfunction(wrapped):
        return InjectedCallable(wrapped)
    elif inspect.isclass(wrapped):
        return InjectedClass(wrapped)
    else:
        raise TypeError(f"{wrapped} cannot be used as a root injection object")

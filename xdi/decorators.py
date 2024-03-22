from functools import wraps
from typing import Callable

from xdi.callables import InjectedCallable


def inject(fn: Callable):
    """
    Decorator for marking a callable as injectable
    :param fn: Callable to decorate
    :return: InjectedCallable[fn]
    """
    return InjectedCallable(fn)

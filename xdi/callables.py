from typing import Any, Dict, Callable, ClassVar

from xdi.exceptions import InjectionError


class InjectedCallable:
    dependencies: Dict[str, Any]
    _orig_callable: Callable

    def __init__(self, orig_callable: Callable):
        """
        Class for handling injected callables. Returned by the inject decorator
        :param orig_callable: The original callable to be wrapped by this object
        """

        self.dependencies = {}
        self._orig_callable = orig_callable

    def __call__(self, *args, **kwargs):
        """
        Calls the original callable with wired dependencies
        :param args: Arguments to pass to the original callable
        :param kwargs: Keyword arguments to pass to the original callable
        :return: Return of the original callable
        """
        if len(self.dependencies) < 1:
            raise InjectionError("DI container is not wired yet!")
        processed_kwargs = {key: value.get_instance() for key, value in self.dependencies.items()}
        processed_kwargs.update(kwargs)

        return self._orig_callable(*args, **processed_kwargs)

    @property
    def wrapped(self):
        """
        Getter for inner callable
        :return: Original callable
        """
        return self._orig_callable

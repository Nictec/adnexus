from typing import Any, Dict, Callable, Type

from adnexus.exceptions import InjectionError


class InjectedClass:
    """
    Wrapper for classes injected by adnexus
    """

    dependencies: Dict[str, Any]
    orig_class: Type[Any]

    def __init__(self, orig_class: Type[Any]):
        self.dependencies = {}
        self.orig_class = orig_class

    def __call__(self, *constructor_args, **constructor_kwargs):
        if len(self.dependencies) < 1:
            raise InjectionError("DI container is not wired yet!")

        processed_kwargs = {key: value.get_instance() for key, value in self.dependencies.items()}
        processed_kwargs.update(constructor_kwargs)

        return self.orig_class(*constructor_args, **processed_kwargs)

    @property
    def wrapped(self) -> Type[Any]:
        return self.orig_class


class InjectedCallable:
    """
    Wrapper for callables injected by adnexus
    """
    dependencies: Dict[str, Any]
    _orig_callable: Callable

    def __init__(self, orig_callable: Callable):

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
            raise InjectionError(f"DI container is not wired yet or {self._orig_callable} has no dependencies!")
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


class InjectedAsyncCallable(InjectedCallable):
    async def __call__(self, *args, **kwargs):
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

        return await self._orig_callable(*args, **processed_kwargs)

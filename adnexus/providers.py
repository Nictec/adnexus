from abc import ABC, abstractmethod
from functools import partialmethod
from typing import Any, Type, Dict, Tuple


class BaseProvider(ABC):
    _instance: Any = None
    _args: Tuple[Any, ...]
    _kwargs: Dict[str, Any]

    def __init__(self, provided_class: Type, *args, **kwargs):
        """
        Base class of all providers
        :param provided_class: class that the provider provides
        :param args: constructor args of the provided class
        :param kwargs: constructor kwargs of the provided class
        """
        
        self._args = args
        self._kwargs = kwargs
        self._provided_class = provided_class

    @abstractmethod
    def get_instance(self) -> Any: # pragma: no cover
        """
        Get an instance of the provided class
        :return: instance of the provided class
        """
        pass

    @abstractmethod
    def wire(self): # parma: no cover
        """
        Wire the provided class and its dependencies
        :return:
        """
        pass # pragma: no cover

    @property
    def provided_class_name(self):
        """
        Getter for the provided class name
        :return: name of the provided class
        """
        return self._provided_class.__name__

    @property
    def provided_class(self):
        return self._provided_class

    def inject_provided_init(self, patched_init: partialmethod): # pragma: no cover
        self._provided_class.__init__ = patched_init


class FactoryProvider(BaseProvider):
    """
    Provides a new injectable every time it is injected
    """
    def get_instance(self) -> Any:
        assert self._instance is not None, "Container is not wired yet"

        return self._instance(*self._args, **self._kwargs)

    def wire(self):
        # TODO: resolve the dependencies of the provided class
        self._instance = self._provided_class


class SingletonProvider(BaseProvider):
    """
    Provides a singleton injectable
    """
    def get_instance(self) -> Any:
        return self._instance

    def wire(self):
        self._instance = self._provided_class(*self._args, **self._kwargs)

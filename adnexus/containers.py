import functools
import importlib
import inspect
from abc import ABC
from typing import List, Dict, get_origin, get_args, Any

from pydantic import BaseModel

from adnexus.wrappers import InjectedCallable, InjectedClass
from adnexus.exceptions import ImproperlyConfigured, WiringError
from adnexus.providers import BaseProvider
from adnexus.markers import Provide


class BaseContainer(ABC):
    config: BaseModel
    injectables: List[BaseProvider]

    config: BaseModel
    _provider_mapping: Dict[str, BaseProvider] = {}

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self):
        """
        Class all container types inherit from
        """
        if len(self.get_injectables()) < 1:
            raise ImproperlyConfigured("Container must have at least one injectable")

    def wire(self, modules: List[str]):
        """
        Parse the config and do implementation specific wiring stuff
        :param modules: Modules of injectable callables
        """
        pass

    def get_injectables(self):
        if hasattr(self, "injectables"):
            return self.injectables
        else:
            return []


class DeclarativeContainer(BaseContainer):
    @staticmethod
    def _get_root_callables(mod_paths: List[str]):
        root_callables = []
        for mod_path in mod_paths:
            module = importlib.import_module(mod_path)
            root_callables.extend(
                [dep[1] for dep in inspect.getmembers(module, predicate=lambda m: isinstance(m, InjectedCallable) or isinstance(m, InjectedClass))])

        return root_callables

    def _resolve(self, injectable_obj: Any):
        if isinstance(injectable_obj, BaseProvider):
            # resolving dependencies of a dependency
            params = inspect.signature(injectable_obj.provided_class.__init__).parameters.items()
        elif isinstance(injectable_obj, InjectedCallable):
            # resolving dependencies of a InjectedCallable or AsyncInjectedCallable
            params = inspect.signature(injectable_obj.wrapped).parameters.items()
        elif isinstance(injectable_obj, InjectedClass):
            # resolving dependencies of InjectedClass
            params = inspect.signature(injectable_obj.wrapped.__init__).parameters.items()

        dependencies = {}
        for param_name, param_type in params:
            if get_origin(param_type.annotation) == Provide:
                dependency_class_name = get_args(param_type.annotation)[0].__name__
                if dependency_class_name not in self._provider_mapping.keys():
                    raise WiringError(f'"{dependency_class_name}" is not registered in container "{self.__class__.__name__}"')

                # resolve dependencies of dependencies
                current_dep_params = {key: value.get_instance() for key, value in self._resolve(self._provider_mapping[dependency_class_name]).items()}
                partial_init = functools.partialmethod(self._provider_mapping[dependency_class_name].provided_class.__init__, **current_dep_params)
                self._provider_mapping[dependency_class_name].inject_provided_init(partial_init)

                dependencies[param_name] = self._provider_mapping[dependency_class_name]

        return dependencies

    def wire(self, modules: List[str]):
        """
        Wire all injectables of this container
        :param modules:
        :return: Modules of injectable callables
        """

        super().wire(modules)

        for provider in self.get_injectables():
            provider.wire()
            self._provider_mapping[provider.provided_class_name] = provider

        for root_callable in self._get_root_callables(modules):
            setattr(root_callable, "dependencies", self._resolve(root_callable))

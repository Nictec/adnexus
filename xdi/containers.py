import importlib
import inspect
from abc import ABC
from typing import List, Dict, get_origin, get_args, Type

from pydantic import BaseModel

from xdi.callables import InjectedCallable
from xdi.config.base import BaseConfigLoader
from xdi.config.helpers import merge
from xdi.exceptions import ImproperlyConfigured, WiringError
from xdi.providers import BaseProvider
from xdi.markers import Provide


class BaseContainer(ABC):
    config_loaders: List[BaseConfigLoader]
    config_model: Type[BaseModel]
    injectables: List[BaseProvider]

    _config: BaseModel
    _provider_mapping: Dict[str, BaseProvider] = {}

    def __init__(self):
        """
        Class all container types inherit from
        """
        if not hasattr(self, "config_loaders") or not hasattr(self, "config_model"):
            raise ImproperlyConfigured("Config must be set on DI Container")
        elif len(self.injectables) < 1:
            pass # raise ImproperlyConfigured("Container must have at least one injectable")

    def wire(self, modules: List[str]):
        """
        Parse the config and do implementation specific wiring stuff
        :param modules: Modules of injectable callables
        """
        # iterate over the configured loaders
        full_cfg = {}
        for loader in self.config_loaders:
            full_cfg = merge(full_cfg, loader.load())

        # validate and store the whole config
        self._config = self.config_model.model_validate(full_cfg)


class DeclarativeContainer(BaseContainer):
    @staticmethod
    def _get_root_callables(mod_paths: List[str]):
        root_callables = []
        for mod_path in mod_paths:
            module = importlib.import_module(mod_path)
            root_callables.extend(
                [dep[1] for dep in inspect.getmembers(module, predicate=lambda m: isinstance(m, InjectedCallable))])

        return root_callables

    def _get_dependencies(self, root_callable: InjectedCallable) -> Dict[str, BaseProvider]:
        params = inspect.signature(root_callable.wrapped).parameters.items()
        dependencies = {}
        for param_name, param_type in params:
            if get_origin(param_type.annotation) == Provide:
                dependency_class_name = get_args(param_type.annotation)[0].__name__
                if dependency_class_name not in self._provider_mapping.keys():
                    raise WiringError(f'"{dependency_class_name}" is not registered in container "{self.__class__.__name__}"')

                dependencies[param_name] = self._provider_mapping[dependency_class_name]

        return dependencies

    def wire(self, modules: List[str]):
        """
        Wire all injectables of this container
        :param modules:
        :return: Modules of injectable callables
        """

        super().wire(modules)

        for provider in self.injectables:
            provider.wire()
            self._provider_mapping[provider.provided_class_name] = provider

        for root_callable in self._get_root_callables(modules):
            setattr(root_callable, "dependencies", self._get_dependencies(root_callable))

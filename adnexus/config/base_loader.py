from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict


class BaseConfigLoader(ABC):
    """
    Base class for implementing ConfigLoaders like TOMLLoader
    """
    def __init__(self, *args, **kwargs): # pragma: no cover
        pass

    @abstractmethod
    def get_config(self) -> Dict[str, Any]: # pragma: no cover
        """
        Internal method for the framework to load config files.
        :return: Loaded config as dict
        """
        pass


class FileConfigLoader(BaseConfigLoader):
    """
    Base class for all loaders that load config from files.
    """
    def __init__(self, path: Path):
        with path.open("r") as f:
            self.data = self.parse(f.read())

    @abstractmethod
    def parse(self, raw_data: str) -> dict:
        """
        Parses the loaded config file, must be implemented in all loaders
        :param raw_data: raw data loaded form file (e.g. toml, json, yaml, ...)
        :return: parsed config as dict
        """
        pass
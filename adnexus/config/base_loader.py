from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict


class BaseConfigLoader(ABC):
    def __init__(self, *args, **kwargs): # pragma: no cover
        pass

    @abstractmethod
    def get_config(self) -> Dict[str, Any]: # pragma: no cover
        pass


class FileConfigLoader(BaseConfigLoader):
    def __init__(self, path: Path):
        with path.open("r") as f:
            self.data = self.parse(f.read())

    @abstractmethod
    def parse(self, raw_data: str) -> dict:
        pass
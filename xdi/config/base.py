from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type

from pydantic import BaseModel


class BaseConfigLoader(ABC):
    """
    Base class for configuration loaders
    """
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def load(self) -> dict:
        pass


class StaticConfigLoader(BaseConfigLoader, ABC):
    """
    Loads configuration from a static file
    """
    file_content: str

    def __init__(self, file_path: Path):
        with file_path.open("r") as f:
            self.file_content = f.read()
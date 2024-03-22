from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type

from pydantic import BaseModel


class BaseConfigLoader(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    def load(self):
        pass


class StaticConfigLoader(BaseConfigLoader, ABC):
    file_content: str

    def __init__(self, file_path: Path):
        with file_path.open("r") as f:
            self.file_content = f.read()
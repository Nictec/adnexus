import json
import tomllib

import yaml
from pydantic import BaseModel

from xdi.config.base import StaticConfigLoader


class JSONConfigLoader(StaticConfigLoader):
    def load(self) -> BaseModel:
        return json.loads(self.file_content)


class TOMLConfigLoader(StaticConfigLoader):
    def load(self) -> BaseModel:
        return tomllib.loads(self.file_content)


class YAMLConfigLoader(StaticConfigLoader):
    def load(self):
        return yaml.safe_load(self.file_content)



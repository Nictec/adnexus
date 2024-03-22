import json
import tomllib

import yaml

from xdi.config.base import StaticConfigLoader


class JSONConfigLoader(StaticConfigLoader):
    """
    Loads configuration from a json file
    """
    def load(self) -> dict:
        return json.loads(self.file_content)


class TOMLConfigLoader(StaticConfigLoader):
    """
    Loads configuration from a toml file
    """
    def load(self) -> dict:
        return tomllib.loads(self.file_content)


class YAMLConfigLoader(StaticConfigLoader):
    """
    Loads configuration from a yaml file
    """
    def load(self) -> dict:
        return yaml.safe_load(self.file_content)



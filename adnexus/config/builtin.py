import json
import tomllib  #
import yaml

from typing import Dict, Any

from .base_loader import FileConfigLoader


class JSONLoader(FileConfigLoader):
    """
    Builtin config loader for JSON config files.
    """
    def parse(self, raw_data: str) -> Dict[str, Any]:
        return json.loads(raw_data)

    def get_config(self) -> Dict[str, Any]:
        return self.data


class TOMLLoader(FileConfigLoader):
    """
    Builtin config loader for TOML config files.
    """
    def parse(self, raw_data: str) -> dict:
        return tomllib.loads(raw_data)

    def get_config(self) -> Dict[str, str]:
        return self.data


class YAMLLoader(FileConfigLoader):
    """
    Builtin config loader for YAML config files.
    """
    def parse(self, raw_data: str) -> dict:
        return yaml.safe_load(raw_data)

    def get_config(self) -> Dict[str, Any]:
        return self.data

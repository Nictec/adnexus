import json
import tomllib  #
import yaml

from typing import Dict, Any

from .base_loader import FileConfigLoader


class JSONLoader(FileConfigLoader):
    def parse(self, raw_data: str) -> Dict[str, Any]:
        return json.loads(raw_data)

    def get_config(self) -> Dict[str, Any]:
        return self.data


class TOMLLoader(FileConfigLoader):
    def parse(self, raw_data: str) -> dict:
        return tomllib.loads(raw_data)

    def get_config(self) -> Dict[str, str]:
        return self.data


class YAMLLoader(FileConfigLoader):
    def parse(self, raw_data: str) -> dict:
        return yaml.safe_load(raw_data)

    def get_config(self) -> Dict[str, Any]:
        return self.data

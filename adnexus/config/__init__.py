from typing import Type, List
from pydantic import BaseModel
from .base_loader import BaseConfigLoader

from .helpers import merge


def load_config(loaders: List[BaseConfigLoader], model: Type[BaseModel]) -> BaseModel:
    """
    Load config from multiple loaders in a model
    :param loaders: List of config loaders to use
    :param model: config model
    :return: Config
    """
    dict_config = {}
    for loader in loaders:
        dict_config = merge(dict_config, loader.get_config())

    return model.parse_obj(dict_config)

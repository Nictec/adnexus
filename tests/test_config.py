from pathlib import Path

import pytest
from pydantic import BaseModel

from xdi.config import merge, load_config
from xdi.config.builtin import JSONLoader, TOMLLoader, YAMLLoader


class ExampleConfig(BaseModel):
    value: int


@pytest.fixture
def example_config_files():
    tmp_path = Path("/tmp")

    files_data = {
        "example_config.json": '{"value": 42}',
        "example_config.toml": 'value = 42',
        "example_config.yaml": "value: 42",
    }
    for file_name, content in files_data.items():
        file_path = tmp_path / file_name
        with file_path.open("w") as f:
            f.write(content)
    return files_data


def test_dict_merge():
    d1 = {"a": "a"}
    d2 = {"b": "b"}
    expected = {"a": "a", "b": "b"}

    assert merge(d1, d2) == expected

@pytest.mark.parametrize("loader_cls,filename", [(JSONLoader, "example_config.json"), (TOMLLoader, "example_config.toml"), (YAMLLoader, "example_config.yaml")])
def test_config_loaders(example_config_files, loader_cls, filename):
    config = load_config([loader_cls(Path("/tmp").joinpath(filename))], ExampleConfig)
    assert config.value == 42

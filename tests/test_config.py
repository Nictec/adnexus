import pytest
from pathlib import Path
from pydantic import BaseModel
from xdi.config import JSONConfigLoader, TOMLConfigLoader, YAMLConfigLoader
from xdi.config.helpers import merge


# Define an ExampleModel for testing purposes
class ExampleModel(BaseModel):
    value: int


# Define fixture for temporary config files
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


# helpers
def test_dict_merge():
    d1 = {"a": "a"}
    d2 = {"b": "b"}
    expected = {"a": "a", "b": "b"}

    assert merge(d1, d2) == expected


# loaders
def test_json_config_loader(example_config_files):
    loader = JSONConfigLoader(Path("/tmp/example_config.json"))
    config = loader.load()
    assert config.get("value") == 42


def test_toml_config_loader(example_config_files):
    loader = TOMLConfigLoader(Path("/tmp/example_config.toml"))
    config = loader.load()
    assert config.get("value") == 42


def test_yaml_config_loader(example_config_files):
    loader = YAMLConfigLoader(Path("/tmp/example_config.yaml"))
    config = loader.load()
    assert config.get("value") == 42

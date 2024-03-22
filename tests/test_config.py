import pytest
from pathlib import Path
from pydantic import BaseModel
from xdi.config import JSONConfigLoader, TOMLConfigLoader, YAMLConfigLoader


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


def test_json_config_loader(example_config_files):
    loader = JSONConfigLoader(ExampleModel, Path("/tmp/example_config.json"))
    config = loader.load()
    assert config.value == 42


def test_toml_config_loader(example_config_files):
    loader = TOMLConfigLoader(ExampleModel, Path("/tmp/example_config.toml"))
    config = loader.load()
    assert config.value == 42


def test_yaml_config_loader(example_config_files):
    loader = YAMLConfigLoader(ExampleModel, Path("/tmp/example_config.yaml"))
    config = loader.load()
    assert config.value == 42

from pathlib import Path
from datetime import datetime

import pytest
from pydantic import BaseModel
from xdi.containers import DeclarativeContainer
from xdi.config.builtin import TOMLConfigLoader
from xdi.exceptions import ImproperlyConfigured
from xdi.providers import FactoryProvider
from xdi.markers import Provide
from xdi.decorators import inject


class UpstreamInjectable:
    def __init__(self):
        self.result = "upstream_result"

    def get_result(self):
        return self.result


class TestInjectable:
    def __init__(self, name: str, upstream: Provide[UpstreamInjectable]):
        self.upstream = upstream
        self.name = name

    def run(self):
        return f"result, {self.name}, {self.upstream.get_result()}"


@inject
def test(injected: Provide[TestInjectable]):
    return injected.run()


@inject
class TestClass:
    def __init__(self, injected: Provide[TestInjectable]):
        self.injected = injected

    def test(self):
        return self.injected.run()


# needed for type completeness
class MyConfig(BaseModel):
    example_config1: str
    example_config2: str


class MyContainer(DeclarativeContainer):
    # the loaded config can be accessed by calling MyContainer.config.<name>
    config_loaders = [
        TOMLConfigLoader(Path("tests/settings.toml"))]  # <-- This file must (obviously) exist for the example to work
    config_model = MyConfig

    injectables = [
        FactoryProvider(TestInjectable, "Bob"),
        FactoryProvider(UpstreamInjectable)
    ]


class NoConfigContainer(DeclarativeContainer):
    injectables = [
        FactoryProvider(TestInjectable, "Bob"),
        FactoryProvider(UpstreamInjectable)
    ]


class MissingInjectablesContainer(DeclarativeContainer):
    config_loaders = [
        TOMLConfigLoader(Path("tests/settings.toml"))]  # <-- This file must (obviously) exist for the example to work
    config_model = MyConfig


@pytest.fixture(scope="module")
def wired_container():
    container = MyContainer()
    container.wire([__name__])

    return container

@pytest.fixture(scope="module")
def unwired_container():
    return MyContainer()

@pytest.fixture(scope="module")
def container_without_config():
    return NoConfigContainer


@pytest.fixture(scope="module")
def container_without_injectables():
    return MissingInjectablesContainer

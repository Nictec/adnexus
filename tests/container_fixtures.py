from pathlib import Path

import pytest
from pydantic import BaseModel
from adnexus.containers import DeclarativeContainer
from adnexus.providers import FactoryProvider
from adnexus.markers import Provide
from adnexus.decorators import inject
from tests.invalid_injectables import Circular1, Circular2


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
    pass

class CircularContainer(DeclarativeContainer):
    injectables = [
        FactoryProvider(Circular1),
        FactoryProvider(Circular2)
    ]


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

@pytest.fixture(scope="module")
def circular_container():
    cont = CircularContainer()
    cont.wire(["invalid_injectables"])
    return cont

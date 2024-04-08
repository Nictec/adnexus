import pytest
from xdi.providers import FactoryProvider, SingletonProvider


class ExampleClass:
    def __init__(self, value):
        self.value = value


def test_factory_provider():
    provider = FactoryProvider(ExampleClass, value=42)
    assert provider.provided_class_name == 'ExampleClass'
    assert provider.provided_class == ExampleClass

    provider.wire()
    instance = provider.get_instance()
    assert isinstance(instance, ExampleClass)
    assert instance.value == 42


def test_singleton_provider():
    provider = SingletonProvider(ExampleClass, value=42)
    assert provider.provided_class_name == 'ExampleClass'

    provider.wire()
    instance1 = provider.get_instance()
    instance2 = provider.get_instance()

    assert instance1 is instance2
    assert instance1.value == 42
    assert instance2.value == 42

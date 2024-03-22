import pytest
from xdi.callables import InjectedCallable


def example_function(arg1, dependency_arg):
    return arg1 + dependency_arg


class ExampleDependency:
    def __init__(self, value):
        self.value = value

    def get_item(self):
        return self.value


def test_injected_callable():
    # Mock dependencies
    dependencies = {
        "dependency_arg": ExampleDependency(42)
    }
    injected_callable = InjectedCallable(example_function)
    injected_callable.dependencies = dependencies

    result = injected_callable(10)
    assert result == 52

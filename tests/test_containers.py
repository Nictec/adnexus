import pytest

from adnexus.warnings import ContainerInitializationWarning
from container_fixtures import wired_container, unwired_container, test, circular_container, container_without_injectables, TestClass
from invalid_injectables import non_inj_test, circular
from adnexus.containers import DeclarativeContainer
from adnexus.exceptions import ImproperlyConfigured, WiringError, InjectionError
from adnexus.wrappers import InjectedCallable

def test_wiring(wired_container):
    assert isinstance(wired_container, DeclarativeContainer)
    assert isinstance(test, InjectedCallable)

def test_missing_injectables(container_without_injectables):
    # with pytest.raises(ImproperlyConfigured):
    #     container_without_injectables()
    with pytest.warns(ContainerInitializationWarning):
        container_without_injectables()

def test_injected_function(wired_container):
    assert test() == "result, Bob, upstream_result"

def test_injected_class(wired_container):
    tc = TestClass()
    assert tc.test() == "result, Bob, upstream_result"


def test_non_injectable(unwired_container):
    with pytest.raises(WiringError):
        unwired_container.wire(["invalid_injectables"])
    with pytest.raises(InjectionError):
        non_inj_test()
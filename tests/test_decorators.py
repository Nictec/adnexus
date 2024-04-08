import pytest

from xdi.decorators import inject
from xdi.wrappers import InjectedCallable, InjectedAsyncCallable, InjectedClass


@inject
def test_fn():
    pass


@inject
async def async_test_fn():
    pass


@inject
class TestClass:
    pass


def test_inject():
    assert isinstance(test_fn, InjectedCallable)
    assert isinstance(async_test_fn, InjectedAsyncCallable)
    assert isinstance(TestClass, InjectedClass)

    with pytest.raises(TypeError):
        inject(1)

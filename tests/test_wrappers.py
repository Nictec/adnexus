import asyncio

import pytest
from unittest.mock import Mock, AsyncMock
from xdi.wrappers import InjectedCallable, InjectedAsyncCallable, InjectedClass
from xdi.exceptions import InjectionError


class TestClass:
    def __init__(self, *args, **kwargs):
        pass

    def get_result(self):
        return "result"


@pytest.mark.parametrize("mock_callable,type",
                         [(Mock(), "callable"), (AsyncMock(), "async_callable"), (TestClass, "class")])
def test_callable_init(mock_callable, type):
    if type == "callable":
        inj_callable = InjectedCallable(mock_callable)
        assert inj_callable._orig_callable == mock_callable
        assert inj_callable.dependencies == {}
    elif type == "async_callable":
        inj_async_callable = InjectedAsyncCallable(mock_callable)
        assert inj_async_callable._orig_callable == mock_callable
        assert inj_async_callable.dependencies == {}
    elif type == "class":
        inj_class = InjectedClass(mock_callable)
        assert inj_class.dependencies == {}


@pytest.mark.parametrize("mock_callable,type",
                         [(Mock(), "callable"), (AsyncMock(), "async_callable"), (TestClass, "class")])
@pytest.mark.asyncio
async def test_callable_call_without_dependencies(mock_callable, type):
    with pytest.raises(InjectionError):
        if type == "callable":
            inj_callable = InjectedCallable(mock_callable)
            inj_callable()
        elif type == "async_callable":
            inj_callable = InjectedAsyncCallable(mock_callable)
            await inj_callable()
        elif type == "class":
            inj_class = InjectedClass(mock_callable)
            inj_obj = inj_class()
            inj_obj.get_result()


@pytest.mark.parametrize("mock_callable,type", [(Mock(return_value='result'), "callable"),
                                                (AsyncMock(return_value='result'), "async_callable"),
                                                (TestClass, "class")])
@pytest.mark.asyncio
async def test_callable_call_with_dependencies(mock_callable, type):
    if type == "callable":
        inj_callable = InjectedCallable(mock_callable)
        inj_callable.dependencies = {'dep1': Mock(get_instance=Mock(return_value='dependency1'))}
        result = inj_callable()
    elif type == "async_callable":
        inj_callable = InjectedAsyncCallable(mock_callable)
        inj_callable.dependencies = {'dep1': Mock(get_instance=Mock(return_value='dependency1'))}
        result = await inj_callable()
    elif type == "class":
        inj_class = InjectedClass(mock_callable)
        inj_class.dependencies = {'dep1': Mock(get_instance=Mock(return_value='dependency1'))}
        inj_obj = inj_class()
        result = inj_obj.get_result()

    assert result == 'result'


@pytest.mark.parametrize("mock_callable,type", [(Mock(return_value='result'), "callable"), (AsyncMock(return_value='result'), "async_callable"), (TestClass, "class")])
@pytest.mark.asyncio
async def test_callable_call_with_additional_args_and_kwargs(mock_callable, type):
    if type == "callable":
        inj_callable = InjectedCallable(mock_callable)
        inj_callable.dependencies = {'dep1': Mock(get_instance=Mock(return_value='dependency1'))}
        result = inj_callable()
    elif type == "async_callable":
        inj_callable = InjectedAsyncCallable(mock_callable)
        inj_callable.dependencies = {'dep1': Mock(get_instance=Mock(return_value='dependency1'))}
        result = await inj_callable()
    elif type == "class":
        inj_callable = InjectedClass(mock_callable)
        inj_callable.dependencies = {'dep1': Mock(get_instance=Mock(return_value='dependency1'))}
        inj_obj = inj_callable()
        result = inj_obj.get_result()
    else:
        result = None

    assert result == 'result'


@pytest.mark.parametrize("mock_callable,type", [(Mock(return_value='result'), "callable"), (AsyncMock(return_value='result'), "async_callable"), (TestClass, "class")])
def test_callable_wrapped_property(mock_callable, type):
    if type == "callable":
        inj_callable = InjectedCallable(mock_callable)
    elif type == "async_callable":
        inj_callable = InjectedAsyncCallable(mock_callable)
    elif type == "class":
        inj_callable = InjectedClass(mock_callable)
    else:
        inj_callable = None

    assert inj_callable.wrapped == mock_callable

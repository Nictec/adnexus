import pytest
from unittest.mock import Mock
from xdi.callables import InjectedCallable
from xdi.exceptions import InjectionError


def test_init():
    mock_callable = Mock()
    inj_callable = InjectedCallable(mock_callable)
    assert inj_callable._orig_callable == mock_callable
    assert inj_callable.dependencies == {}


def test_call_without_dependencies():
    mock_callable = Mock()
    inj_callable = InjectedCallable(mock_callable)
    with pytest.raises(InjectionError):
        inj_callable()


def test_call_with_dependencies():
    mock_callable = Mock(return_value='result')
    inj_callable = InjectedCallable(mock_callable)
    inj_callable.dependencies = {'dep1': Mock(get_instance=Mock(return_value='dependency1'))}
    result = inj_callable()
    mock_callable.assert_called_once_with(dep1='dependency1')
    assert result == 'result'


def test_call_with_additional_args_and_kwargs():
    mock_callable = Mock(return_value='result')
    inj_callable = InjectedCallable(mock_callable)
    inj_callable.dependencies = {'dep1': Mock(get_instance=Mock(return_value='dependency1'))}
    result = inj_callable(1, arg2='arg2_value')
    mock_callable.assert_called_once_with(1, dep1='dependency1', arg2='arg2_value')
    assert result == 'result'


def test_wrapped_property():
    mock_callable = Mock()
    inj_callable = InjectedCallable(mock_callable)
    assert inj_callable.wrapped == mock_callable

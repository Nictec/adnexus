import pytest

from adnexus.exceptions import *


@pytest.mark.parametrize("exception", [AdnexusError, InjectionError, WiringError])
def test_generic_error(exception):
    with pytest.raises(exception) as exec_info:
        raise exception("test")

    assert str(exec_info.value) == "test"


def test_improperly_configured():
    with pytest.raises(ImproperlyConfigured) as exec_info:
        raise ImproperlyConfigured("test")

    expected = "Framework config error: test"
    assert str(exec_info.value) == expected

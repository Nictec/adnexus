from xdi.decorators import inject
from xdi.callables import InjectedCallable


@inject
def test():
    pass


def test_inject():
    assert isinstance(test, InjectedCallable)

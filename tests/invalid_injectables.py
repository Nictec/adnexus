from xdi.decorators import inject
from xdi.markers import Provide


class NonInjecteable:
    pass

@inject
def non_inj_test(ni: Provide[NonInjecteable]):
    pass
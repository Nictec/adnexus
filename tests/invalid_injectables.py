from adnexus.decorators import inject
from adnexus.markers import Provide


class NonInjecteable:
    pass

@inject
def non_inj_test(ni: Provide[NonInjecteable]):
    pass
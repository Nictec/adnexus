from adnexus.decorators import inject
from adnexus.markers import Provide


class NonInjecteable:
    pass

@inject
def non_inj_test(ni: Provide[NonInjecteable]):
    pass


class Circular1:
    def __init__(self, c: Provide["Circular2"]):
        pass

class Circular3:
    def __init__(self, c: Provide[Circular1]):
        pass

class Circular2:
    def __init__(self, c: Provide[Circular1]):
        pass

@inject
def circular(c: Provide[Circular2]):
    pass

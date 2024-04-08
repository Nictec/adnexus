from typing import get_args
from xdi.markers import *

def test_provide_marker():
    marker = Provide[str]()

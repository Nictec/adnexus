from typing import get_args
from adnexus.markers import *

def test_provide_marker():
    marker = Provide[str]()

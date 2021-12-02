import pytest
from .. import es1

def test_positive():
    arr = [1,7,2,8,4,6,9,4]
    res = es1.helloworld()
    assert res == "helloworld"
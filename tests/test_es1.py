import pytest
from .. import es1


def test_one():
    arr = [1, 7, 2, 8, 4, 6, 9, 4]
    res = es1.lds(arr)
    assert res == [8, 6, 4]


def test_two():
    arr = [4, 4, 3, 7, 5]
    res = es1.lds(arr)
    assert res == [7, 5]

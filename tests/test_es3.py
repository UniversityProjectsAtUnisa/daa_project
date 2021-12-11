import pytest
import statistics
from .. import es3
import random
from .conftest import generate_random_integer


def oracle(l):
    if len(l) == 0:
        return None
    sl = list(sorted(set(l)))
    return sl[len(sl)//2]


def create_tree(l):
    t = es3.MedianTreeMap()
    for el in l:
        t[el] = 0
    return t


def mess_up_tree(t, l):
    l = list(sorted(set(l)))
    for _ in range(50):
        ch = random.choice([0, 1])
        if ch == 0 or len(l) == 0:  # Add random integer
            i = generate_random_integer()
            while i in l:
                i = generate_random_integer()
            l.append(i)
            t[i] = 0
        else:  # Remove existing random element from both structures
            i = random.choice(l)
            l.remove(i)
            del t[i]
    return t, l


@pytest.fixture
def random_tree(random_list):
    t = create_tree(random_list)
    return t, random_list


@pytest.mark.parametrize('execution_number', range(50))
def tests_multiple_insert_random(execution_number, random_tree):
    t, l = random_tree
    expected = oracle(l)
    result = t.median()
    result = None if result is None else result.key()
    with open("logs/es3.log", "a") as f:
        f.write(
            f"INSERT_ONLY: {execution_number=} {l=} {result=} {expected=}\n")
    assert result == expected, f"{result=} {expected=}"


@pytest.mark.parametrize('execution_number', range(50))
def tests_multiple_operations_random(execution_number, random_tree):
    t, l = mess_up_tree(*random_tree)
    expected = oracle(l)
    result = t.median()
    result = None if result is None else result.key()
    with open("logs/es3.log", "a") as f:
        f.write(
            f"INSERTS_AND_DELETES: {execution_number=} {l=} {result=} {expected=}\n")
    assert result == expected, f"{result=} {expected=}"

# autopep8: off
@pytest.mark.parametrize("test_input,expected", [
    ([1, 7, 2, 5, 3, 6, 4               ], 4   ),
    ([1, 2, 3, 4, 5, 6, 7               ], 4   ),
    ([1, 7, 2, 8, 4, 6, 9, 4, 9         ], 6   ),
    ([-1, -7, -2, -8, -4, -6, -9, -4, -9], -6  ),
    ([-1, -7, -2, 8, 4, -6, -9, -4, 9   ], -2  ),
    ([1, 7, 2, -8, 4, 6, 9, 4, 9        ], 4   ),
    ([                                  ], None),
    ([0, 0, 0, 0, 0, 0, 0, 0            ], 0   ),
    ([-1                                ], -1  ),
])
def test_success(test_input, expected):
    t = create_tree(test_input)
    result = t.median()
    result = None if result is None else result.key()
    assert result == expected, f"{result=} {expected=}"

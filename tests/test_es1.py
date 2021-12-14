import pytest
from .. import es1
from itertools import combinations
from os import path


def is_valid(it, arr):
    """Verifies if an iterable of integers has descending values (in wide sense) 
    and is a valid subsequence of another list

    Args:
        it (iterable of int): The iterable of integers to verify
        arr (list of int): The list used of which "it" should be a subsequence

    Returns:
        bool: True if "it" is a descending subsequence (in wide sense) of integers from "arr" 
    """
    # Has descending values
    for i in range(len(it)-1):
        if it[i+1] > it[i]:
            return False

    # Is subsequence
    arr = iter(arr)
    return all(i in arr for i in it)


def oracle(arr):
    """Oracle that finds the greatest descending subsequence (in wide sense) in an array
    by means of bruteforce

    Args:
        arr (list of int): list of integers to extract the subsequence from

    Returns:
        list of int: greatest descending subsequence (in wide sense)
    """
    best = tuple()
    # Iterate over every possibile combination of elements
    for i in range(len(arr) + 1):
        for comb in combinations(arr, i):
            if is_valid(comb, arr) and sum(comb) > sum(best):
                best = comb
    return list(best)


@pytest.mark.parametrize('execution_number', range(500))
def test_random(execution_number, random_list, LOG_RESULTS, LOG_DIRECTORY):
    """Tests the gds function with a list of random integers.
    Compares the result to the oracle

    Args:
        execution_number (int): the current execution identifier
        random_list (list of int): list of random integers
        LOG_RESULTS (bool): whether to log results or not
        LOG_DIRECTORY (str): relative path to log 
    """
    expected = oracle(random_list)
    result = es1.gds(random_list)
    if LOG_RESULTS:
        with open(path.join(LOG_DIRECTORY, "es1.log"), "a") as f:
            f.write(f"{execution_number=} {result=} {expected=}\n")
    assert is_valid(
        result, random_list), f"{result=} {expected=} {random_list=}"
    assert sum(result) == sum(expected), f"{result=} {expected=}"


# autopep8: off
@pytest.mark.parametrize("test_input,expected", [ 
    ([ 1,  7,  2,  8,  4,  6,  9,  4     ], [ 8,  6,  4 ]), 
    ([ 4,  4,  3,  7,  5                 ], [ 7,  5     ]),
    ([ 1,  7,  2,  8,  4,  6,  9,  4,  9 ], [ 9,  9     ]),
    ([-1, -7, -2, -8, -4, -6, -9, -4, -9 ], [           ]),
    ([-1, -7, -2,  8,  4, -6, -9, -4,  9 ], [ 8,  4     ]),
    ([ 1,  7,  2, -8,  4,  6,  9,  4,  9 ], [ 9,  9     ]),
    ([                                   ], [           ]),
    ([ 0,  0,  0,  0,  0,  0,  0,  0     ], [           ]),
    ([-1                                 ], [           ]),
])
def test_edge_cases(test_input, expected):
    """Tests the gds funciton with a fixed list of integers.

    There can be multiple valid answers, therefore it does not expect an exact matching.
    Either way the result must 
    - be a valid descending subsequence (in wide sense) of the test_input
    - have a sum that matches the sum of the expected result

    Args:
        test_input (list of int): fixed list of integers
        expected (list of int): expected result 
    """
    result = es1.gds(test_input)
    assert is_valid(result, test_input), f"{result=} {expected=}"
    assert sum(result) == sum(expected), f"{result=} {expected=}"
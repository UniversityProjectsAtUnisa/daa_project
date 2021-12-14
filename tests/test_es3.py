import pytest
from .. import es3
import random
from .conftest import generate_random_integer
from os import path


def oracle(l):
    """Oracle that finds the median in a list of integers

    Args:
        l (list of int): The list of integers

    Returns:
        int: The median of the list
    """
    length = len(l)
    if length == 0:
        return None
    sl = sorted(l)
    return sl[length//2]


def create_tree(l):
    """Creates a tree with keys from the list in input and values set to 0.

    Args:
        l (list of int): Values to use as keys of the tree

    Returns:
        MedianTreeMap: The created tree
    """
    t = es3.MedianTreeMap()
    for el in l:
        t[el] = 0
    return t


def mess_up_tree(t, l):
    """Executes random insertions and deletion in a tree.
    The operations are mirrored on a list that represents the set of keys of the tree.

    Args:
        t (MedianTreeMap): The tree
        l (list of int): The list that represents the set of keys of the tree

    Returns:
        tuple of (MedianTreeMap, list of int):
            tuple of a reference to the tree given in input and 
            the list that represents the set of keys of the tree after the operations have been applied
    """
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
def random_list_no_duplicates(random_list):
    """Fixture that represents a list of random integers without duplicates

    Args:
        random_list (list of int): list of random integers

    Returns:
        list of int: the list without duplicates
    """
    return list(set(random_list))


@pytest.fixture
def random_tree_with_list(random_list_no_duplicates):
    """Fixture that represents a tuple of a tree and
    the associated list that represents the set of keys of the tree, generated randomly.

    Args:
        random_list_no_duplicates (list of int): a list of random integers without duplicates
        on which base the tre must be created

    Returns:
        tuple of (MedianTreeMap, list of int): 
            tuple of the created tree and the list associated to the key set of the tree
    """
    t = create_tree(random_list_no_duplicates)
    return t, random_list_no_duplicates


@pytest.mark.parametrize('execution_number', range(250))
def test_median_inserts_random(execution_number, random_tree_with_list, LOG_RESULTS, LOG_DIRECTORY):
    """Tests the median method on a tree with keys generated randomly

    Args:
        execution_number (int): the current execution identifier
        random_tree_with_list (tuple of (MedianTreeMap, list of int)): 
            A tuple of a median tree and its associated key set as a list
        LOG_RESULTS (bool): whether to log results or not
        LOG_DIRECTORY (str): relative path to log
    """
    t, l = random_tree_with_list
    expected = oracle(l)
    result = t.median()
    result = None if result is None else result.key()
    if LOG_RESULTS:
        with open(path.join(LOG_DIRECTORY, "es3.log"), "a") as f:
            f.write(
                f"INSERTS_ONLY: {execution_number=} {l=} {result=} {expected=}\n")
    assert result == expected, f"{result=} {expected=}"


@pytest.mark.parametrize('execution_number', range(250))
def tests_median_operations_random(execution_number, random_tree_with_list, LOG_RESULTS, LOG_DIRECTORY):
    """Tests the median method on a tree with keys generated randomly.
    Before testing, multiple random insertion and deletion 
    are executed both on the list and the tree.

    Args:
        execution_number (int): the current execution identifier
        random_tree_with_list (tuple of (MedianTreeMap, list of int)): 
            A tuple of a median tree and its associated key set as a list
        LOG_RESULTS (bool): whether to log results or not
        LOG_DIRECTORY (str): relative path to log
    """
    t, l = mess_up_tree(*random_tree_with_list)
    expected = oracle(l)
    result = t.median()
    result = None if result is None else result.key()
    if LOG_RESULTS:
        with open(path.join(LOG_DIRECTORY, "es3.log"), "a") as f:
            f.write(
                f"INSERTS_AND_DELETES: {execution_number=} {l=} {result=} {expected=}\n")
    assert result == expected, f"{result=} {expected=}"

# autopep8: off
@pytest.mark.parametrize("test_input,expected", [
    ([ 1,  2,  3,  4,  5,  6,  7         ],  4   ),
    ([ 1,  2,  3,  4,  5,  6             ],  4   ),
    ([ 1,  2,  4,  6,  7,  8,  9         ],  6   ),
    ([-9, -8, -7, -6, -4, -2, -1         ], -6   ),
    ([-9, -7, -6, -4, -2, -1,  4,  8,  9 ], -2   ),
    ([-8,  1,  2,  4,  6,  7,  9         ],  4   ),
    ([                                   ], None ),
    ([ 0                                 ],  0   ),
    ([-2                                 ], -2   ),
    ([ 3                                 ],  3   ),
])
def test_edge_cases(test_input, expected):
    """Tests the median method with a fixed list of integers.

    Args:
        test_input (list of int): fixed list of integers
        expected (int): expected result
    """
    t = create_tree(test_input)
    result = t.median()
    result = None if result is None else result.key()
    assert result == expected, f"{result=} {expected=}"

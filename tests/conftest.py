import pytest
import random


@pytest.fixture
def LOG_RESULTS():
    """Fixture that acts like an environment variable for tests.
    Establishes whether to log results or not

    Returns:
        bool: whether you want to log results
    """
    return False


@pytest.fixture
def LOG_DIRECTORY():
    """Fixture that acts like an environment variable for tests.
    Establishes in which directory you want to store logs.
    The directory must exist while running tests.

    Returns:
        str: relative path to the directory where you want to store logs 
    """
    return "logs"


def generate_random_integer(min=-50, max=50):
    """Utility function to generate a random integer

    Args:
        min (int, optional): The minimum value of the randomly generated integer. Defaults to -50.
        max (int, optional): The minimum value of the randomly generated integer. Defaults to 50.

    Returns:
        int: The randomly generated integer
    """
    return random.randint(min, max)


@pytest.fixture
def random_list():
    """Fixture that represents a list of random integers

    Returns:
        list of int: List of random integers
    """
    N_ELEMENTS = 12
    l = [0] * N_ELEMENTS
    for i in range(len(l)):
        l[i] = generate_random_integer()
    return l

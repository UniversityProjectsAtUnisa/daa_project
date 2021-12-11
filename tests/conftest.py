import pytest
import random
import os
from datetime import datetime
from pathlib import Path


def generate_random_integer():
    MIN = -50
    MAX = 50
    return random.randint(MIN, MAX)


@pytest.fixture
def random_list():
    N_ELEMENTS = 12
    l = [0] * N_ELEMENTS
    for i in range(len(l)):
        l[i] = generate_random_integer()
    return l


def get_list_of_files(dirname):
    listOfFile = os.listdir(dirname)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirname, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + get_list_of_files(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles


def pytest_sessionstart(session):
    DIRECTORY_RELATIVE_PATH = "logs"
    Path(DIRECTORY_RELATIVE_PATH).mkdir(parents=True, exist_ok=True)
    for path in get_list_of_files(DIRECTORY_RELATIVE_PATH):
        with open(path, "w") as f:  # Reset content
            f.write(f"{datetime.now()}\n")

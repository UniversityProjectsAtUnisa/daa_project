import pytest
import random
import os
from datetime import datetime
from pathlib import Path


def generate_random_integer():
    return random.randint(-50, 50)


@pytest.fixture
def random_list():
    l = [0] * 12
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
    directory = "logs"
    Path(directory).mkdir(parents=True, exist_ok=True)
    for path in get_list_of_files(directory):
        with open(path, "w") as f:  # Reset content
            f.write(f"{datetime.now()}\n")

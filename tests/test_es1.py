import pytest
import random
from ..src import es1


def bruteforce(arr):
    best = []
    best_value = 0
    for i in range(2**len(arr)):
        cur = []
        for j, taken in enumerate(f"{i:>0{len(arr)+2}b}"[2:]):
            if taken == "1":
                if len(cur) and arr[j] > cur[-1]:
                    break
                cur.append(arr[j])
        if sum(cur) > best_value:
            best = cur
            best_value = sum(cur)

    return best


@pytest.mark.parametrize('execution_number', range(50))
def tests_multiple_random(execution_number):
    r = [0] * 12
    for i in range(len(r)):
        r[i] = random.randint(-50, 50)

    expected = bruteforce(r)
    result = es1.lds(r)
    assert sum(result) == sum(expected), f"{result} {expected}"


# autopep8: off
@pytest.mark.parametrize("test_input,expected", [ 
    ([1, 7, 2, 8, 4, 6, 9, 4            ], [8, 6, 4]), 
    ([4, 4, 3, 7, 5                     ], [7, 5   ]),
    ([1, 7, 2, 8, 4, 6, 9, 4, 9         ], [9, 9   ]),
    ([-1, -7, -2, -8, -4, -6, -9, -4, -9], [       ]),
    ([-1, -7, -2, 8, 4, -6, -9, -4, 9   ], [8, 4   ]),
    ([1, 7, 2, -8, 4, 6, 9, 4, 9        ], [9, 9   ]),
    ([                                  ], [       ]),
    ([0, 0, 0, 0, 0, 0, 0, 0            ], [       ]),
    ([-1                                ], [       ]),
])
def test_success(test_input, expected):
    result = es1.lds(test_input)
    assert sum(result) == sum(expected), f"{result} {expected}"

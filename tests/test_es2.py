import pytest
import random
from ..daa_collections.graphs.graph import Graph
from .. import es2


def oracle(g: Graph):
    if len(g.vertices()) <= 1:
        return g.vertices()
    return set(es2.bruteforce_independent_set(g))


def create_graph(n_vertices):
    g = Graph()
    for _ in range(n_vertices):
        g.insert_vertex()

    vertices = list(g.vertices())
    for i, v in enumerate(vertices[:-1]):
        for o in vertices[i+1:]:
            if random.choice([0, 1]):
                g.insert_edge(v, o)
    return g


@pytest.fixture
def random_graph():
    N_VERTICES = 20
    return create_graph(N_VERTICES)


@pytest.mark.parametrize('execution_number', range(50))
def tests_multiple_random(execution_number, random_graph):
    expected = len(oracle(random_graph))
    result = es2.independent_set(random_graph)
    with open("logs/es2.log", "a") as f:
        f.write(
            f"{execution_number=} {len(result)=} {expected=}\n")
    assert len(result) >= 1


# autopep8: off
@pytest.mark.parametrize("test_input,expected", [
    (0, 0),
    (1, 1),
])
def test_success(test_input, expected):
    g = create_graph(test_input)
    result = es2.independent_set(g)
    assert len(result) == expected, f"{len(result)=} {expected=}"

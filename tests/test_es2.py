import pytest
import random
from ..daa_collections.graphs.graph import Graph
from .. import es2
import math


def oracle(g: Graph):
    return set(es2.bruteforce_independent_set(g))


def create_graph(n_vertices, prob=None):
    if prob is None:
        prob = random.random()
    g = Graph()
    for _ in range(n_vertices):
        g.insert_vertex()

    vertices = list(g.vertices())
    for i, v in enumerate(vertices[:-1]):
        for o in vertices[i+1:]:
            if random.choices([0, 1], [1-prob, prob])[0]:
                g.insert_edge(v, o)
    return g


@pytest.fixture
def random_graph():
    N_VERTICES = 20
    return create_graph(N_VERTICES)


@pytest.mark.parametrize('execution_number', range(50))
def tests_multiple_random(execution_number, random_graph: Graph):
    expected = len(oracle(random_graph))
    result = es2.independent_set(random_graph)
    e = random_graph.edge_count()
    n = random_graph.vertex_count()
    k = math.floor(math.log2(n))
    MIN = max(1, expected*k/n)
    MAX = min(k, expected)
    max_e = n*(n-1)//2
    with open("logs/es2.log", "a") as f:
        f.write(
            f"{execution_number=} {len(result)=} {expected=} {MIN=} {MAX=} {k=} {n=} {e=} {max_e=}\n")
    assert len(result) >= MIN
    assert len(result) <= MAX
    assert es2.is_valid(random_graph, result)


@pytest.mark.parametrize("test_input,expected", [
    (0, 0),
    (1, 1),
])
def test_independet_set_edge_cases(test_input, expected):
    g = create_graph(test_input)
    result = es2.independent_set(g)
    assert len(result) == expected, f"{len(result)=} {expected=}"
    assert es2.is_valid(g, result)


def test_independent_set_complete_graph():
    g = Graph()
    for _ in range(5):
        g.insert_vertex()
    vs = list(g.vertices())
    for i in range(len(vs)-1):
        for j in range(i+1, len(vs)):
            g.insert_edge(vs[i], vs[j])
    result = es2.independent_set(g)
    expected = 1
    assert len(result) == expected


def test_independent_set_complete_graph():
    g = Graph()
    for _ in range(5):
        g.insert_vertex()
    vs = list(g.vertices())
    for i in range(len(vs)-1):
        for j in range(i+1, len(vs)):
            g.insert_edge(vs[i], vs[j])
    result = es2.independent_set(g)
    expected = 1
    assert len(result) == expected


@pytest.mark.parametrize("test_input,expected", [
    (0, 0),
    (1, 1),
])
def test_is_valid_edge_cases(test_input, expected):
    g = Graph()
    for _ in range(test_input):
        g.insert_vertex()
    assert es2.is_valid(g, g.vertices())


def test_is_valid_independent_set():
    """Tests is_valid with an independent_set"""
    g = Graph()
    for _ in range(5):
        g.insert_vertex()
    assert es2.is_valid(g, g.vertices())


def test_is_valid_not_independent_set():
    """Tests is_valid with a set of vertices definitely not independent"""
    g = Graph()
    for _ in range(5):
        g.insert_vertex()
    vs = list(g.vertices())
    for i in range(5):
        g.insert_edge(vs[i], vs[(i+1) % 5])
    assert es2.is_valid(g, g.vertices()) == False


def test_is_valid_almost_independent_set():
    """Tests is_valid with a set of vertices almost independent"""
    g = Graph()
    for _ in range(5):
        g.insert_vertex()
    vs = list(g.vertices())
    g.insert_edge(vs[2], vs[3])
    assert es2.is_valid(g, g.vertices()) == False


def test_is_valid_independent_set_bigger_graph():
    """Tests is_valid with a set of vertices independent but smaller than the set of all vertices"""
    g = Graph()
    for _ in range(10):
        g.insert_vertex()
    vs = list(g.vertices())
    for i in range(5):
        g.insert_edge(vs[i], vs[i+1])
    assert es2.is_valid(g, vs[6:])

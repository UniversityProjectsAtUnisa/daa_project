import pytest
import random
from ..daa_collections.graphs.graph import Graph
from .. import es2
from itertools import combinations
from os import path


def is_valid(g: Graph, vertices):
    """Verifies if vertices is a valid independent set for a graph.

    Args:
        g (Graph): The graph
        vertices (set of Vertex): The vertices set to verify

    Returns:
        bool: whether vertices is a valid independent set for g
    """
    if not isinstance(vertices, set):
        return False
    vertices = list(vertices)
    for i, v in enumerate(vertices[:-1]):
        for o in vertices[i+1:]:
            if g.get_edge(v, o) is not None:
                return False
    return True


def oracle(g: Graph):
    """Oracle that finds the maximum independent set of a graph.

    Args:
        g (Graph): the graph

    Returns:
        set of Vertex: the maximum independent set for g
    """
    return set(es2.bruteforce_independent_set(g))


def create_graph(n_vertices, prob=None):
    """Creates a graph of n_vertices.
    
    The edge between to arbitrary vertices vi, vj exists with chance prob.

    Args:
        n_vertices (int): the amount of vertices to insert in the new graph
        prob (float, optional): the chance of a valid edge to exist in the graph. 
            Defaults to a random value in [0, 1].

    Returns:
        Graph: the new graph
    """
    if prob is None:
        prob = random.random()
    elif not (0 <= prob <= 1):
        raise ValueError("Prob must belong to the interval [0, 1]")
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
def big_random_graph():
    """Fixture that represents a graph with a fixed high amount of vertices
    and a random amount of edges.

    Returns:
        Graph: the new graph
    """
    N_VERTICES = 1000
    return create_graph(N_VERTICES)


@pytest.fixture
def small_random_graph():
    """Fixture that represents a graph with a fixed low amount of vertices
    and a random amount of edges.

    Returns:
        Graph: the new graph
    """
    N_VERTICES = 20
    return create_graph(N_VERTICES)


@pytest.mark.parametrize('execution_number', range(50))
def tests_independent_set_random_graph(execution_number, big_random_graph: Graph, LOG_RESULTS, LOG_DIRECTORY):
    """Tests the independent_set function with a big_random_graph.

    "independent_set" is an approximation algorithm, therefore it does not always find the best answer.
    Since the approximation ratio has been bounded it tests that
        - the independent set contains m Vertices with m in [1, k]
        - the independent set is a valid independent set for big_random_graph

    Args:
        execution_number (int): the current execution identifier
        big_random_graph (Graph): the random graph
        LOG_RESULTS (bool): whether to log results or not
        LOG_DIRECTORY (str): relative path to log
    """
    result = es2.independent_set(big_random_graph)
    n = big_random_graph.vertex_count()
    k = es2.group_size(n)
    if LOG_RESULTS:
        edges = big_random_graph.edge_count()
        max_e = n*(n-1)//2
        with open(path.join(LOG_DIRECTORY, "es2.log"), "a") as f:
            f.write(
                f"{execution_number=} {len(result)=} {k=} {n=} {edges=} {max_e=}\n")
    assert 1 <= len(result) <= k
    assert is_valid(big_random_graph, result)


@pytest.mark.parametrize("test_input,expected", [
    (0, 0),
    (1, 1),
])
def test_independent_set_edge_cases(test_input, expected):
    """Tests the independent_set function with a graph of chosen amount of vertices.

    Args:
        test_input (int): the amount of vertices in the graph
        expected (int): the amount of vertices expected in the independent set
    """
    g = create_graph(test_input)
    result = es2.independent_set(g)
    assert len(result) == expected, f"{len(result)=} {expected=}"
    assert is_valid(g, result)


def test_independent_set_complete_graph():
    """Tests the independent_set function with a complete graph with more than one vertex.
    
    Expects the resulting independent set to contain only 1 vertex.
    """
    g = Graph()
    for _ in range(5):
        g.insert_vertex()
    vs = list(g.vertices())
    for i in range(len(vs)-1):
        for j in range(i+1, len(vs)):
            g.insert_edge(vs[i], vs[j])
    result = es2.independent_set(g)
    assert len(result) == 1


@pytest.mark.parametrize('execution_number', range(50))
def test_bruteforce_independent_set(execution_number, small_random_graph: Graph):
    """Tests the bruteforce_independent_set function with a small_random_graph. 

    Args:
        execution_number ([type]): [description]
        small_random_graph (Graph): [description]
    """
    vertices = list(small_random_graph.vertices())
    result = es2.bruteforce_independent_set(small_random_graph, vertices)
    assert is_valid(small_random_graph, result)
    for i in range(len(vertices), 0, -1):
        for comb in combinations(vertices, i):
            if is_valid(small_random_graph, set(comb)):
                # Manually found maximum independent set
                assert len(comb) == len(result)
                # There is no need to keep searching
                return


@pytest.mark.parametrize("test_input", [0, 1])
def test_is_valid_edge_cases(test_input):
    """Tests the is_valid function with a graph of chosen amount of vertices.

    Args:
        test_input (int): the amount of vertices in the graph
    """
    g = Graph()
    for _ in range(test_input):
        g.insert_vertex()
    assert is_valid(g, set(g.vertices()))


def test_is_valid_empty_graph():
    """Tests the is_valid function with a graph with
        - More than one vertex
        - No edges

    Expects is_valid to return True when the entire vertices set is given.
    """
    g = Graph()
    for _ in range(5):
        g.insert_vertex()
    assert is_valid(g, set(g.vertices()))


def test_is_valid_list():
    """Tests the is_valid function with an independent set with wrong types (should be a set)
    """
    g = Graph()
    for _ in range(5):
        g.insert_vertex()
    # Wrong because it's a list
    assert is_valid(g, list(g.vertices())) == False
    # Wrong because it's a dict_keys
    assert is_valid(g, g.vertices()) == False


def test_is_valid_cycle_graph():
    """Tests the is_valid function with a vertices set of a cycle graph"""
    g = Graph()
    for _ in range(5):
        g.insert_vertex()
    vs = list(g.vertices())
    for i in range(5):
        g.insert_edge(vs[i], vs[(i+1) % 5])
    assert is_valid(g, g.vertices()) == False


def test_is_valid_almost_independent_set():
    """Tests the is_valid function with a vertices set of a graph with 
        - more than two vertices
        - one edge
    """
    g = Graph()
    for _ in range(5):
        g.insert_vertex()
    vs = list(g.vertices())
    g.insert_edge(vs[2], vs[3])
    assert is_valid(g, g.vertices()) == False


def test_is_valid_independent_set_bigger_graph():
    """Tests the is_valid function with an set of vertices that is 
        - a subset of the vertices set of a graph with at least one edge
        - a valid independent set for said graph
    """
    g = Graph()
    for _ in range(10):
        g.insert_vertex()
    vs = list(g.vertices())
    for i in range(5):
        g.insert_edge(vs[i], vs[i+1])
    assert is_valid(g, set(vs[6:]))

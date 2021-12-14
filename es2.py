from .daa_collections.graphs.graph import Graph
import math


def group_size(n):
    """Finds a suitable group size for a vertices set of size n

    Args:
        n (int): the size of a vertices set

    Returns:
        int: a suitable group size based on n
    """
    CONSTANT = 1
    return math.floor(CONSTANT*math.log2(n))


def _groups(l: list, k=None):
    """Generator of lists which are a suitable partitioning 
    for a list of vertices

    Args:
        l (list of Vertex): the list of vertices
        k (int, optional): the group size. Defaults to group_size(len(l)).

    Yields:
        list of Vertex: the groups of size k. 
            The last group has at most k vertices.
    """
    if k is None:
        k = group_size(len(l))
    for i in range(0, len(l), k):
        yield l[i:i+k]


def bruteforce_independent_set(g: Graph, vertices=None):
    """Finds the maximum (with most vertices) independent set of a graph.
    If a list of vertices is given, finds the maximum independent set 
    among those vertices in relation to g.

    This algorithm, given enough time and space, 
    is always able to find the best independent set

    Args:
        g (Graph): the graph
        vertices (set of Vertex or list of Vertex, optional): the vertices set to consider. 

            Defaults to g.vertices()

    Returns:
        set of Vertex: inpdendent set for g
    """
    if vertices == None:
        # Use the entire vertices set
        vertices = list(g.vertices())
    elif isinstance(vertices, set):
        # Prepare for indexed access
        vertices = list(vertices)
    elif not isinstance(vertices, list):
        # Also accepts list for convenience
        raise TypeError("Vertices must be of type set or list")

    if len(vertices) == 0:
        return set()

    indices_of_best = []
    cur = [0]
    last = cur[-1]
    while last < len(vertices):
        is_valid = True
        for j in cur:
            if g.get_edge(vertices[last], vertices[j]) is not None:
                is_valid = False
                break
        if is_valid:
            if len(cur) > len(indices_of_best):
                indices_of_best = cur[:]
        if not is_valid:
            cur.pop()

        last += 1
        while last == len(vertices) and len(cur):
            last = cur.pop()+1
        cur.append(last)
    return set(vertices[i] for i in indices_of_best)


def independent_set(g: Graph):
    """Finds the maximum (with most vertices) independent set of a graph.

    This is an approximation algorithm, 
    therefore it does not always find the optimal result.

    Args:
        g (Graph): the graph

    Returns:
        set of Vertex: inpdendent set for g
    """
    vertices = list(g.vertices())
    if len(vertices) <= 1:
        return set(vertices)

    k = group_size(len(vertices))
    best = set()
    for group in _groups(vertices, k):
        cur = bruteforce_independent_set(g, group)
        if len(cur) > len(best):
            best = cur

    return best

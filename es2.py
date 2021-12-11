from daa_collections.graphs.graph import Graph
import math


def complementary_graph(g: Graph):
    c = Graph()
    vertices = g.vertices()
    for v in vertices:
        c.insert_vertex(v)
    for i, v in enumerate(vertices[:-1]):
        for o in vertices[i+1:]:
            if g.get_edge(v, o) is None:
                c.insert_edge(v, o)
    return c


def groups(l: list, k):
    for i in range(0, len(l), k):
        yield l[i:i+k]


def bruteforce_clique(g: Graph, l: list):
    best = []
    vertices = l
    for i in range(2**len(vertices)):
        cur = []
        for j, taken in enumerate(f"{i:>0{len(vertices)+2}b}"[2:]):
            if taken == 1:
                cur.append(vertices[j])
        if len(cur) > len(best):
            best = cur
    return best


def clique(g: Graph):
    vertices = list(g.vertices())
    best = []
    k = max(math.floor(math.log2()), 1)
    for group in groups(vertices, k):
        cur = bruteforce_clique(g, group)
        if len(cur) > len(best):
            best = cur

    return set(best)


def independent_set(g):
    c = complementary_graph(g)
    return clique(g)


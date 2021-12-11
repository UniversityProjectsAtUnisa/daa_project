import random
from .daa_collections.graphs.graph import Graph
import math
from itertools import combinations


def is_valid(g: Graph, vertices):
    vertices = list(vertices)
    for i, v in enumerate(vertices[:-1]):
        for o in vertices[i+1:]:
            if g.get_edge(v, o) is not None:
                return False
    return True


def groups(l: list, k):
    for i in range(0, len(l), k):
        yield l[i:i+k]


def bruteforce_independent_set(g: Graph, l=None):
    vertices = list(g.vertices()) if l == None else l
    for i in range(len(vertices), 0, -1):
        for comb in combinations(vertices, i):
            if is_valid(g, comb):
                return comb
    return tuple()


def independent_set(g: Graph):
    if len(g.vertices()) <= 1:
        return g.vertices()
    vertices = list(g.vertices())
    k = math.floor(math.log2(len(vertices)))
    best = []
    for group in groups(vertices, k):
        cur = bruteforce_independent_set(g, group)
        if len(cur) > len(best):
            best = cur

    return set(best)


############################################################################
# random.seed(1)


# def create_graph(n_vertices):
#     g = Graph()
#     for _ in range(n_vertices):
#         g.insert_vertex()

#     vertices = list(g.vertices())
#     for i, v in enumerate(vertices[:-1]):
#         for o in vertices[i+1:]:
#             if random.choice([0, 1]):
#                 g.insert_edge(v, o)
#     return g


# g = create_graph(5)
# s = bruteforce_independent_set(g)
# s = independent_set(g)
# print(s)

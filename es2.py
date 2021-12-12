import io
import pstats
import cProfile
import random
from daa_collections.graphs.graph import Graph
import math
from itertools import combinations


class Validator():
    __slots__ = "_cache", "_k"

    def __init__(self, _k):
        self._k = _k
        self.init_cache()

    def init_cache(self):
        self._cache = [None] * 2**self._k

    def is_valid_recursive(self, g: Graph, vertices):
        if len(vertices) <= 1:
            return True
        if not isinstance(vertices, tuple):
            vertices = tuple(vertices)
        if vertices in self._cache:
            return self._cache[vertices]
        if not self.is_valid_recursive(g, vertices[:-1]):
            return False
        v = vertices[-1]
        for o in vertices[:-1]:
            if g.get_edge(v, o) is not None:
                self._cache[vertices] = False
                return False
        self._cache[vertices] = True
        return True

    def is_valid(self, g: Graph, indexed_vertices):
        if len(indexed_vertices) <= 1:
            return True
        index = 2**indexed_vertices[0][0]
        for j, (i, v) in enumerate(indexed_vertices[1:]):
            index += 2**i
            if self._cache[index] == True:
                continue
            if self._cache[index] == False:
                return False
            # elif self._cache[index] is None:
            for _, o in indexed_vertices[:j+1]:
                if g.get_edge(v, o) is not None:
                    self._cache[index] = False
                    return False
            self._cache[index] = True
        return True

    def write(self, lung):
        with open(f"logs/test.log", "a") as f:
            f.write(
                f"{Validator._validator=} {self._calculated=} {self._from_cache=} {lung=}\n")


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


def bruteforce_independent_set(g: Graph, l=None, validator=None):
    vertices = list(g.vertices()) if l == None else l
    if validator is None:
        validator = Validator(len(vertices))
    else:
        validator.init_cache()
    for i in range(len(vertices), 0, -1):
        for comb in combinations(enumerate(vertices), i):
            if validator.is_valid(g, comb):
        # for comb in combinations(vertices, i):
        #     if is_valid(g, comb):
                return comb
    return tuple()


# -----------------------------------------------------


def profile(fnc):
    """A decorator that uses cProfile to profile a function"""

    def inner(*args, **kwargs):

        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner
# -----------------------------------------------------


@profile  # Remove
def independent_set(g: Graph):
    if len(g.vertices()) <= 1:
        return g.vertices()

    vertices = list(g.vertices())
    k = math.floor(math.log2(len(vertices)))
    validator = Validator(k)
    best = []
    for group in groups(vertices, k):
        cur = bruteforce_independent_set(g, group, validator)
        if len(cur) > len(best):
            best = cur

    return set(best)


# ------------------------------------------------------------
random.seed(1)


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


def random_graph():
    N_VERTICES = 2000
    return create_graph(N_VERTICES, .5)


independent_set(random_graph())

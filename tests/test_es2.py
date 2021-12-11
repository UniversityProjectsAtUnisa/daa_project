from daa_collections.graphs.graph import Graph


def is_valid(g: Graph, vertices):
    vertices = list(vertices)
    for i, v in enumerate(vertices[:-1]):
        for o in vertices[i+1:]:
            if g.get_edge(v, o) is None:
                return False
    return True


def best_answer(g: Graph):
    """Bruteforce oracle

    Returns the size of the biggest valid independent set
    """
    best_value = 0
    vertices = list(g.vertices())
    for i in range(2**len(vertices)):
        cur = []
        for j, taken in enumerate(f"{i:>0{len(vertices)+2}b}"[2:]):
            if taken == 1:
                cur.append(vertices[j])
        if is_valid(g, cur) and len(cur) > best_value:
            best_value = len(cur)
    return best_value

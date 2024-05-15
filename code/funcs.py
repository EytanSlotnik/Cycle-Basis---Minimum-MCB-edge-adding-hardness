import random
from itertools import combinations

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def relevantize(c) -> nx.Graph:
    rc = frozenset(c)
    relevant = nx.Graph()
    relevant.add_node(rc)
    relevant.add_edges_from([(rc, v) for v in c])
    relevant.add_edges_from([(c[i], c[(i + 1) % len(c)]) for i in range(len(c))])

    return relevant


def layering(g: nx.Graph) -> nx.Graph:
    lg = nx.union(g.copy(), g.copy(), rename=('a', 'b'))
    connecting_edges = [(f'a{u}', f'b{v}') for u, v in g.edges] + [(f'b{u}', f'a{v}') for u, v in g.edges]
    lg.add_edges_from(connecting_edges)

    return lg


def reduction(g: nx.Graph):
    lg = layering(g)

    mcb = nx.minimum_cycle_basis(g)
    rs = [relevantize(c) for c in mcb]
    for r in rs:
        lr = nx.union(r.copy(), r.copy(), rename=('a', 'b'))
        lg = nx.compose(lg, lr)
    rs = [relevantize([f'a{u}', f'a{v}', f'b{u}', f'b{v}']) for u, v in g.edges]
    for r in rs:
        lg = nx.compose(lg, r)
    mcb4 = [c for c in nx.minimum_cycle_basis(lg) if len(c) > 3]
    for u, v in g.edges:
        lg.remove_node(frozenset([f'a{u}', f'a{v}', f'b{u}', f'b{v}']))
    rs = [relevantize(c) for c in mcb4]
    for r in rs:
        lg = nx.compose(lg, r)

    return lg


def triangle_free_graph(total_nodes, m=None):
    """Construct a triangle free graph."""
    if m is None:
        m = total_nodes * (total_nodes - 1) // 2
    nodes = range(total_nodes)
    g = nx.Graph()
    g.add_nodes_from(nodes)
    edge_candidates = list(combinations(nodes, 2))
    random.shuffle(edge_candidates)
    for (u, v) in edge_candidates:
        if not set(n for n in g.neighbors(u)) & set(n for n in g.neighbors(v)):
            g.add_edge(u, v)
        if len(g.edges) == m:
            break
    return g


def new_reduction(g: nx.Graph) -> nx.Graph:
    lg = nx.union(g.copy(), g.copy(), rename=('a', 'b'))
    edges_from_a_to_b = [(f'a{u}', f'b{v}') for u, v in g.edges]
    edges_from_b_to_a = [(f'b{u}', f'a{v}') for u, v in g.edges]

    lg.add_edges_from(edges_from_a_to_b)
    mcb = nx.minimum_cycle_basis(lg)
    rs = [relevantize(c) for c in mcb]
    for r in rs:
        lg = nx.compose(lg, r)

    lg.add_edges_from(edges_from_b_to_a)

    return lg

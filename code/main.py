from itertools import product, combinations

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy as sp

from funcs import relevantize, layering, reduction, triangle_free_graph, new_reduction

if __name__ == '__main__':
    g = nx.cycle_graph(7)
    lg = new_reduction(g)

    mcb = nx.minimum_cycle_basis(lg)
    mcb4 = [c for c in mcb if len(c) > 3]
    print(mcb4)
    new_g = nx.Graph()
    for c in mcb4:
        n1, n2 = (c[0], c[2]), (c[1], c[3])
        new_g.add_edge(n1, n2)

    print(new_g.edges)
    layout = nx.planar_layout(new_g)
    nx.draw(new_g, layout, with_labels=True)
    plt.show()

    edge_gadgets = [[f'a{u}', f'a{v}', f'b{u}', f'b{v}'] for u, v in g.edges]
    new_new_g = nx.Graph()
    for c in edge_gadgets:
        n1, n2 = (c[0], c[2]), (c[1], c[3])
        new_new_g.add_edge(n1, n2)

    print(new_new_g.edges)
    layout = nx.planar_layout(new_new_g)
    nx.draw(new_new_g, layout, with_labels=True)
    plt.show()

    new_lg = nx.Graph()
    for v in new_g.nodes:
        new_lg.add_node(v[0])
        new_lg.add_node(v[1])
    for u, v in new_g.edges:
        new_lg.add_edge(u[0], v[0])
        new_lg.add_edge(u[1], v[1])
        new_lg.add_edge(u[0], v[1])
        new_lg.add_edge(u[1], v[0])

    # check if new_lg is contained in lg
    print(new_lg.edges)
    print(lg.edges)
    print(all(e in lg.edges for e in new_lg.edges))

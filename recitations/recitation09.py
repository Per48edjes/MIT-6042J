#!/usr/bin/env python3


import itertools as it
import math

import matplotlib.pyplot as plt
import networkx as nx


def construct_graph(side_len: int) -> nx.Graph:
    vertices = set(
        filter(
            lambda t: t[0] in (0, side_len) or t[1] in (0, side_len),
            set(it.product(range(side_len + 1), repeat=2)),
        )
    )
    vertices |= {(-2, 0), (0, side_len + 2), (side_len + 2, side_len), (side_len, -2)}
    G = nx.Graph()
    G.add_nodes_from(list((v, {"pos": v}) for v in vertices))
    G.add_edges_from(
        list(
            (v1, v2, {"weight": math.dist(v2, v1)})
            for v2 in vertices
            for v1 in vertices
            if v2 != v1
        )
    )
    return G


def augment_graph(
    graph: nx.Graph, min_weight_edges: set[tuple[tuple[int]]]
) -> nx.MultiGraph:
    graph_aug = nx.MultiGraph(graph.copy())
    for pair in min_weight_edges:
        graph_aug.add_edge(
            pair[0],
            pair[1],
            attr_dict={
                "distance": nx.dijkstra_path_length(graph, pair[0], pair[1]),
                "trail": "augmented",
            },
        )
    return graph_aug


def three_two_tsp(graph: nx.Graph) -> list[tuple[tuple[int, int]]]:
    G = graph
    T = nx.minimum_spanning_tree(G)
    S = {v for v in nx.nodes(G) if T.degree(v) % 2 == 1}
    M = nx.algorithms.matching.min_weight_matching(nx.induced_subgraph(G, S))
    G_prime = augment_graph(T, M)
    return list(nx.algorithms.euler.eulerian_circuit(G_prime))


def main() -> None:
    # Construct desired graph
    side_len = 6
    G = construct_graph(side_len)

    # Run 3/2-approximation algorithm
    edge_traversal = three_two_tsp(G)
    route = list(u for u, v in edge_traversal)

    # Plot results
    fig, ax = plt.subplots()
    nx.draw(
        G,
        pos=nx.get_node_attributes(G, "pos"),
        node_size=100,
        with_labels=False,
        ax=ax,
    )
    nx.draw_networkx_edges(
        G,
        pos=nx.get_node_attributes(G, "pos"),
        edgelist=edge_traversal,
        edge_color="red",
        arrows=True,
        arrowstyle="-|>",
        width=2,
    )

    plt.axis("on")
    ax.set_xlim(min(v[0] for v in nx.nodes(G)) - 5, max(v[0] for v in nx.nodes(G)) + 5)
    ax.set_ylim(min(v[1] for v in nx.nodes(G)) - 5, max(v[1] for v in nx.nodes(G)) + 5)
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)

    print("The route of the traveller is:", route)
    plt.show()


if __name__ == "__main__":
    main()

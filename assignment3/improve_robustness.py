import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def improve_robustness_high_degree_edges(G, num_edges):
    G_copy = G.copy()
    degree_dict = dict(G_copy.degree())
    high_degree_nodes = sorted(degree_dict, key=degree_dict.get, reverse=True)[:300]
    while num_edges > 0 and len(high_degree_nodes) > 1:
        node1 = high_degree_nodes.pop(0)
        for node2 in high_degree_nodes:
            if not G_copy.has_edge(node1, node2):
                G_copy.add_edge(node1, node2)
                num_edges -= 1
                if num_edges <= 0:
                    break
    return G_copy

def improve_robustness_peripheral_edges(G, num_edges):
    G_copy = G.copy()
    degree_dict = dict(G_copy.degree())
    low_degree_nodes = [node for node in degree_dict if degree_dict[node] == min(degree_dict.values())]
    while num_edges > 0 and len(low_degree_nodes) > 1:
        node1, node2 = random.sample(low_degree_nodes, 2)
        if not G_copy.has_edge(node1, node2):
            G_copy.add_edge(node1, node2)
            num_edges -= 1
    return G_copy

def improve_robustness_betweenness_edges(G, num_edges):
    G_copy = G.copy()
    centrality_dict = nx.betweenness_centrality(G_copy)
    high_centrality_nodes = sorted(centrality_dict, key=centrality_dict.get, reverse=True)[:300]
    while num_edges > 0 and len(high_centrality_nodes) > 1:
        node1 = high_centrality_nodes.pop(0)
        for node2 in high_centrality_nodes:
            if not G_copy.has_edge(node1, node2):
                G_copy.add_edge(node1, node2)
                num_edges -= 1
                if num_edges <= 0:
                    break
    return G_copy


def main():
    G = nx.read_edgelist("assignment3/sampled_graph.edges")
    #G = nx.karate_club_graph()
    num_edges = 1000
    G_degree = improve_robustness_high_degree_edges(G, num_edges)
    G_peripheral = improve_robustness_peripheral_edges(G, num_edges)
    G_betweenness = improve_robustness_betweenness_edges(G, num_edges)
    nx.write_edgelist(G_degree, "assignment3/data/improved_graph_degree.edges")
    nx.write_edgelist(G_peripheral, "assignment3/data/improved_graph_peripheral.edges")
    nx.write_edgelist(G_betweenness, "assignment3/data/improved_graph_betweenness.edges")

if __name__ == "__main__":
    main()
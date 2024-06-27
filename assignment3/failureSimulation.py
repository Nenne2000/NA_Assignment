import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np

def dataplot(random, degree, betweenness, pagerank):

    x = [i for i in range(len(random))]
    
    plt.plot(x, random, color='blue', label='Random attack')
    plt.plot(x, degree, color='red', label='Degree attack')
    plt.plot(x, betweenness, color='green', label='Betweenness attack')
    plt.plot(x, pagerank, color='yellow', label='Pagerank attack')

    plt.xlabel('iteration')
    plt.ylabel('dimension')
    plt.legend()

    plt.savefig(f"assignment3/plot.jpg")

def size(G):
    return len(max(nx.connected_components(G), key=len))

def random_failures(G, n):
    nodes = list(G.nodes())
    for i in range(n):
        G.remove_node(random.choice(nodes))
    return size(G)

def degree_failures(G, n):
    for i in range(n):
        degree_dict = dict(G.degree())
        max_degree_node = max(degree_dict, key=degree_dict.get)
        G.remove_node(max_degree_node)
    return size(G)

def pagerank_failures(G, n):
    for i in range(n):
        pagerank_dict = nx.pagerank(G)
        max_pagerank_node = max(pagerank_dict, key=pagerank_dict.get)
        G.remove_node(max_pagerank_node)
    return size(G)

def betweenness_failures(G, node_count):
    for i in range(node_count):
        betweenness_dict = nx.betweenness_centrality(G)
        max_betweenness_node = max(betweenness_dict, key=betweenness_dict.get)
        G.remove_node(max_betweenness_node)
    return size(G)


def main():
    #G = nx.erdos_renyi_graph(500, 0.1)
    #G = nx.read_edgelist("assignment2/sampled_graph.edges")
    #G = nx.karate_club_graph()
    G = nx.barabasi_albert_graph(500, 3)
    node_to_remove_each_time = 1
    iteration = 50

    print("componente gigante:", len(max(nx.connected_components(G), key=len)))

    G_random = G.copy()
    random = [random_failures(G_random, node_to_remove_each_time) for i in range(iteration)]

    G_degree = G.copy()
    degree = [degree_failures(G_degree, node_to_remove_each_time) for i in range(iteration)]

    G_betweenness = G.copy()
    betweenness = [betweenness_failures(G_betweenness, node_to_remove_each_time) for i in range(iteration)]

    G_pagerank = G.copy()
    pagerank = [pagerank_failures(G_pagerank, node_to_remove_each_time) for i in range(iteration)]

    print("random", random)
    print("degree", degree)
    print("betweenness", betweenness)
    print("pagerank", pagerank)
    dataplot(random, degree, betweenness, pagerank)


if __name__ == "__main__":
    main()
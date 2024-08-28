import statistics
import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

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

def critical_threshold(G):
    nodes = []
    for _, degree in G.degree():
        nodes.append(degree)
    second_moment = stats.moment(nodes, moment=2)
    avg_degree = statistics.mean(nodes)
    critical_threshold = 1-(1/(second_moment /avg_degree-1))
    return critical_threshold

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
    G = nx.read_edgelist("assignment3/sampled_graph.edges")
    #G = nx.karate_club_graph()
    #G = nx.barabasi_albert_graph(2000, 3)
    node_to_remove_each_time = 1
    iteration = 20

    G_random = G.copy()
    random = [random_failures(G_random, node_to_remove_each_time) for i in range(iteration)]

    G_degree = G.copy()
    degree = [degree_failures(G_degree, node_to_remove_each_time) for i in range(iteration)]

    G_betweenness = G.copy()
    betweenness = [betweenness_failures(G_betweenness, node_to_remove_each_time) for i in range(iteration)]

    G_pagerank = G.copy()
    pagerank = [pagerank_failures(G_pagerank, node_to_remove_each_time) for i in range(iteration)]

    dataplot(random, degree, betweenness, pagerank)

    G_a = nx.read_edgelist("assignment3/data/improved_graph_degree.edges")
    G_b = nx.read_edgelist("assignment3/data/improved_graph_peripheral.edges")
    G_c = nx.read_edgelist("assignment3/data/improved_graph_betweenness.edges")

    print(critical_threshold(G))
    print(critical_threshold(G_a))
    print(critical_threshold(G_b))
    print(critical_threshold(G_c))



if __name__ == "__main__":
    main()
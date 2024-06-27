import networkx as nx
import matplotlib.pyplot as plt

def calculate_critical_threshold(G):
    #todo: implementare il calcolo del critical threshold
    return 1

def add_edges_to_improve_robustness(G, strategy="degree", top_n=3):
    G_robust = G.copy()
    
    if strategy == "degree":
        degree_dict = dict(G.degree())
        sorted_nodes = sorted(degree_dict, key=degree_dict.get, reverse=True)
    elif strategy == "betweenness":
        betweenness_dict = nx.betweenness_centrality(G)
        sorted_nodes = sorted(betweenness_dict, key=betweenness_dict.get, reverse=True)
    elif strategy == "pagerank":
        pagerank_dict = nx.pagerank(G)
        sorted_nodes = sorted(pagerank_dict, key=pagerank_dict.get, reverse=True)
    else:
        raise ValueError("Strategia non valida. Scegli tra 'degree', 'betweenness', 'pagerank'.")

    for i in range(top_n):
        neighbors = list(G_robust.neighbors(sorted_nodes[i]))
        for j in range(len(neighbors)):
            for k in range(j+1, len(neighbors)):
                if not G_robust.has_edge(neighbors[j], neighbors[k]):
                    G_robust.add_edge(neighbors[j], neighbors[k])

    return G_robust

def main():
    G = nx.karate_club_graph()
    G_robust = add_edges_to_improve_robustness(G, strategy="betweenness", top_n=3)
    
    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    nx.draw_networkx(G, node_size=20, with_labels=False)
    plt.title("Grafo Originale, critical threshold: " + str(calculate_critical_threshold(G)))
    plt.subplot(122)
    nx.draw_networkx(G_robust, node_size=20, with_labels=False)
    plt.title("Grafo Modificato, critical threshold: " + str(calculate_critical_threshold(G_robust)))
    plt.show()

if __name__ == "__main__":
    main()

import os
import subprocess
import matplotlib.pyplot as plt
import networkx as nx
import random as rand


def plot_network_states(iteration, G, pos, labels, colors, output_directory):
    plt.figure(figsize=(8, 6))
    node_colors = [colors[labels[node]] for node in G.nodes()]
    nx.draw_networkx(G, pos=pos, node_color=node_colors, with_labels=False)
    plt.title(f"Iteration {iteration}")
    filename = os.path.join(output_directory, f"network_{iteration}.png")
    plt.savefig(filename)
    plt.close()

def plot_state_histogram(iteration, labels, output_directory):
    states = ["NotInformed", "Gossipier", "Malicious"]
    counts = [list(labels.values()).count(state) for state in ['N', 'G', 'M']]
    colors = ['blue', 'green', 'red']

    plt.figure(figsize=(8, 6))
    plt.bar(states, counts, color=colors)
    plt.title(f"Node States - Iteration {iteration}")
    plt.xlabel("States")
    plt.ylabel("Nodes")
    plt.ylim(0, sum(counts) + 1)
    filename = os.path.join(output_directory, f"histogram_{iteration}.png")
    plt.savefig(filename)
    plt.close()

def create_animation(output_directory):
    cmd = [
        'ffmpeg',
        '-framerate', '1/2',
        '-i', os.path.join(output_directory, 'network_%d.png'),
        '-c:v', 'libx264',
        '-r', '30',
        '-pix_fmt', 'yuv420p',
        os.path.join(output_directory, 'spread_animation.mp4')
    ]
    subprocess.run(cmd, check=True)


def initialize_network(G):
    return {node: 'N' for node in G.nodes()}

def initialize_gossipiers_and_malicious_nodes(G, num_gossipier, num_malicious):
    node_list = list(G.nodes())
    initial_informed = rand.sample(node_list, k=num_gossipier)
    remaining_nodes = list(set(node_list) - set(initial_informed))
    malicious_nodes = rand.sample(remaining_nodes, k=num_malicious)
    return initial_informed, malicious_nodes

def spread_information(G, labels, threshold):
    new_labels = labels.copy()
    spreading = False

    for node in G.nodes():

        if labels[node] == 'N':
            neighbors = list(G.neighbors(node))
            informed_neighbors = sum(1 for n in neighbors if labels[n] in ['G', 'M'])
            if informed_neighbors / len(neighbors) >= threshold:
                # se la maggioranza dei vicini è malicius allora il nodo diventa malizioso
                if sum(1 for n in neighbors if labels[n] == 'M') >= len(neighbors) / 2:
                    new_labels[node] = 'M'
                else:
                    new_labels[node] = 'G'
                spreading = True
    
    return new_labels, spreading

# ------------------------------------ Parametri del modello ------------------------------------
threshold = 0.1 #soglia di trasmissione dell'informazione
num_gossipier = 600 #numero di nodi inizialmente informati
num_malicious = 500 #numero di nodi malicious
# -----------------------------------------------------------------------------------------------


def main():
    #G = nx.karate_club_graph()
    G = nx.read_edgelist("assignment2/sampled_graph.edges")

    output_directory = f"assignment2/results/threshold={threshold}_init_informed={num_gossipier}_malicious={num_malicious}"
    os.makedirs(output_directory, exist_ok=True)

    pos = nx.spring_layout(G, seed=42)

    labels = initialize_network(G)
    gossipiers, malicious_nodes = initialize_gossipiers_and_malicious_nodes(G, num_gossipier, num_malicious)

    for node in gossipiers:
        labels[node] = 'G'

    for node in malicious_nodes:
        labels[node] = 'M'

    colors = {'N': 'blue', 'G': 'green', 'M': 'red'}

    num_iterations = 0
    spreading = True

    while spreading:
        plot_network_states(num_iterations, G, pos, labels, colors, output_directory)
        plot_state_histogram(num_iterations, labels, output_directory)

        labels, spreading = spread_information(G, labels, threshold)
        num_iterations += 1

    create_animation(output_directory)

if __name__ == "__main__":
    main()

import networkx as nx
import matplotlib.pyplot as plt
import random


G = nx.karate_club_graph()

node_colors = ['blue'] * len(G.nodes)

pos = nx.spring_layout(G, seed=42) 

theta = 0.5

initial_infected = random.sample(list(G.nodes), 3)

for node in initial_infected:
    node_colors[node] = 'red'

def contagion_step(G, node_colors, theta):
    new_node_colors = node_colors[:]
    for node in G.nodes:
        if node_colors[node] == 'blue': 
            neighbors = list(G.neighbors(node))
            infected_neighbors = sum([1 for neighbor in neighbors if node_colors[neighbor] == 'red'])
            if infected_neighbors / len(neighbors) >= theta:
                new_node_colors[node] = 'red' 
    return new_node_colors

while True:
    new_node_colors = contagion_step(G, node_colors, theta)
    if new_node_colors == node_colors:
        break
    node_colors = new_node_colors

plt.figure(figsize=(10, 7))
nx.draw_networkx(G, pos, node_color=node_colors, with_labels=True, node_size=500, font_color='white')
plt.title("Social Contagion in Zachary Karate Club Graph")
plt.show()

from matplotlib import pyplot as plt
import networkx as nx

def snowball_sampling(G, num_nodes):
    sampled_nodes = set()
    frontier = {'2300'}
    while len(sampled_nodes) < num_nodes and frontier:
        new_node = frontier.pop()
        sampled_nodes.add(new_node)
        frontier.update(set(G.neighbors(new_node)) - sampled_nodes)
    
    sampled_graph = G.subgraph(sampled_nodes).copy()
    return sampled_graph

G = nx.read_edgelist("assignment2/soc-gplus.edges")
components = nx.connected_components(G)
giant_component = max(components, key=len)
G = G.subgraph(giant_component)
sampled_G = snowball_sampling(G, 6000) 

#save the sampled graph in a .edge file
nx.write_edgelist(sampled_G, "assignment2/sampled_graph.edges")

nx.draw_networkx(sampled_G, with_labels=False)
plt.show()
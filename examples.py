import networkx as nx
import matplotlib.pyplot as plt


vertices1 = list(range(5))
edges1 = [(0, 1), (1, 2), (2, 3), (3, 4), (3, 1)]
w = [0, 3, 2, -2, -4]
weights1 = {k: v for k, v in zip(edges1, w)}

G = nx.DiGraph()
G.add_nodes_from(vertices1)
G.add_edges_from(edges1)
pos = nx.shell_layout(G)
nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightgreen', 
    font_size=11, font_weight='bold', arrowsize=20,)
nx.draw_networkx_edge_labels(G, pos, edge_labels=weights1, font_color='red', 
    font_size=11, font_weight='bold',rotate=False)

text1 = """
the cycle `1 2 3` is not a negative cycle as its sum is still positive
"""
# Add the text box
props = dict(boxstyle='round', facecolor='wheat', alpha=0.4)
plt.text(0.5, 0.98, text1, transform=plt.gca().transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='center', bbox=props)
plt.show()

#--------------------------------------------------------------------------------
vertices2 = list(range(5))
edges2 = [(0, 1), (1, 2), (2, 3), (3, 4), (3, 1)]
w = [0, 3, 2, -2, -6]
weights2 = {k: v for k, v in zip(edges2, w)}

text2 = """ 
the cycle `1 2 3` is a negative cycle as its sum is still positive.
A negative cycle always has an edge that can be relaxed
"""
G = nx.DiGraph()
G.add_nodes_from(vertices2)
G.add_edges_from(edges2)
pos = nx.shell_layout(G)
nx.draw_networkx_edge_labels(G, pos, edge_labels=weights2, font_color='red', 
    font_size=11, font_weight='bold',rotate=False)
nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightgreen', 
    font_size=11, font_weight='bold', arrowsize=20,)
plt.text(0.5, 0.01, text2, transform=plt.gca().transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='center', bbox=props)
plt.show()
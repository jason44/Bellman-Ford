import random
import numpy as np
import torch
import networkx as nx
import matplotlib.pyplot as plt

# The Bellman-Ford algorithm finds the smallest path from one node to another in a weighted digraph

vertex_count = 10
vertices = list(range(vertex_count))

# random edges (not a good idea, just saving time)
g = torch.Generator().manual_seed(1627596)
g2 = torch.Generator().manual_seed(208174839)
v1 = torch.randint(0, vertex_count, (30,), generator=g).tolist()
v2 = torch.randint(0, vertex_count, (30,), generator=g).tolist()
edges = list(set(filter(lambda tup: tup[0] != tup[1], [(u, v) for u, v in zip(v1, v2)])))

# assign weights to edges
ws = torch.randint(-vertex_count, vertex_count, (len(edges),), generator=g2).tolist()
weights = {k : v for k, v in zip(edges, ws)}

source = 3
target = 5
previous_node = [-1 for _ in range(vertex_count)]
distance = [9999999999 for _ in range(vertex_count)]
distance[source] = 0

# Since all distances are initialized towards infty except for source, the first iteration relaxes the edges adjacent to source.
# Then the next iteration relaxes the edges of the neighborhood of source and so on until we've traversed all connected nodes. 
#
# When we relax some edge to v, say (u, v), we choose the smallest path that goes from x to v for any x adjacent to v,  
# Because of how we initalized distance, this edge will always be part of a path from source to v. 
#
# THEOREM 1: If there exist a noncyclic path between two vertices, then it has at most |V|-1 edges 
# THEOREM 2: If there exist a path between two vertices, and there is a cycle along the path, then 
#            the shorter of the two paths is the path NOT along the cycle.
#
# Hence, if we relax all edges |V|-1 times we are guranteed that a noncyclic path has been found for all nodes.
# If no edges are relaxed, then we've already found all shortest paths from source and we can break early (and there are no negative cycles).
def relax():
    for _ in range(9):
        edges_relaxed = 0
        for edge in edges:
            u = edge[0]
            v = edge[1]
            w = weights[edge]
            if distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                previous_node[v] = u
                edges_relaxed += 1
        if edges_relaxed == 0: break
    
# However, if the path updates eve after the |V|-1 iterations of the relax routine, 
# then a negative cycle exist in the graph, ie: a cycle whose edges sum to a negative value 
# the cycle cannot be a positive cycle, because positive cycles do not update the smallest path.
# If there exist a negative cycle in the path to the target, then there is no smallest path as you could just loop around the cycle indefinetly
# The routine find_negative_cycle() outputs the negative cycles from any path that starts from source.
def find_negative_cycle():
    visited = [False for _ in range(vertex_count)]
    for edge in edges:
        u = edge[0]
        v = edge[1]
        w = weights[edge]
        if distance[u] + w < distance[v]:    
            # There is a cycle in a path, however (u,v) is not necessarily in this cycle. 
            # Every vertex within and after the cycle has the property that distance[u]+w < distance[v] is always true
            previous_node[v] = u
            visited[v] = True
            # Search for a vertex in the path that is guranteed to be in the cycle
            while not visited[u]:
                visited[u] = True
                u = previous_node[u]
            # Form the cycle itself and print
            ncycle = [u]
            v = previous_node[u]
            while v != u:
                ncycle.append(v)
                v = previous_node[v]
            print("negative cycle in the graph:", ncycle)
            break

def visualize():
    G = nx.DiGraph()
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightgreen', 
        font_size=11, font_weight='bold', arrowsize=20,)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weights, font_color='red', 
        font_size=11, font_weight='bold',rotate=False)
    plt.show()

relax()
visualize()
find_negative_cycle()

# Print Smallest Path from Source to Target
# In this example, the negative cycle is not in the path from 3 to 5. 
# If it was, then our print algorithm above would likely be unable to print 
# unless the cycle contains only target and no other vertex in the path, 
# or if the cycle contains target and other vertices in the path, but the path is |V|-1 edges long
print(previous_node)
current = target
path = []
while True:
    path.append(current)
    current = previous_node[current]
    if current == source:
        path.append(current)
        break
for v in path[:-1]:
    print(v, '<-- ', end='')
print(path[-1])



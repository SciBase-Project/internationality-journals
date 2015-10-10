print "[INFO] Reading aminer_edge_list.csv"
# all edges
edge_list = []
# self cited edges
edge_list_1 = []
# non self cited edges
edge_list_2 = []

import csv
with open('../output/aminer_edge_list.csv', 'rb') as file:
    reader = csv.reader(file)
    try:
        for row in reader:
            src = row[0]
            dest = row[1]
            type = row[2]

            edge = (src, dest)
            edge_list.append(edge)

            if type == '1' : edge_list_1.append(edge)
            else : edge_list_2.append(edge)
    except :
        pass

print "[INFO] Done reading"



print "[INFO] Generating graph"

import networkx as nx
import matplotlib.pyplot as plt

# make a new graph
G = nx.Graph()

all_edges = []
all_edges.extend(edge_list_1)
all_edges.extend(edge_list_2)
G.add_edges_from(all_edges)

# positions for all nodes
pos = nx.spring_layout(G)

# draw set of nodes
nx.draw_networkx_nodes(G, pos, node_size=15, node_color='b')

# draw set of edges from self cited list
nx.draw_networkx_edges(G,pos, edgelist=edge_list_1, width=1, edge_color='r')

# draw set of edges from non self cited list
# nx.draw_networkx_edges(G,pos, edgelist=edge_list_2, width=1, edge_color='g')

plt.show() # display

print "[INFO] Done generating graph"

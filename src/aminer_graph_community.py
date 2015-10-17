print "[INFO] Reading aminer_cites.json"

# nodes belonging to each publication
nodes = {}

# self cited edges
edge_list_1 = []
# non self cited edges
edge_list_2 = []
# publication edges
edge_list_3 = []

import json
with open('../output/aminer_cites.json') as data_file:
    data = json.load(data_file)

for publication in data :
    papers = data[publication]
    for paper in papers :

        # add edge to publication
        src = paper
        edge_list_3.append((publication, src))

        # add node to respective publication
        if publication not in nodes :
            nodes[publication] = []
        nodes[publication].append(paper)

        cites = data[publication][paper]
        for cite in cites :
            src = paper
            dest = cite['index']

            # add node to respective publication
            cite_pub = cite['publication']
            if cite_pub not in nodes :
                nodes[cite_pub] = []
            nodes[cite_pub].append(dest)


            # add edges
            edge  = (src, dest)

            # self cited edge
            if cite['self'] == True : edge_list_1.append(edge)
            # non self cited edge
            else                    : edge_list_2.append(edge)

            # add edge to publication
            edge_list_3.append((cite_pub, dest))

# remove all duplicates
edge_list_3 = list(set(edge_list_3))

# remove all duplicates
for pub in nodes :
    nodes[pub] = list(set(nodes[pub]))

print "[INFO] Done reading"



print "[INFO] Generating graph"

import networkx as nx
import matplotlib.pyplot as plt

# make a new graph
G = nx.Graph()

all_edges = []
all_edges.extend(edge_list_1)
all_edges.extend(edge_list_2)
all_edges.extend(edge_list_3)

G.add_edges_from(all_edges)

# positions for all nodes
pos = nx.spring_layout(G)

# draw set of nodes
for pub in nodes :
    from random import random
    nx.draw_networkx_nodes(G, pos, nodelist=nodes[pub], node_size=15, node_color=(random(), random(), random()))

# draw set of edges from self cited list
nx.draw_networkx_edges(G,pos, edgelist=edge_list_1, width=1, edge_color='r')

# draw set of edges from non self cited list
nx.draw_networkx_edges(G,pos, edgelist=edge_list_2, width=1, edge_color='g')

# draw set of edges to publications
# nx.draw_networkx_edges(G,pos, edgelist=edge_list_3, width=1, edge_color='k')

plt.show() # display

print "[INFO] Done generating graph"


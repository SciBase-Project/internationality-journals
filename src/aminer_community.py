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


cite_dict = {}
edge_dict = {}

import community
#first compute the best partitionf
partition=community.best_partition(G)
#drawing the graph based on number of links
size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0.
for com in set(partition.values()) :
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))


#nx.draw_networkx_edges(G,pos, alpha=0.5)
nx.draw(G,pos,node_size=15,alpha=1,node_color="blue", with_labels=False) # aplha = transparency, labels = names
#plt.savefig("aminer_smallest.png",dpi=1000)

#nx.draw_networkx_edges(G,pos, alpha=0.5)
plt.show()

print "[INFO] Done generating graph"
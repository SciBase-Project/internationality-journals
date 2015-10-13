import json
import networkx as nx

with open('../output/aminer_cites.json') as data_file:
    data = json.load(data_file)

for publication in data :
    G = nx.Graph()

    papers = data[publication]
    for paper in papers :
        cites = data[publication][paper]
        for cite in cites :
            src = paper
            dest = cite['index']
            G.add_edge(src, dest)

    A = nx.adjacency_matrix(G).todense()

    from numpy import linalg as LA
    w, v = LA.eig(A)

    print publication
    # eigen values
    print w
    # eigen vectors
    print v

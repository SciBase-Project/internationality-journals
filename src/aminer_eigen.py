import json
import networkx as nx

with open('../output/aminer_cites.json') as data_file:
    data = json.load(data_file)

G = nx.DiGraph()
for publication in data :

    papers = data[publication]
    for paper in papers :
        cites = data[publication][paper]
        for cite in cites :

            # source - main publication
            src = publication
            # destination - cited publication
            dest = cite['publication']

            if G.has_edge(src, dest) :
                G[src][dest]['weight'] += 1
            else :
                G.add_edge(src, dest, weight=1.0)

# for e in G.edges(data=True) :
#    print e


# adjacency matrix
adj = nx.to_numpy_matrix(G)

# import numpy
# for (x,y), value in numpy.ndenumerate(adj):
#     print x, y, value


from numpy import linalg as LA
w, v = LA.eig(adj)

# eigen values
print "eigen values : ", w
# eigen vectors
print "eigen vectors : ", v

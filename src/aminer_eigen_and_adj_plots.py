import json
import networkx as nx
from matplotlib import pyplot, patches
import numpy as np

def draw_adjacency_matrix(G, node_order=None, partitions=[], colors=[]):
    """
    - G is a netorkx graph
    - node_order (optional) is a list of nodes, where each node in G
          appears exactly once
    - partitions is a list of node lists, where each node in G appears
          in exactly one node list
    - colors is a list of strings indicating what color each
          partition should be
    If partitions is specified, the same number of colors needs to be
    specified.
    """
    adjacency_matrix = nx.to_numpy_matrix(G, dtype=np.bool, nodelist=node_order)

    #Plot adjacency matrix in toned-down black and white
    fig = pyplot.figure(figsize=(5, 5)) # in inches
    pyplot.imshow(adjacency_matrix,
                  cmap="Greys",
                  interpolation="none")
    pyplot.savefig("../output/aminer_adj_matrix.png")
    # The rest is just if you have sorted nodes by a partition and want to
    # highlight the module boundaries
    assert len(partitions) == len(colors)
    ax = pyplot.gca()
    for partition, color in zip(partitions, colors):
        current_idx = 0
        for module in partition:
            ax.add_patch(patches.Rectangle((current_idx, current_idx),
                                          len(module), # Width
                                          len(module), # Height
                                          facecolor="none",
                                          edgecolor=color,
                                          linewidth="1"))
            current_idx += len(module)



def draw_graph(G) :

    import math
    import matplotlib.pyplot as plt

    # make new graph
    G1 = nx.DiGraph()

    for edge in G.edges() :
        src, dest, weight = edge[0], edge[1], G[edge[0]][edge[1]]['weight']

        # self - loop
        if src == dest : continue

        # add edge to new graph
        G1.add_edge(src, dest, weight=math.log10(weight))

    edges,weights = zip(*nx.get_edge_attributes(G1,'weight').items())

    pos = nx.spring_layout(G1)
    nx.draw(G1, pos, node_color='b', node_size=50, edgelist=edges, edge_color=weights, width=1, edge_cmap=plt.cm.Blues, arrows=False)

    plt.show()




def calulate_eigen(G) :
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



def read_graph() :

    count = 0

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
                    count+=1
                else :
                    G.add_edge(src, dest, weight=1.0)

    for e in G.edges(data=True) :
        print e

    # print count

    return G



G = read_graph()

print "[INFO]  Calculating eigen values."
calulate_eigen(G)
print "[INFO]  Done calculating eigen values."


print "[INFO]  Drawing adjacency matrix.."
#draw_adjacency_matrix(G)
print "[INFO]  Done drawing adjacency matrix.."


print "[INFO]  Drawing graph.."
draw_graph(G)
print "[INFO]  Done drawing graph.."


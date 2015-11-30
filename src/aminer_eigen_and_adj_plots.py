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
                  interpolation="none"
                  )
    pyplot.savefig("../output/adj_low_to_high.png")

    print "[DEBUG]  Number of adj edges : ", len(G.edges())

    # pyplot.savefig("../output/aminer_adj_matrix.png")

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

    print "[INFO] Processing snip values of journals to be considered"
    snip = {}
    file = open("../data/journal_snip.txt")
    for line in file.readlines() :
        line = line.strip()
        vals = line.split(" : ")
        snip[vals[0]] = int(vals[1])
    file.close()
    print "[INFO] Done processing snip values"


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

    # node is journal
    for node in G.nodes() :
        nx.draw_networkx_nodes(G1, pos, nodelist=[node], node_size=(snip[node]/10), node_color='b')
    nx.draw_networkx_labels(G,pos, font_size=8)

    nx.draw_networkx_edges(G1, pos, edgelist=edges, edge_color=weights, width=1, edge_cmap=plt.cm.Blues, arrows=False)

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

    # median split statistics
    # get median split journal lists
    from aminer_median import get_median_split_journals
    journals_low , journals_high = get_median_split_journals()
    low_to_low_count = 0
    low_to_high_count = 0
    high_to_low_count = 0
    high_to_high_count = 0
    count = 0

    journal_self_edge_count = {}
    self_edge_count = 0


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


                if src == dest :
                    self_edge_count += 1

                    if src in journal_self_edge_count :
                        journal_self_edge_count[src] += 1
                    else :
                        journal_self_edge_count[src] = 1

                    # this should be commented while plotting adj plots
                    # continue


                # median split data
                type = 0
                if src in journals_low and dest in journals_low :
                    low_to_low_count += 1
                    type = 1
                if src in journals_low and dest in journals_high :
                    low_to_high_count += 1
                    type = 2
                if src in journals_high and dest in journals_low :
                    high_to_low_count += 1
                    type = 3
                if src in journals_high and dest in journals_high :
                    high_to_high_count += 1
                    type = 4

                # change types # type == 1
                if type == 2 :
                    if G.has_edge(src, dest) :
                        G[src][dest]['weight'] += 1
                    else :
                        G.add_edge(src, dest, weight=1.0)

                count+=1

    #for e in G.edges(data=True) :
    #    print e

    print ""
    print "[INFO] Printing self edges within each journal less than median"
    total = 0
    for j in journal_self_edge_count :
        if j in journals_low :
            print j, journal_self_edge_count[j]
            total += journal_self_edge_count[j]
    print "[DEBUG] Total self edges within journals less than median", total
    print "[INFO] Done printing self edges within each journal"
    print ""

    print ""
    print "[INFO] Printing self edges within each journal above than median"
    total = 0
    for j in journal_self_edge_count :
        if j in journals_high :
            print j, journal_self_edge_count[j]
            total += journal_self_edge_count[j]
    print "[DEBUG] Total self edges within journals above than median", total
    print "[INFO] Done printing self edges within each journal"
    print ""


    print "[DEBUG] Total edges : ", count + self_edge_count
    print "[DEBUG] Self edge count : ", self_edge_count
    print "[DEBUG] Edges without self edges : ", count
    print "[DEBUG] Low to low count : ", low_to_low_count
    print "[DEBUG] Low to high count : ", low_to_high_count
    print "[DEBUG] High to low count : ", high_to_low_count
    print "[DEBUG] High to high count : ", high_to_high_count

    return G



G = read_graph()

print "[INFO]  Calculating eigen values."
calulate_eigen(G)
print "[INFO]  Done calculating eigen values."


print "[INFO]  Drawing adjacency matrix.."
# comment out continue in read_graph
draw_adjacency_matrix(G)
print "[INFO]  Done drawing adjacency matrix.."


print "[INFO]  Drawing graph.."
#draw_graph(G)
print "[INFO]  Done drawing graph.."



import OnePlanarTester as opt
import networkx as nx

#INPUT: networkx graph G
#OUTPUT: bool which is True is G is maximally 1-planar
def maximalityTester(G):
    l = list(nx.non_edges(G))
    isMaximal = True
    for i in len(l):
        Gtemp = nx.Graph()
        Gtemp.add_edges_from(G.edges)
        Gtemp.add_edge(l[i])
        E = opt.generateE(Gtemp)
        x, y = opt.searchTree([],Gtemp,E, verbose = False)
        if(x == 0):
            isMaximal = False
    return isMaximal


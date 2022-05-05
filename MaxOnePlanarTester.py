import OnePlanarTester as opt
import networkx as nx
import multiprocessing as mp

#INPUT: networkx graph G
#OUTPUT: bool which is True is G is maximally 1-planar
def maximalityTester(G: nx.Graph):
    l = list(nx.non_edges(G))
    isMaximal = True
    gs = []
    for i in range(len(l)):
        Gtemp = nx.Graph()
        Gtemp.add_edges_from(G.edges)
        Gtemp.add_edge(l[i][0], l[i][1])
        gs.append(Gtemp)
    pool = mp.Pool()
    outputs = pool.map(checkMaximality, gs)
    return outputs

def checkMaximality(Graph):
    E = opt.generateE(Graph)
    x ,y = opt.searchTree([],Graph, E, verbose = False)
    onePlanar = False
    if (x == 0):
        onePlanar = True
    return onePlanar

def main():
    adjacency_dict = {
    0: (1, 2, 3, 4, 5, 6, 7),
    1: (0, 2, 3, 4, 5, 6),
    2: (0, 1, 3),
    3: (0, 1, 2, 4, 5, 7),
    4: (0, 1, 3, 5, 6, 7),
    5: (0, 1, 3, 4, 6, 7),
    6: (0, 1, 4, 5, 7),
    7: (0, 3, 4, 5, 6)}
    G = nx.Graph(adjacency_dict)
    print(G.edges)
    maximal = maximalityTester(G)
    print(maximal)

if __name__ == "__main__":
    main()

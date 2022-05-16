import OnePlanarTester as opt
import networkx as nx
import multiprocessing as mp

#INPUT: networkx graph G
#OUTPUT: list of bools indicating whether G remains 1-planar under a specific edge addition
#Uses a multiprocessing pool to parallelize the calculations, generating one thread per edge tested
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

#INPUT: networkx graph G
#OUTPUT: bool indicating whether G is 1-planar
def checkMaximality(Graph):
    E = opt.generateE(Graph)
    x ,y = opt.searchTree([],Graph, E, verbose = False)
    onePlanar = False
    if (x == 0):
        onePlanar = True
    return onePlanar

#Main function to generate graph and hand it over
def main():
    adjacency_dict = {
    0: (1, 2, 3, 4, 5, 7),
    1: (0, 2, 3, 4, 5, 7),
    2: (0, 1, 3),
    3: (0, 1, 2, 4, 5, 7),
    4: (0, 1, 3, 5, 6, 7),
    5: (0, 1, 3, 4, 6, 7),
    6: (4, 5, 7),
    7: (0, 1, 3, 4, 5, 6)}
    G = nx.Graph(adjacency_dict)
    print(G.edges)
    maximal = maximalityTester(G)
    print(maximal)

#Clownery required for parallel computing to work
if __name__ == "__main__":
    main()

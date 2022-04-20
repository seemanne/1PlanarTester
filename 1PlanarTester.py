import networkx as nx
import matplotlib.pyplot as plt
import random as rd
import numpy as np

#we generate the set E exactly once to save time by preprocessing, the set itself doesn't change throughout the code
def generateE(G):
    l1 = []
    l2 = []
    for e in nx.edges(G):
        l1.append(e)
    n = len(l1)
    #create the list of all crossing pairs, indexing j at 1 to kick out diagonals
    #atm this includes crossings from the same vertex which is unnecessary but otherwise its messy
    #no difference atm
    for i in range(n):
        for j in range(n-i-1):
            l2.append((l1[i], l1[j+1]))
    E = np.array(l2)
    return E



def searchTree(y, G, E):
    x = verifyNode(y, G, E)
    if (x==0): return 0,y
    if (x==1):
        rand = rd.random()
        if (rand > 0.5):
            r,r_y = searchTree(y.append(1), G, E)
            if (r == 0): return 0, r_y
            r,r_y = searchTree(y.append(0), G, E)
            if (r == 0): return 0, r_y
            return 2, None
        else:
            r,r_y = searchTree(y.append(0), G, E)
            if (r == 0): return 0, r_y
            r, r_y = searchTree(y.append(1), G, E)
            if (r == 0): return 0, r_y
            return 2, None
    if(x == 2):
        return 2, None

#todo: the following three functions can be merged together to save time and space

def checkLegalCrossings(y, E):
    S = {}
    n = len(y)
    for i in range(n):
        if (y[i] == 1):
            if (S.intersect({E[i][0], E[i][1]}) == {}):
                S.union({E[i][0], E[i][1]})
            else: return False
    return True

def findCrossedEdges(y, E):
    S = {}
    n = len(y)
    for i in range(n):
        if (y[i] == 1):
            S.union({E[i][0], E[i][1]})
    return S
    
def findKiteEdges(y, E, am):
    n = len(y)
    S = {}
    for i in range(n):
        if (y[i] == 1):
            v1, v2 = E[i][0][0], E[i][0][1]
            w1, w2 = E[i][1][0], E[i][1][1]
            if(am[v1][w1] == 1): S.add([v1, w1])
            if(am[v1][w2] == 1): S.add([v1, w2])
            if(am[v2][w1] == 1): S.add([v2, w1])
            if(am[v2][w2] == 1): S.add([v2, w2])
    return S

def computeInducedGraph():
    

def verifyNode(y, G, E):
    am = nx.to_numpy_array(G) #gives us the adjacency matrix as an np array
    if(not checkLegalCrossings(y, E)): return 2
    cross_edges = findCrossedEdges(y, E)
    kite_edges = findKiteEdges(y, E, am)
    if(cross_edges.intersection(kite_edges) != {}): return 2

    Gv = ComputeInducedGraph(y, G, E)
    Gstar = CreateCrossVertices(y, G, E)

    if(nx.check_planarity(Gstar)):
        if(Gv == G): return 0
        else:
            return 1
    else:
        return 2

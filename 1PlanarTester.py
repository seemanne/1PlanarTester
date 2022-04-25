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
            l2.append((l1[i], l1[i+j+1]))
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

#returns a set containing all edges that are crossed, without caring about the edges they are crossed with
def findCrossedEdges(y, E):
    S = {}
    n = len(y)
    for i in range(n):
        if (y[i] == 1):
            S.union({E[i][0], E[i][1]})
    return S
    
#returs a set containing all edges that are element of a kite in the drawing (even if the full kite doesn't exist)
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

def computeInducedGraph(y, G , E, am, cross_edges, kite_edges):
    edgeList = []
    #edges of type a)
    n = len(cross_edges)
    for i in range(n):
        edgeList.append(cross_edges[i])
    #edges of type b)
    index = len(y)
    #E[i] has shape [[a b][x y]]
    a = E[index][0][0]
    b = E[index][0][1]
    for i in range(a):
        #we use b-2 here because we want to add edges up to [a b-1] but need to care not to add edges like [0 0]
        for j in range(b-2):
            edgeList.append([a, b+1])
    #add [a, b] to the edge list if the next crossing in E starts with a different edge
    if (E[index+1][0] != np.array([(a, b)])):
        edgeList.append([a, b])
    #we do not implement c because its too expensive to check with too little gain (we need to check almost n^2 edges for every edge and its rarely true)
    #edges of type d)
    n = len(kite_edges)
    for i in range(n):
        edgeList.add(kite_edges[i])
    #build the graph Gv
    Gv = nx.Graph()
    Gv.add_edges_from(edgeList)
    return Gv

def createCrossVertices(y, G, E):
    #figure out the size of the graph so we know how to label our edges, keep in mind that the label of the last vertex is n-1 (index at zero but count at 1)
    n = len(G)
    m = len(y)
    j = 0
    #iteratively construct the planarization of G using the crossings for y and E
    for i in range(m):
        if (y[i] == 1):
            (v1, v2) = E[i][0]
            (w1, w2) = E[i][1]
            G.remove_edge(v1, v2)
            G.remove_edge(w1, w2)
            G.add_edge(v1, n+j)
            G.add_edge(v2, n+j)
            G.add_edge(w1, n+j)
            G.add_edge(w2, n+j)
            j += 1
    return G



    

def verifyNode(y, G, E):
    am = nx.to_numpy_array(G) #gives us the adjacency matrix as an np array
    if(not checkLegalCrossings(y, E)): return 2
    cross_edges = findCrossedEdges(y, E)
    kite_edges = findKiteEdges(y, E, am)
    if(cross_edges.intersection(kite_edges) != {}): return 2

    Gv = computeInducedGraph(y, G, E)
    Gstar = createCrossVertices(y, G, E)

    if(nx.check_planarity(Gstar)):
        if(Gv == G): return 0
        else:
            return 1
    else:
        return 2

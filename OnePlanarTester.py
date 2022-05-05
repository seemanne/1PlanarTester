import networkx as nx
import matplotlib.pyplot as plt
import random as rd
import numpy as np
import sys

rd.seed(0)

#INPUT: graph G
#OUTPUT: list of all edge*edge combinations which could represent a legal crossing for G
def generateE(G):
    #we generate the set E exactly once to save time by preprocessing, the set itself doesn't change throughout the code
    #E has the shape [[[a1, b1],[x1, y1]]...[[an, bm],[xj, yk]]], so E[i] is the ith crossing pair, E[i][0] the first edge of the ith crossing
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
            #nx.edges will always give us the edges in the format [a, b] where a \leq b, we abuse this in the following process
            if(l1[i][0]!=l1[i+j+1][0] and l1[i][1] != l1[i+j+1][0] and l1[i][1] != l1[i+j+1][1]):
                l2.append((l1[i], l1[i+j+1]))
    E = np.array(l2)
    return E


#INPUT: indicator y, graph G, edge*edge list E
#OUTPUT: 0, y' if the subtree rooted at y contains a solution for G with solution indicator y' and 2, None if it doesn't
def searchTree(y, G, E, verbose = True):
    #0 = SOL, 1 = CNT, 2 = CUT
    if(len(y) > len(E)):
        return 2, None
    x = verifyNode(y, G, E, verbose)
    if (x==0): return 0,y
    if (x==1):
        rand = rd.random()
        y1 = y.copy()
        y0 = y.copy()
        y1.append(1)
        y0.append(0)
        if (rand > 0.8):
            r,r_y = searchTree(y1, G, E, verbose)
            if (r == 0): return 0, r_y
            r,r_y = searchTree(y0, G, E, verbose)
            if (r == 0): return 0, r_y
            return 2, None
        else:
            r,r_y = searchTree(y0, G, E, verbose)
            if (r == 0): return 0, r_y
            r, r_y = searchTree(y1, G, E, verbose)
            if (r == 0): return 0, r_y
            return 2, None
    if(x == 2):
        return 2, None

#todo: the following three functions can be merged together to save time and space

#INPUT: indicator y, edge*edge list E
#OUTPUT: bool which is true if no edge is crossed twice for y
def checkLegalCrossings(y, E):
    S = set()
    n = len(y)
    for i in range(n):
        if (y[i] == 1):
            if (S.intersection({(E[i][0][0], E[i][0][1]), (E[i][1][0], E[i][1][1])}) == set()):
                S = S.union({(E[i][0][0], E[i][0][1]), (E[i][1][0], E[i][1][1])})
            else: return False
    return True

#INPUT: indicator y, edge*edge list E
#OUTPUT: set S containing all eges of G which are crossed for y
def findCrossedEdges(y, E):
    S = set()
    n = len(y)
    for i in range(n):
        if (y[i] == 1):
            S = S.union({(E[i][0][0], E[i][0][1]), (E[i][1][0], E[i][1][1])})
    return S
    
#INPUT: indicator y, edge*edge list E, adjacency matrix am
#OUTPUT: set S containing all edges of G which would be kite edges for crossings in y
def findKiteEdges(y, E, am):
    n = len(y)
    S = set()
    for i in range(n):
        if (y[i] == 1):
            v1, v2 = E[i][0][0], E[i][0][1]
            w1, w2 = E[i][1][0], E[i][1][1]
            if(am[v1][w1] == 1): S.add((v1, w1))
            if(am[v1][w2] == 1): S.add((v1, w2))
            if(am[v2][w1] == 1): S.add((v2, w1))
            if(am[v2][w2] == 1): S.add((v2, w2))
    return S


#INPUT: indicator y, graph G, edge*edge list E, set of crossing edges, set of kite edges
#OUTPUT: the graph Gv induced by the saturated edges
def computeInducedGraph(y, G , E, am, cross_edges, kite_edges):
    edgeList = []
    Gv = nx.Graph()
    Gv.add_edges_from(G.edges)
    #edges of type a)
    n = len(cross_edges)
    for i in range(n):
        edgeList.append(list(cross_edges)[i])
    #edges of type b)
    #complete rework of computeInducedGraph below, now removes edges instead of adding
    removeEdges = []
    depth = len(y)
    m = len(E)
    for k in range(m-depth):
        removeEdges.append((E[depth+k][0][0],E[depth+k][0][1]))
        removeEdges.append((E[depth+k][1][0],E[depth+k][1][1]))
    Gv.remove_edges_from(removeEdges)
    #E[i] has shape [[a b][x y]]

    #OLD WONKY CALCULATIONS

    #a = E[index][0][0]
    #b = E[index][0][1]
    #for i in range(a):
        #we use b-2 here because we want to add edges up to [a b-1] but need to care not to add edges like [0 0]
    #    for j in range(b-2):
    #        edgeList.append((i, j+1))
    #add [a, b] to the edge list if the next crossing in E starts with a different edge
    #to prevent an index out of bounds error on the last pass we add the check
    #if (index == len(E)-1):
    #    Gv.add_edges_from(G.edges)
        #The argument here is that on the last pass the induced graph has to be the full graph
    #else: 
    #    if(not np.array_equal(E[index+1][0], np.array((a, b)))): 
    #        edgeList.append((a, b))
    #we do not implement c because its too expensive to check with too little gain (we need to check almost n^2 edges for every edge and its rarely true)
    #edges of type d)
    
    n = len(kite_edges)
    for i in range(n):
        edgeList.append(list(kite_edges)[i])
    #build the graph Gv
    Gv.add_edges_from(edgeList)
    return Gv


#INPUT: indicator y, graph Gv, edge*edge list E
#OUTPUT: Graph Gtemp representing the planarisation of Gv for the crossings in y
def createCrossVertices(y, Gv, E):
    #figure out the size of the graph so we know how to label our edges, keep in mind that the label of the last vertex is n-1 (index at zero but count at 1)
    m = len(y)
    j = 0
    Gtemp = nx.Graph()
    Gtemp.add_edges_from(Gv.edges)
    n = len(Gtemp)
    #iteratively construct the planarization of G using the crossings for y and E
    for i in range(m):
        if (y[i] == 1):
            (v1, v2) = E[i][0]
            (w1, w2) = E[i][1]
            Gtemp.remove_edge(v1, v2)
            Gtemp.remove_edge(w1, w2)
            Gtemp.add_edge(v1, n+j)
            Gtemp.add_edge(v2, n+j)
            Gtemp.add_edge(w1, n+j)
            Gtemp.add_edge(w2, n+j)
            j += 1
    return Gtemp



    
#INPUT: indicator y, graph G, edge*edge list E
#OUTPUT: 0 if y is a solution, 1 if y is potentially part of a solution, 2 if cannot be part of a solution
def verifyNode(y, G, E, verbose):
    #0 = SOL, 1 = CNT, 2 = CUT
    am = nx.to_numpy_array(G) #gives us the adjacency matrix as an np array
    if(not checkLegalCrossings(y, E)): 
        #print("Failed legal crossing check: ", y)
        return 2
    cross_edges = findCrossedEdges(y, E)
    kite_edges = findKiteEdges(y, E, am)
    #note that the check below also takes care of crossings of type (a, b), (b, c) as that makes the crossing edges show up as kite edges
    #while this wasn't intended it works so it stays in, there might be a more elegant way of checking for this exception
    if(cross_edges.intersection(kite_edges) != set()): 
        #print("Failed cross/kite check: ", y)
        return 2

    Gv = computeInducedGraph(y, G, E, am, cross_edges, kite_edges)
    Gstar = createCrossVertices(y, Gv, E)

    if(nx.check_planarity(Gstar)[0]):
        if(nx.utils.graphs_equal(Gv, G)):
            if(verbose):
                nx.draw_planar(Gstar, with_labels = True) 
            #print(" Found planar drawing of G", y)
            return 0
        else:
            return 1
    else:
        #print("Failed planarity check: ", y)
        return 2

#INPUT: solution x,y, edge*edge List E, size of graph n
#OUTPUT: prints the added vertices and the crossing they represent
def createLog(x, y, E, n):
    if(x == 2):
        return
    m = len(y)
    print("Crossings in order: ")
    j = 0
    for i in range(m):
        if(y[i] == 1):
            print("Vertex ", n+j, " represents the crossing ", E[i])
            j += 1
    return


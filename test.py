import OnePlanarTester as opt
import sys
import networkx as nx
import matplotlib.pyplot as plt
adjacency_dict = {
0: (1, 2, 3, 4, 5, 6, 7),
1: (0, 2, 3, 4, 5, 6),
2: (0, 1, 3),
3: (0, 1, 2, 4, 5, 7),
4: (0, 1, 3, 5, 6, 7),
5: (0, 1, 3, 4, 6, 7),
6: (0, 1, 4, 5, 7),
7: (0, 3, 4, 5, 6)}
sys.stdout = open("log.txt", "w")
#G = nx.Graph(adjacency_dict)
G = nx.complete_graph(6)
E = opt.generateE(G)
n = len(E)
yi = []
for i in range(n):
    j = 0
    if(i == 36):
        j = 1
    if(i == 49):
        j = 1
    if(i == 97):
        j = 1
    if(i == 126):
        j = 1
    yi.append(j)
    #print(i, " ", E[i])
opt.createLog(1, yi, E, len(G))
x, y = opt.searchTree(yi, G, E)
print(x, y)
opt.createLog(x, y, E, len(G))
sys.stdout.close()
plt.show()
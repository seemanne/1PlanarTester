# 1PlanarTester

A Python implementation of the algorithm to test and embedd 1-planar graphs as described in the paper of Binucci et al. "An Experimental Study of a 1-Planarity Testing and Embedding Algorithm" https://doi.org/10.1007/978-3-030-39881-1_28 using the python networkx library as a basis. The scope of the algorithm has extended somewhat.  

OnePlanarTester.py implements the algorithm of binucci et al. with minor changes in how the induced edges are computed (Our implementation mainly removes non-induced edges as this has low complexity for nodes deep into the search tree)

MaxOnePlanarTester.py tests whether a given graph is maximal 1-planar by checking whether one could add any edge while keeping the graph one planar.

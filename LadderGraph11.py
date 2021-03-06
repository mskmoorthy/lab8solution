"""
Words/Ladder Graph
------------------
Generate  an undirected graph over the 5757 5-letter words in the
datafile words_dat.txt.gz.  Two words are connected by an edge
if they differ in one letter, resulting in 14,135 edges. This example
is described in Section 1.1 in Knuth's book [1]_,[2]_.

References
----------
.. [1] Donald E. Knuth,
   "The Stanford GraphBase: A Platform for Combinatorial Computing",
   ACM Press, New York, 1993.
.. [2] http://www-cs-faculty.stanford.edu/~knuth/sgb.html
"""
__author__ = """\n""".join(['Aric Hagberg (hagberg@lanl.gov)',
                            'Brendt Wohlberg',
                            'hughdbrown@yahoo.com'])
#    Copyright (C) 2004-2010 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.

import networkx as nx
wordsd={}
#-------------------------------------------------------------------
#   The Words/Ladder graph of Section 1.1
#-------------------------------------------------------------------
def generate_graph(words):
    from string import ascii_lowercase as lowercase
    G = nx.Graph(name="words")
    lookup = dict((c,lowercase.index(c)) for c in lowercase)
    def edit_distance_one(word):
        word1="".join(sorted(word))
        for i in reversed(range(len(word))):
            left, c, right = word1[0:i], word1[i], word1[i+1:]
            j = lookup[c] # lowercase.index(c)
            bound=25
            for cc in lowercase[0:bound]:
                if (cc !=c):
                    yield left + cc + right
##    candgen = ((word, cand) for word in sorted(words)
##  for cand1 in edit_distance_one(word) if ((cand1 in wordsd.values()) and (cand==wordsd.keys()[words.values.index(cand1)]))
    candgen=[]
    for word in sorted(words):
        for cand2 in edit_distance_one(word):
            cand1 = ''.join(sorted(cand2))
            if (cand1 in wordsd.values()):
                cand=wordsd.keys()[wordsd.values().index(cand1)]
                candgen.append([word,cand])
                                  
    G.add_nodes_from(words)
    for word, cand in candgen:
        G.add_edge(word, cand)
    return G

def words_graph():
    """Return the words example graph from the Stanford GraphBase"""
    import gzip
    fh=gzip.open('words_dat.txt.gz','r')
    words=set()
    for line in fh.readlines():
        line = line.decode()
        if line.startswith('*'):
            continue
        w=str(line[0:5])
        words.add(w)
        w1=''.join(sorted(w))
        wordsd[w]=w1
    return generate_graph(words)

if __name__ == '__main__':
    from networkx import *
    G=words_graph()
    print("Loaded words_dat.txt containing 5757 five-letter English words.")
    print("Two words are connected if they differ in one letter.")
    print("Graph has %d nodes with %d edges"
          %(number_of_nodes(G),number_of_edges(G)))
    print("%d connected components" % number_connected_components(G))
##    for (source,target) in [('love','hate'),
##                            ('warm','cold'),
##                            ('idle','busy')]:
    for (source,target) in [('chaos','order'),
                            ('nodes','graph'),
                            ('moron','smart'),
                            ('pound','marks')]:
        print("Shortest path between %s and %s is"%(source,target))
        try:
            sp=shortest_path(G, source, target)
            for n in sp:
                print(n)
        except nx.NetworkXNoPath:
            print("None")

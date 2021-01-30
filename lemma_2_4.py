"""A NOTE ON OPTIMAL DEGREE-THREE SPANNERS OF THE SQUARE LATTICE - PROOF OF LEMMA 2.4

Usage:
    lemma_2_4.py
    lemma_2_4.py (-h | --help)

Options:
    -h --help       Show this screen.

Explanation:
    This program performs the verification mentioned in the proof of Lemma 2.4.
"""

from docopt import docopt

from queue import PriorityQueue

from util import *

if __name__ == '__main__':
    arguments = docopt(__doc__)
    
    # Building the graph
    nodes = [(i, j) for i in range(-10, 11) for j in range(-10, 11)]

    graph = {}
    for p in nodes:
        graph[p] = []
        for q in nodes:
            d = manhattan(p, q)
            if d == 1:
                graph[p].append((q, SquareRootNumber(1, 1))) # 1 + sqrt(2)
            elif d == 2:
                graph[p].append((q, SquareRootNumber(2, 1))) # (1 + sqrt(2))*sqrt(2) = 2 + sqrt(2)
            elif d == 3:
                graph[p].append((q, SquareRootNumber(3, 1))) # 3 + sqrt(2)

    # Dijkstra's algorithm
    distances_from_origin = {}  # stores the graph distance between (0, 0) to all the other points
    pq = PriorityQueue()
    pq.put((SquareRootNumber(0, 0), (0, 0)))

    while not pq.empty():
        cur_dist, cur_point = pq.get()
        
        if not cur_point in distances_from_origin:    
            distances_from_origin[cur_point] = cur_dist
            for neigh, edge_length in graph[cur_point]:
                if not neigh in distances_from_origin:
                    pq.put((cur_dist + edge_length, neigh))

    # Checking the shortest path property
    for (x, y) in nodes:
        p1 = (0, 0)
        p2 = (x, y)
        
        square_dist_p1_p2 = SquareRootNumber(dist_squared(p1, p2), 0)   # we have to convert this integer explicitly to a SquareRootNumber
        if not(distances_from_origin[p2]**2 <= (SquareRootNumber(1, 1)**2)*square_dist_p1_p2):
            raise ValueError('The lemma is not verified for point', p2)

    print('The lemma is verified for all points (p, q) with -10 <= p, q <= 10')

"""A NOTE ON OPTIMAL DEGREE-THREE SPANNERS OF THE SQUARE LATTICE

Usage:
    launch.py prove (h1 | h2 | p1 | p2 | p3 | p4) (--text | --gui)
    launch.py prove all (--text | --gui)
    launch.py (-h | --help)

Options:
    -h --help       Show this screen.
    --text          Use the text-based interface.
    --gui           Use the graphical interface.
"""

from util import SquareRootNumber

class ToProve:
    def __init__(self, u, v, length_of_path, name, path_of_config, edges_to_consider, tot, known_lemmas):
        self.u = u
        self.v = v
        self.length_of_path = length_of_path
        self.name = name
        self.path_of_config = path_of_config
        self.edges_to_consider = edges_to_consider
        self.tot = tot
        self.known_lemmas = known_lemmas


# Lemma 1 --- "Small tile"
lemma1 = ToProve(None,
None,
None,
"h1",
[(0, 0), (-1, 0), (0, 1), (1, 0), (1, -1), (0, 0)],
[((1, 1), (2, 1)), ((1, 1), (1, 0)), ((1, 2), (2, 2)), ((1, 2), (1, 1)), ((0, 2), (1, 2)), ((0, 2), (0, 1)), ((-1, 1), (0, 1)), ((-1, 1), (-1, 0)), ((1, -1), (2, -1)), ((1, -1), (1, -2)), ((-1, 2), (-1, 1)), ((-1, 2), (0, 2)), ((2, 0), (3, 0)), ((2, 0), (2, -1)), ((2, 1), (3, 1)), ((2, 1), (2, 0)), ((2, 2), (3, 2)), ((2, 2), (2, 1)), ((0, 3), (0, 2)), ((-1, 3), (0, 3)), ((-1, 3), (-1, 2)), ((-1, 2), (0, 2)), ((-1, 2), (-1, 1))],
1467,
[])


# Lemma 2 --- "Zigzag"
lemma2 = ToProve(None,
None,
None,
"h2",
[(0, 2), (-1, 2), (-1, 1), (-1, 0), (0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)],
[((0, 0), (0, -1)), ((-1, 0), (-1, -1)), ((-1, 0), (-2, 0)), ((-1, 1), (-2, 1)), ((-2, 2), (-1, 2)), ((-1, 2), (-1, 3)), ((0, 2), (0, 3)), ((-1, 1), (0, 1)), ((1, 2), (2, 2)), ((1, 1), (2, 1)), ((1, 2), (1, 1)), ((2, 2), (3, 2)), ((2, 2), (2, 1)), ((1, 1), (1, 0)), ((2, 1), (3, 1)), ((2, 1), (2, 0)), ((1, 0), (2, 0)), ((1, 0), (1, -1)), ((2, 0), (3, 0)), ((2, 0), (2, -1)), ((0, 0), (1, 0)), ((0, 0), (0, -1)), ((1, -1), (2, -1)), ((0, -1), (1, -1)), ((-1, 0), (0, 0)), ((-1, 0), (-1, -1)), ((-1, -1), (0, -1)), ((-2, 0), (-1, 0)), ((-2, 0), (-2, -1)), ((-2, -1), (-1, -1)), ((-2, 1), (-1, 1)), ((-2, 1), (-2, 0)), ((-1, 1), (0, 1)), ((-1, 1), (-1, 0)), ((-2, 2), (-1, 2)), ((-2, 2), (-2, 1))],
922,
[lemma1])


three_first_paths_edges_to_consider = [((0, 2), (1, 2)), ((0, 2), (0, 1)), ((0, 1), (1, 1)), ((0, 1), (0, 0)), ((-1, 2), (0, 2)), ((-1, 2), (-1, 1)), ((-1, 1), (0, 1)), ((-1, 1), (-1, 0)), ((-2, 1), (-1, 1)), ((-2, 1), (-2, 0)), ((-2, 2), (-1, 2)), ((-2, 2), (-2, 1)), ((-2, 3), (-1, 3)), ((-2, 3), (-2, 2)), ((-1, 3), (0, 3)), ((-1, 3), (-1, 2)), ((0, 3), (1, 3)), ((0, 3), (0, 2)), ((1, 3), (2, 3)), ((1, 3), (1, 2)), ((1, 2), (2, 2)), ((1, 2), (1, 1)), ((1, 1), (2, 1)), ((1, 1), (1, 0)), ((1, 0), (2, 0)), ((1, 0), (1, -1)), ((0, 0), (1, 0)), ((0, 0), (0, -1)), ((-1, 0), (0, 0)), ((-1, 0), (-1, -1)), ((-2, 0), (-1, 0)), ((-2, 0), (-2, -1)), ((-1, -1), (0, -1)), ((-1, -1), (-1, -2)), ((0, -1), (1, -1)), ((0, -1), (0, -2)), ((1, -1), (2, -1)), ((1, -1), (1, -2)), ((2, 0), (3, 0)), ((2, 0), (2, -1)), ((2, 1), (3, 1)), ((2, 1), (2, 0)), ((2, 2), (3, 2)), ((2, 2), (2, 1)), ((2, 3), (3, 3)), ((2, 3), (2, 2)), ((1, 4), (2, 4)), ((1, 4), (1, 3)), ((2, 4), (3, 4)), ((2, 4), (2, 3)), ((3, 4), (4, 4)), ((3, 4), (3, 3)), ((3, 3), (4, 3)), ((3, 3), (3, 2)), ((3, 2), (4, 2)), ((3, 2), (3, 1)), ((0, 4), (1, 4)), ((0, 4), (0, 3)), ((-1, 4), (0, 4)), ((-1, 4), (-1, 3)), ((-2, 4), (-1, 4)), ((-2, 4), (-2, 3)), ((-3, 3), (-2, 3)), ((-3, 3), (-3, 2)), ((-3, 2), (-2, 2)), ((-3, 2), (-3, 1)), ((-3, 1), (-2, 1)), ((-3, 1), (-3, 0)), ((0, 5), (1, 5)), ((0, 5), (0, 4)), ((-4, 2), (-3, 2)), ((-4, 2), (-4, 1)), ((-1, 5), (0, 5)), ((-1, 5), (-1, 4)), ((0, -2), (1, -2)), ((0, -2), (0, -3)), ((0, 6), (1, 6)), ((0, 6), (0, 5)), ((1, 5), (2, 5)), ((1, 5), (1, 4)), ((3, 1), (4, 1)), ((3, 1), (3, 0)), ((4, 2), (5, 2)), ((4, 2), (4, 1)), ((-5, 2), (-4, 2)), ((-5, 2), (-5, 1)), ((-4, 1), (-3, 1)), ((-4, 1), (-4, 0)), ((-4, 3), (-3, 3)), ((-4, 3), (-4, 2)), ((-3, 0), (-2, 0)), ((-3, 0), (-3, -1)), ((-3, 4), (-2, 4)), ((-3, 4), (-3, 3)), ((-2, -1), (-1, -1)), ((-2, -1), (-2, -2)), ((-2, 5), (-1, 5)), ((-2, 5), (-2, 4)), ((-1, -2), (0, -2)), ((-1, -2), (-1, -3)), ((-1, 6), (0, 6)), ((-1, 6), (-1, 5)), ((0, -3), (1, -3)), ((0, -3), (0, -4)), ((0, 7), (1, 7)), ((0, 7), (0, 6)), ((1, -2), (2, -2)), ((1, -2), (1, -3)), ((1, 6), (2, 6)), ((1, 6), (1, 5)), ((2, -1), (3, -1)), ((2, -1), (2, -2)), ((2, 5), (3, 5)), ((2, 5), (2, 4)), ((3, 0), (4, 0)), ((3, 0), (3, -1)), ((4, 1), (5, 1)), ((4, 1), (4, 0)), ((4, 3), (5, 3)), ((4, 3), (4, 2)), ((5, 2), (6, 2)), ((5, 2), (5, 1))]


# First path of length 3*sqrt(2) + 1
path1 = ToProve((0, 0),
(1, 2),
SquareRootNumber(1, 3),
"p1",
[(0, 0), (-1, 1), (-1, 2), (0, 3), (1, 2)],
three_first_paths_edges_to_consider,
11,
[lemma1, lemma2])


# Second path of length 3*sqrt(2) + 1
path2 = ToProve((0, 0),
(1, 2),
SquareRootNumber(1, 3),
"p2",
[(0, 0), (-1, 1), (0, 2), (0, 3), (1, 2)],
three_first_paths_edges_to_consider,
8,
[lemma1, lemma2])


# Third path of length 3*sqrt(2) + 1
path3 = ToProve((0, 0),
(1, 2),
SquareRootNumber(1, 3),
"p3",
[(0, 0), (-1, 1), (0, 2), (1, 3), (1, 2)],
three_first_paths_edges_to_consider,
15,
[lemma1, lemma2])


# Path of length 5
path4 = ToProve((0, 0),
(1, 2),
SquareRootNumber(5, 0),
"p4",
[(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2)],
[((2, 1), (3, 1)), ((2, 1), (2, 0)), ((2, 0), (3, 0)), ((2, 0), (2, -1)), ((1, 1), (2, 1)), ((1, 1), (1, 0)), ((1, 0), (2, 0)), ((1, 0), (1, -1)), ((0, 0), (1, 0)), ((0, 0), (0, -1)), ((0, 1), (1, 1)), ((0, 1), (0, 0)), ((0, 2), (1, 2)), ((0, 2), (0, 1)), ((1, 2), (2, 2)), ((1, 2), (1, 1)), ((2, 2), (3, 2)), ((2, 2), (2, 1)), ((3, 2), (4, 2)), ((3, 2), (3, 1)), ((3, 1), (4, 1)), ((3, 1), (3, 0)), ((3, 0), (4, 0)), ((3, 0), (3, -1)), ((3, -1), (4, -1)), ((3, -1), (3, -2)), ((2, -1), (3, -1)), ((2, -1), (2, -2)), ((1, -1), (2, -1)), ((1, -1), (1, -2)), ((0, -1), (1, -1)), ((0, -1), (0, -2)), ((1, -2), (2, -2)), ((1, -2), (1, -3)), ((2, -2), (3, -2)), ((2, -2), (2, -3)), ((3, -2), (4, -2)), ((3, -2), (3, -3)), ((4, -1), (5, -1)), ((4, -1), (4, -2)), ((4, 0), (5, 0)), ((4, 0), (4, -1)), ((4, 1), (5, 1)), ((4, 1), (4, 0)), ((4, 2), (5, 2)), ((4, 2), (4, 1)), ((3, 3), (4, 3)), ((3, 3), (3, 2)), ((4, 3), (5, 3)), ((4, 3), (4, 2)), ((5, 3), (6, 3)), ((5, 3), (5, 2)), ((5, 2), (6, 2)), ((5, 2), (5, 1)), ((5, 1), (6, 1)), ((5, 1), (5, 0)), ((2, 3), (3, 3)), ((2, 3), (2, 2)), ((1, 3), (2, 3)), ((1, 3), (1, 2)), ((0, 3), (1, 3)), ((0, 3), (0, 2)), ((-1, 2), (0, 2)), ((-1, 2), (-1, 1)), ((-1, 1), (0, 1)), ((-1, 1), (-1, 0)), ((-1, 0), (0, 0)), ((-1, 0), (-1, -1)), ((2, 4), (3, 4)), ((2, 4), (2, 3)), ((-2, 1), (-1, 1)), ((-2, 1), (-2, 0)), ((1, 4), (2, 4)), ((1, 4), (1, 3)), ((2, -3), (3, -3)), ((2, -3), (2, -4)), ((2, 5), (3, 5)), ((2, 5), (2, 4)), ((3, 4), (4, 4)), ((3, 4), (3, 3)), ((5, 0), (6, 0)), ((5, 0), (5, -1)), ((6, 1), (7, 1)), ((6, 1), (6, 0)), ((-3, 1), (-2, 1)), ((-3, 1), (-3, 0)), ((-2, 0), (-1, 0)), ((-2, 0), (-2, -1)), ((-2, 2), (-1, 2)), ((-2, 2), (-2, 1)), ((-1, -1), (0, -1)), ((-1, -1), (-1, -2)), ((-1, 3), (0, 3)), ((-1, 3), (-1, 2)), ((0, -2), (1, -2)), ((0, -2), (0, -3)), ((0, 4), (1, 4)), ((0, 4), (0, 3)), ((1, -3), (2, -3)), ((1, -3), (1, -4)), ((1, 5), (2, 5)), ((1, 5), (1, 4)), ((2, -4), (3, -4)), ((2, -4), (2, -5)), ((2, 6), (3, 6)), ((2, 6), (2, 5)), ((3, -3), (4, -3)), ((3, -3), (3, -4)), ((3, 5), (4, 5)), ((3, 5), (3, 4)), ((4, -2), (5, -2)), ((4, -2), (4, -3)), ((4, 4), (5, 4)), ((4, 4), (4, 3)), ((5, -1), (6, -1)), ((5, -1), (5, -2)), ((6, 0), (7, 0)), ((6, 0), (6, -1)), ((6, 2), (7, 2)), ((6, 2), (6, 1)), ((7, 1), (8, 1)), ((7, 1), (7, 0))],
6155,
[lemma1, lemma2])


import sys
from docopt import docopt

import proof
import interface

if __name__ == '__main__':
    to_prove_dictionary = {
        'h1' : lemma1,
        'h2' : lemma2,
        'p1' : path1,
        'p2' : path2,
        'p3' : path3,
        'p4' : path4
    }

    arguments = docopt(__doc__)
    
    if arguments['--gui']:
        interface = interface.GUIInterface()
    else:
        interface = interface.TextInterface()
    
    if not arguments['all']:
        for to_prove_name in ['h1', 'h2', 'p1', 'p2', 'p3', 'p4']:
            if arguments[to_prove_name]:
                proof.prove(to_prove_dictionary[to_prove_name], interface)
    else:
        for to_prove_name in ['h1', 'h2', 'p1', 'p2', 'p3', 'p4']:
            proof.prove(to_prove_dictionary[to_prove_name], interface)

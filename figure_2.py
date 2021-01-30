"""A NOTE ON OPTIMAL DEGREE-THREE SPANNERS OF THE SQUARE LATTICE - PROOF OF LOCAL OPTIMALITY OF THE THREE EXAMPLES OF FIGURE 2

Usage:
    figure_2.py
    figure_2.py (-h | --help)

Options:
    -h --help       Show this screen.

Explanation:
    This program checks that the geometric graphs in Figure 2 are locally optimal.
    Since they are periodic, it suffices to verify Definition 1.2 for p in a fundamental parallelogram
    (the purple points in the GUI). 
"""

import sys

from docopt import docopt

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('qt5agg')
from matplotlib.widgets import Button, Slider

from queue import PriorityQueue

from util import *

from proposition_2_1 import verify_shortest_paths, GUI

def fundamental_parallelogram(v1, v2):
    '''
    Given two small vectors v1, v2 with integer coefficients, returns the list of points
    with integer coefficients contained in the parallelogram based at (0, 0) and with v1, v2 as sides.
    '''
    
    x1, y1 = v1
    x2, y2 = v2
    
    length_v1_squared = x1**2 + y1**2
    length_v2_squared = x2**2 + y2**2
    
    ls_points = []
    for x in range(-10, 11):
        for y in range(-10, 11):
            scalar_product_1 = x*x1 + y*y1
            scalar_product_2 = x*x2 + y*y2
            
            if 0 <= scalar_product_1 and 0 <= scalar_product_2 and scalar_product_1 < length_v1_squared and scalar_product_2 < length_v2_squared:
                ls_points.append((x, y))
    return ls_points


def translate(p, vec):
    return (p[0]+vec[0], p[1]+vec[1])

def add_path(path, shift, edges):
    l = len(path)
    for i in range(l-1):
        a, b = translate(path[i], shift), translate(path[i+1], shift)
        if not (a, b) in edges:
            edges.add((a, b))
        if not (b, a) in edges:
            edges.add((b, a))

def first_config():
    edges = set()
    for i in range(-3, 4):
        for j in range(-3, 4):
            # fundamental parallelogram
            shift = (4*i+2*j, -3*j)
            add_path([(0, 1), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (5, 1), (4, 2), (3, 3)], shift, edges)
            add_path([(2, 0), (2, 1), (1, 2), (1, 1)], shift, edges)
            add_path([(1, 2), (2, 2), (1, 3)], shift, edges)
            add_path([(2, 1), (3, 1), (4, 0)], shift, edges)
            add_path([(3, 1), (3, 2)], shift, edges)
            add_path([(2, 2), (3, 2), (4, 2)], shift, edges)
    return edges, fundamental_parallelogram((4, 0), (2, -3))


def second_config():
    edges = set()
    for i in range(-3, 4):
        for j in range(-3, 4):
            # fundamental parallelogram
            shift = (3*i+4*j, 2*i-4*j)
            add_path([(0, 0), (1, 0), (1, -1), (2, -1), (2, -2), (3, -2), (3, -3), (4, -3)], shift, edges)
            add_path([(4, -3), (4, -4), (5, -3), (6, -2), (7, -1)], shift, edges)
            add_path([(1, -1), (2, 0), (2, 1), (1, 1)], shift, edges)
            add_path([(3, -3), (4, -2), (4, -1), (4, 0), (3, -1), (2, -2)], shift, edges)
            add_path([(6, -2), (5, -2), (5, -1), (6, 0)], shift, edges)
            add_path([(4, -2), (5, -2)], shift, edges)
            add_path([(4, -1), (5, -1)], shift, edges)
            add_path([(4, 0), (5, 1)], shift, edges)
            add_path([(2, 0), (3, 0)], shift, edges)
            add_path([(2, 1), (3, 1)], shift, edges)
            add_path([(3, -1), (3, 0), (3, 1), (4, 2)], shift, edges)
    return edges, fundamental_parallelogram((3, 2), (4, -4))


def third_config():
    edges = set()
    for i in range(-3, 4):
        for j in range(-3, 4):
            # fundamental parallelogram
            shift = (2*i+4*j, 3*i-3*j)
            add_path([(0, 0), (1, 1), (2, 2), (3, 3), (3, 2), (4, 2), (4, 1), (5, 1), (5, 0), (6, 1), (6, 0), (7, 0)], shift, edges)
            add_path([(2, 2), (2, 1), (2, 0), (3, 0), (3, -1), (4, 0), (4, -1), (5, -1), (5, -2)], shift, edges)
            add_path([(4, -1), (4, -2)], shift, edges)
            add_path([(2, -2), (3, -1)], shift, edges)
            add_path([(1, -1), (2, 0)], shift, edges)
            add_path([(5, -1), (5, 0)], shift, edges)
            add_path([(3, 1), (4, 2)], shift, edges)
            add_path([(4, 0), (5, 1)], shift, edges)
            add_path([(2, 1), (3, 1), (3, 0)], shift, edges)
    return edges, fundamental_parallelogram((2, 3), (4, -3))


if __name__ == '__main__':
    arguments = docopt(__doc__)
    
    gui = GUI(False)

    ls_configs = [first_config(), second_config(), third_config()]
    ls_titles = ['FIRST', 'SECOND', 'THIRD']

    for i in range(3):
        gui.set_title(ls_titles[i] + ' CONFIGURATION')
        config, possible_values_for_p1 = ls_configs[i]
        
        gui.visualize(config, [], possible_values_for_p1)
        verify_shortest_paths(config, possible_values_for_p1)
        
        while not gui.next:
            plt.pause(0.001)
        gui.next = False

"""A NOTE ON OPTIMAL DEGREE-THREE SPANNERS OF THE SQUARE LATTICE - PROOF OF PROPOSITION 2.1

Usage:
    proposition_2_1.py (--text | --gui)
    proposition_2_1.py (-h | --help)

Options:
    -h --help       Show this screen.
    --text          Use the text-based interface.
    --gui           Use the graphical interface.

Explanation:
    Let H be te periodic geometric graph in solid lines shown in Figure 3 in the article (here H will be displayed in blue in the GUI). 
    Let p1, p2 be two points in Z² with |p1p2| <= √5.
    Since H is periodic, we may assume that p1 is one of the points displayed in purple in the GUI (see possible_points_for_p1).
    This program iterates over all choices of p1 (purple points), all choices of p2 (close to p1)
    and all choices of vertical/horizontal segments (that are relevant to p1 and p2)
    to determine if there is a path of dilation at most 1+√2 in all cases.
"""

import sys

from docopt import docopt

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('qt5agg')
from matplotlib.widgets import Button, Slider

from queue import PriorityQueue

from util import *


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


def initial_config():
    edges = set()
    for i in range(-4, 5):
        for j in range(-4, 5):
            # fundamental parallelogram
            shift = (2*i+5*j, -2*i)
            add_path([(0, 0), (1, 1), (1, 2), (2, 2), (3, 3), (3, 2), (4, 2), (4, 1), (5, 1)], shift, edges)
            add_path([(1, 1), (2, 1), (2, 2)], shift, edges)
            add_path([(1, -1), (2, 0), (3, 1), (4, 2),], shift, edges)
    
    return edges


def exhaustive(gui):
    possible_values_for_p1 = [(1, -1), (2, -1), (3, -1), (1, 0), (2, 0), (3, 0), (4, 0), (2, 1), (3, 1), (3, 2)]
    points_with_choice_for_graph_edges = [(0, 3), (2, 1), (4, -1), (-1, -1)]
    
    edges = initial_config()
    
    nb_choices = len(points_with_choice_for_graph_edges)
    number_of_cases = 2**nb_choices
    
    progress_counter = 0
    for mask in range(number_of_cases): # to iterate on all possible choices of vertical and horizontal segments
        progress_counter += 1
        
        if gui is None:
            print('Progress:', str(progress_counter) + '/' + str(number_of_cases))
        else:
            gui.progress_slider.set_val(100*progress_counter/number_of_cases)
        
        new_edges = []
        for i in range(nb_choices):
            x, y = points_with_choice_for_graph_edges[i]
            if(mask & (1 << i)):
                # we use horizontal segmnents at this point
                new_edges.append(((x, y), (x+1, y)))
                new_edges.append(((x, y-1), (x+1, y-1)))
            else:
                # we use vertical segmnents at this point
                new_edges.append(((x, y), (x, y-1)))                
                new_edges.append(((x+1, y), (x+1, y-1)))           
        
        if gui is not None:
            gui.visualize(edges, new_edges, possible_values_for_p1)
            while not gui.next:
                plt.pause(0.001)
            gui.next = False
        
        for a, b in new_edges:
            edges.add((a, b))
            edges.add((b, a))
        
        verify_shortest_paths(edges, possible_values_for_p1)
        
        for a, b in new_edges:
            edges.remove((a, b))
            edges.remove((b, a))
            

def verify_shortest_paths(config, possible_values_for_p1):
    # create the adjacency lists from the set of edges
    nodes = set()
    neighbours = {} # nodes adjacent to a given node
    graph = {}      # weighed edges starting from a given node
    for a, b in config:
        nodes.add(a)
        nodes.add(b)
        neighbours[a] = set()
        neighbours[b] = set()
        graph[a] = []
        graph[b] = []
    
    for a, b in config:
        neighbours[a].add(b)
        neighbours[b].add(a)
    
    # initialize the weights in the adjacency lists
    for a in nodes:
        for b in neighbours[a]:
            if manhattan(a, b) == 1:
                graph[a].append((b, SquareRootNumber(1, 0)))   # length 1
            elif manhattan(a, b) == 2:
                graph[a].append((b, SquareRootNumber(0, 1)))   # length √2
            else:
                print(a, b)
                raise ValueError('Some edges are longer than sqrt(2)')
    
    # Dijkstra's algorithm
    for p1 in possible_values_for_p1:
        distances = {}
        pq = PriorityQueue()
        pq.put((SquareRootNumber(0, 0), p1))
        
        number_of_close_points = 0  # number of points with Euclidean distance at most √5 from p1

        while not pq.empty() and number_of_close_points < 21:   # there are 21 possible values for p2
            cur_dist, cur_point = pq.get()
            
            if not cur_point in distances:
                if dist_squared(p1, cur_point) <= 5:
                    number_of_close_points += 1
            
                distances[cur_point] = cur_dist
                for neigh, edge_length in graph[cur_point]:
                    if not neigh in distances:
                        pq.put((cur_dist + edge_length, neigh))

        x1, y1 = p1
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                p2 = (x1+dx, y1+dy)
                if dist_squared(p1, p2) <= 5:
                    square_dist_p1_p2 = SquareRootNumber(dist_squared(p1, p2), 0)   # we have to convert this integer explicitly to a SquareRootNumber
                    if not(distances[p2]**2 <= (SquareRootNumber(1, 1)**2)*square_dist_p1_p2):
                        raise ValueError('Some dilations are greater than sqrt(2): ' + str(p1) + ', ' + str(p2))

class GUI:
    def __init__(self, _is_progress_bar=True):
        self.fig = plt.figure(figsize=(10, 8), dpi=80)
        self.ax = self.fig.add_subplot(111, aspect='equal')
        self.__init_axes()
        
        def handle_close(evt):
            print('Execution terminated')
            plt.close('all')
            sys.exit()
        
        self.fig.canvas.mpl_connect('close_event', handle_close)
        
        widget_color = 'palegoldenrod'
        
        if _is_progress_bar:
            self.fig.subplots_adjust(bottom=0.2)
            
            self.progress_slider_ax = self.fig.add_axes([0.15, 0.08, 0.75, 0.04], facecolor=widget_color)
            self.progress_slider = Slider(self.progress_slider_ax, 'Progress', 0, 100, valinit=0, dragging=False)
            self.progress_slider.set_active(False)
            
        self.next_button_ax = self.fig.add_axes([0.8, 0.01, 0.1, 0.04])
        self.next_button = Button(self.next_button_ax, 'Next', color=widget_color, hovercolor='lightgray')
        self.next = False
        
        def next_button_callback(mouse_event):
            self.next = True
        
        self.next_button.on_clicked(next_button_callback)
    
    def __init_axes(self):
        x_ticks = range(-5, 10)
        y_ticks = range(-7, 8)
        self.ax.set_xticks(x_ticks)
        self.ax.set_yticks(y_ticks)
        self.ax.set_xlim([-5, 9])
        self.ax.set_ylim([-7, 7])
        self.ax.grid(which='both')

    def visualize(self, edges, new_edges=[], possible_values_for_p1=[]):
        self.ax.cla()
        self.__init_axes()
        
        for seg in edges:
            a, b = seg
            xa, ya = a
            xb, yb = b
            self.ax.plot((xa, xb), (ya, yb), color='blue')
        
        for seg in new_edges:
            a, b = seg
            xa, ya = a
            xb, yb = b
            self.ax.plot((xa, xb), (ya, yb), linewidth=3, color='orange')
        
        for pt in possible_values_for_p1:
            x, y = pt
            self.ax.plot([x], [y], marker='o', markersize=10, color='purple')
        
        plt.pause(0.001)
    
    def set_title(self, title):
        self.fig.canvas.set_window_title(title)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    
    if arguments['--gui']:
        gui = GUI(True)
        gui.set_title('UNCOUNTABLY MANY LOCALLY OPTIMAL GEOMETRIC GRAPHS')
    else:
        gui = None
    
    exhaustive(gui)
    
    print('Check successful')

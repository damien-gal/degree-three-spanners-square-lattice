"""A NOTE ON OPTIMAL DEGREE-THREE SPANNERS OF THE SQUARE LATTICE - PROOF OF LEMMA 3.8

Usage:
    lemma_3_8.py
    lemma_3_8.py (-h | --help)

Options:
    -h --help       Show this screen.

Explanation:
    This program performs the verification mentioned in the proof of Lemma 3.8.
"""

import sys
from docopt import docopt

import sympy as s
import numpy as np

import matplotlib
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt

from matplotlib.widgets import Button


# -----------------------------------------------------------------------------------------------------------------
# BASIC GEOMETRY
directions = [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1] if (i, j) != (0, 0)]


def translate(p, v):
    '''
    Returns the image of the point p by the translation of vector v.
    '''
    px, py = p
    vx, vy = v
    return (px+vx, py+vy)


def dist(p, q):
    '''
    Returns the Euclidean distance between points p and q.
    '''
    px, py = p
    qx, qy = q
    return s.sqrt((px-qx)*(px-qx)+(py-qy)*(py-qy))


def norm(v):
    '''
    Given a vector v, returns its Euclidean norm.
    '''
    return dist(v, (0, 0))


# -----------------------------------------------------------------------------------------------------------------
# EXHAUSTIVE SEARCH
def paths_bounded_length(start, end, min_length, max_length):
    '''
    Returns all paths (without cycle) between 'start' and 'end' of
    length 'l' such that min_length < l <= max_length.
    '''
    if dist(start, end) > max_length:
        return []
    if start == end:
        if min_length < 0:
            return [[start]]
        else:
            return []
    ans = []
    for d in directions:
        next = translate(start, d)
        cur_paths = paths_bounded_length(
            next, end, min_length-norm(d), max_length-norm(d))
        for path in cur_paths:
            if start not in path:
                ans.append([start]+path)
    return ans


def there_is_obvious_shorter_path(path, max_dilation=1+s.sqrt(2)):
    '''
    Returns 'True' if there necessarily exists a path which is shorter than 
    the given path, using the 'max_dilation' constraint.
    '''
    n = len(path)
    partial_sums = [0] # length of the path from its first vertex to its i-th vertex
    for i in range(1, n):
        path_dist = partial_sums[i-1]+dist(path[i-1], path[i])
        partial_sums.append(path_dist)

    for i in range(n):
        for j in range(i, n):
            path_dist = partial_sums[j] - partial_sums[i]
            max_dist = max_dilation * dist(path[i], path[j])
            if path_dist > max_dist:
                return True, (path[i], path[j], max_dist)
    return False, None


# -----------------------------------------------------------------------------------------------------------------
# GUI
def plot_path(fig, ax, path):
    ax.cla()
    x_coord = [p[0] for p in path]
    y_coord = [p[1] for p in path]
    x_ticks = np.arange(-2, 4, 1)
    y_ticks = np.arange(-2, 5, 1)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.set_xlim([-2, 3])
    ax.set_ylim([-2, 4])
    ax.grid(which='both')
    ax.plot(x_coord, y_coord)
    fig.canvas.draw_idle()
    plt.pause(0.001)


def wait_loop(fig):
    while fig.in_pause:
        fig.canvas.start_event_loop(0.001)


def wait_until_next_button_pressed(fig):
    fig.in_pause = True
    wait_loop(fig)


def init_GUI():
    fig = plt.figure(figsize=(10, 8), dpi=80)
    def handle_close(evt):
        print('Execution terminated')
        exit()
    fig.canvas.mpl_connect('close_event', handle_close)

    ax = fig.add_subplot(111, aspect='equal')
    fig.subplots_adjust(left=0.2, bottom=0.2)
    fig.canvas.set_window_title('Considering all possible paths')


    fig.in_pause = False


    next_button_ax = fig.add_axes([0.8, 0.01, 0.1, 0.04])
    next_button = Button(next_button_ax, 'Next',
                         color='palegoldenrod', hovercolor='lightgray')


    def next_button_callback(mouse_event):
        fig.in_pause = False

    next_button.on_clicked(next_button_callback)
    return fig, ax, next_button


# -----------------------------------------------------------------------------------------------------------------
# MAIN PROGRAM
if __name__ == '__main__':
    arguments = docopt(__doc__)

    # SHOW ALL POSSIBLE PATHS AND FIND VALID PATHS AMONG THEM
    fig, ax, next_button = init_GUI()

    list_paths = paths_bounded_length(
        (0, 0), (1, 2), 3+s.sqrt(2), s.sqrt(5)*(1+s.sqrt(2)))

    valid_paths = []

    for i, path in enumerate(list_paths):
        print("Considering path", i+1, "out of", len(list_paths))
        invalid, reason = there_is_obvious_shorter_path(path)
        plot_path(fig, ax, path)
        if invalid:
            p, q, max_dist = reason
            print("Not a shortest path: problem between", p, "and", q)
            print("There must exist a path of distance at most",
                  max_dist, "between those points.")
            ax.plot([p[0], q[0]], [p[1], q[1]], color="red", linestyle="--")
            fig.canvas.draw_idle()
            plt.pause(0.001)
        else:
            print("Valid shortest path.")
            valid_paths.append(path)

        wait_until_next_button_pressed(fig)


    # SHOW ALL VALID PATHS
    print("\n"+"-"*77)
    print("\nThe valid paths are:")
    fig.canvas.set_window_title('Valid paths')

    for path in valid_paths:
        print(path)
        plot_path(fig, ax, path)

        wait_until_next_button_pressed(fig)

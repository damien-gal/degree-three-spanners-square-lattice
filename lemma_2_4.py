import sympy as s
import numpy as np

import matplotlib
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt

# Let p and q be points in Z^2 with 0 < |pq| < 64.
# Without loss of generality, we will assume that p = (0, 0)
# and q = (i, j) with 0 <= j <= i.
# For every possible point q = (i, j), the program constructs a path between p = (0, 0) and q
# consisting of segments of the following types:
# * [euclidean length = 1] and [weight = 1 + sqrt(2)];
# * [euclidean length = sqrt(2)] and [weight = 2 + sqrt(2)];
# * [euclidean length = sqrt(5)] and [weight = 3 + sqrt(2)].
# The program then checks that the weighted length of the path is not more than (1+sqrt(2)) * |pq|.

# A drawing of the path is plotted when the optional 'figure' argument is True.
# Some additional explanatory text is printed if 'details' is True.
# The sympy library is used for symbolic computations of expressions involving square roots of integers.


def can_be_reached(pt, details, figure):
    def next_point(pt):
        '''
        Given a point pt, returns the next point on the path from pt to (0, 0)
        that is being constructed.
        '''
        x, y = pt
        if y == 0:
            if x <= 3:
                return (x-1, y), 1+s.sqrt(2)
            else:
                return (x-2, y+1), 3+s.sqrt(2)
        elif x == y:
            if pt == (1, 1):
                return (0, 0), 2+s.sqrt(2)
            else:
                return (x-1, y-2), 3+s.sqrt(2)
        else:
            return (x-2, y-1), 3+s.sqrt(2)

    x, y = pt
    eucl_dist = s.sqrt(x**2+y**2)

    list_points = [pt]
    path_dist = 0
    while pt != (0, 0):
        pt, dist = next_point(pt)
        list_points += [pt]
        path_dist += dist
    path_dil = s.simplify(path_dist/eucl_dist)

    successful = path_dil <= 1+s.sqrt(2)

    if details:
        print("From (0, 0) to ", list_points[0])
        print("List of points in the path:", list_points)
        print("(Weighted) length of the path:", path_dist)
        print("(Weighted) dilation of the path:", path_dil, "==", str(s.N(path_dil, 4))+"...")
        print("The path has (weighted) dilation at most 1+sqrt(2):", successful)
        print()

    if figure:
        x_coord = [p[0] for p in list_points]
        y_coord = [p[1] for p in list_points]
        fig = plt.figure()
        ax = fig.add_subplot(111, aspect='equal')
        x_ticks = np.arange(-1, x+1, 1)
        y_ticks = np.arange(-1, y+1, 1)
        ax.set_xticks(x_ticks)
        ax.set_yticks(y_ticks)
        ax.grid(which='both')
        plt.plot(x_coord, y_coord)
        plt.draw()
        plt.pause(0.001)
        plt.clf()
        plt.close()

    return successful


if __name__ == "__main__":
    for i in range(1, 64):
        for j in range(0, i+1):
            if i**2 + j**2 < 64**2:  # Cases that need to be checked
                # It is discouraged to display a figure at every iteration
                # considering the number of pairs (i, j)
                if not can_be_reached((i, j), details=True, figure=False):
                    raise("The proof did not work.")

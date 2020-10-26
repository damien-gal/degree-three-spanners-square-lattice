# -----------------------------------------------------------------------------------------------------------------
# CLASS FOR REPRESENTING DISTANCES EXACTLY

class SquareRootNumber():
    '''
    A SquareRootNumber is an element of Z[sqrt(2)], i.e. a number of the
    form a+b*sqrt(2), for integers a and b.
    Attributes: a and b, integers.
    Methods: standard arithmetic operations and comparisons.
    '''

    def __init__(self, _a, _b):  # a+b*sqrt(2)
        self.a = _a
        self.b = _b

    def __str__(self):
        return str(self.a)+" + "+str(self.b)+"*sqrt(2)"

    def __add__(self, nb):
        return SquareRootNumber(self.a+nb.a, self.b+nb.b)

    def __sub__(self, nb):
        return SquareRootNumber(self.a-nb.a, self.b-nb.b)

    def __mul__(self, nb):
        a1, b1 = (self.a, self.b)
        a2, b2 = (nb.a, nb.b)
        return SquareRootNumber(a1*a2 + 2*b1*b2, a1*b2 + b1*a2)

    def __pow__(self, exponent):  # exponent is a nonnegative integer
        ans = SquareRootNumber(1, 0)
        for _ in range(exponent):
            ans *= self
        return ans

    def is_positive(self):
        a, b = (self.a, self.b)
        if a < 0:
            if b <= 0:
                return False
            else:  # b > 0
                return 2*b**2 > a**2
        else:  # a >= 0
            if b > 0:
                return True
            else:  # b <= 0
                return a**2 > 2*b**2

    def __eq__(self, nb):
        return self.a == nb.a and self.b == nb.b

    def __ne__(self, nb):
        return not self == nb

    def __lt__(self, nb):
        return (nb - self).is_positive()

    def __gt__(self, nb):
        return nb < self

    def __le__(self, nb):
        return (self == nb) or (self < nb)

    def __ge__(self, nb):
        return (self == nb) or (self > nb)

# -----------------------------------------------------------------------------------------------------------------
# LISTS WITH THE POSSIBLE DIRECTIONS


# All 8 directions (right, upRight, ...) together with the norm (sqrt(2) if diagonal, 1 otherwise)
directions = []
for _i in [-1, 0, 1]:
    for _j in [-1, 0, 1]:
        if (_i, _j) != (0, 0):
            if _i != 0 and _j != 0:
                _norm = SquareRootNumber(0, 1)
            else:
                _norm = SquareRootNumber(1, 0)
            directions.append(((_i, _j), _norm))

# -----------------------------------------------------------------------------------------------------------------
# HELPER FUNCTIONS


def translate(p, v):
    '''Returns the image of the point p by the translation of vector v.'''
    px, py = p
    vx, vy = v
    return (px+vx, py+vy)


def vec(p, q):
    '''Returns the components of the vector joining p and q.'''
    px, py = p
    qx, qy = q
    return (qx-px, qy-py)


def dist_squared(p, q):
    '''Returns the square of the Euclidean distance between p and q.'''
    px, py = p
    qx, qy = q
    return (px-qx)**2 + (py-qy)**2


def manhattan(p, q):
    '''Usual manhattan distance between p and q.'''
    vx, vy = vec(p, q)
    return abs(vx) + abs(vy)


def manhattan_with_diagonals(p, q):
    '''
    Returns the modified manhattan distance between p and q,
    where it is also allowed to use diagonals.
    '''
    vx, vy = vec(p, q)
    m = min(abs(vx), abs(vy))
    M = max(abs(vx), abs(vy))
    return SquareRootNumber(M - m, m)


def is_close_to(p, set_of_pts, d):
    '''
    Given a point p, a set of points set_of_pts and a distance d,
    returns True if and only if p is at distance at most d from
    at least a point of set_of_pts.
    '''
    for q in set_of_pts:
        if manhattan(p, q) <= d:
            return True
    return False


def path_to_list_of_edges(path):
    '''Given a path, i.e. a list of points, return the associated list of edges.
    If points are numbered p[0], ... p[l-1],
    this function returns the list of edges
    (p[0], p[1]), (p[1], p[2]), ..., (p[l-2], p[l-1])'''
    ans = []
    l = len(path)
    for i in range(l-1):
        ans.append((path[i], path[i+1]))
    return ans


def the_five_short_paths(p, q):
    '''
    Given two points p and q such that |pq| = 1,
    returns the list of 5 paths joining p and q
    of length at most 1+sqrt(2).
    '''
    right_up_left_down = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    i = right_up_left_down.index(vec(p, q))
    rotated_left = right_up_left_down[(i+1) % 4]
    rotated_right = right_up_left_down[(i+3) % 4]

    ls_paths = [[p, q]]  # the first path is made only of the edge (p, q)
    for pt in [p, q]:
        for v in [rotated_left, rotated_right]:
            # the 4 other paths are of the form (p, r, q)
            ls_paths.append([p, translate(pt, v), q])
    return ls_paths

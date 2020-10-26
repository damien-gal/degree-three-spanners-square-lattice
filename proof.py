import math
import copy
import numpy as np
from numpy.linalg import matrix_power

from util import *  # file with SquareRootNumber class, helper functions and data


# -----------------------------------------------------------------------------------------------------------------
# GLOBAL VARIABLES

DIL = SquareRootNumber(1, 1)


# -----------------------------------------------------------------------------------------------------------------
# TRAVERSAL

def can_add_path(path):
    '''
    Given a path, returns True iff
    1) no edge of the path is a forbidden edge
    2) every vertex has degree at most 3 after adding the edges from this path to the already existing edges
    '''

    degree_increment = {}    # maps points to the increment in degree they receive
    l = len(path)
    for i in range(l-1):
        a = path[i]
        b = path[i+1]

        if (a, b) in forbidden_edges:
            return False

        if not (a, b) in edges:  # already existing edges are fine
            for p in [a, b]:
                degree_increment[p] = degree_increment.get(p, 0) + 1
                # p will have a degree > 3 after adding the edge
                if degree_increment[p] + deg.get(p, 0) > 3:
                    return False
    return True


def exists_good_path(p, q):
    '''
    Returns True iff there exists a path between p and q,
    made only of existing edges of length at most DIL*|pq|.
    '''
    d_pq_squared = dist_squared(p, q)

    def DFS(u, lg, previous=None):
        '''
        We are currently at u and we want to reach q. 
        The variable 'lg' is the distance already traveled between p and u.
        '''

        if u == q:
            return lg**2 <= (DIL**2)*SquareRootNumber(d_pq_squared, 0)

        # pruning using manhattan_with_diagonals which is a lower bound of the length of the path from q to u
        if (lg + manhattan_with_diagonals(q, u))**2 > (DIL**2) * SquareRootNumber(d_pq_squared, 0):    # the dilation is too big
            return False  # we end the exploration of the current path

        for d, norm in directions:
            v = translate(u, d)
            if (v != previous) and ((u, v) in edges):   # we don't go back and use an existing edge
                if DFS(v, lg+norm, u):
                    return True
                # else we continue to explore all possible paths
        return False    # we did not find any valid end to the current path

    return DFS(p, SquareRootNumber(0, 0))


def find_paths(p, q, max_nb_paths=math.inf):
    '''
    Returns a list of paths between p and q of length at most DIL*|pq|.
    The edges of those paths may or may not in 'edges'.
    The paths must satisfy the conditions of the function 'can_add_path'.

    The size of this list is limited to at most 'max_nb_paths' different paths.
    The list is exhaustive unless the limit 'max_nb_paths' has been reached.
    '''
    d_pq_squared = dist_squared(p, q)

    paths = []

    def DFS(u, lg, path):   # we are currently at u and we want to reach q
        '''
        We are currently at u and we want to reach q. 
        The variable 'path' is the current path from p to u, and 'lg' is the length of this path.

        Returns True if enough paths are found and we can stop the search,
        False if more paths needs to be considered.
        Valid paths are added to the list 'paths'.
        '''

        if u == q and (lg**2 <= (DIL**2) * SquareRootNumber(d_pq_squared, 0)) and can_add_path(path):
            paths.append(path)
            return len(paths) == max_nb_paths    # True if we must stop

        # pruning
        if (lg + manhattan_with_diagonals(q, u))**2 > (DIL**2) * SquareRootNumber(d_pq_squared, 0):
            return False  # we end the exploration of the current path

        for d, norm in directions:
            v = translate(u, d)
            # we don't go back and go through an allowed edge
            if ((len(path) == 1) or (v != path[-2])) and not (u, v) in forbidden_edges:
                if DFS(v, lg+norm, path+[v]):
                    return True
        return False

    DFS(p, SquareRootNumber(0, 0), [p])
    return paths


def find_shortcut(p, q, c):
    '''
    If we can infer that there exists a path between p and q,
    with length strictly less than c, it returns this path. Otherwise, returns None. 


    The strategy is as follows: if a and b are two vertices with |ab| <= sqrt(5),
    - if ab is in 'edges', we know that there is a segment of length |ab| between a and b;
    - in all cases, we know that there is a path of length at most |ab|*DIL between them (*)
      (since the geometric graph has local dilation DIL = 1+sqrt(2)).
    '''

    def DFS(u, lg, prev=None):   # we are currently at u and we want to reach q, length of current path is 'lg'
        if u == q and lg < c:
            return [q]

        # pruning
        if lg + manhattan_with_diagonals(q, u) >= c:
            return None  # we end the exploration of the current path

        for d, norm in directions:
            v = translate(u, d)
            if (u, v) not in edges:
                norm *= SquareRootNumber(1, 1)  # explanation above, see (*)

            if v != prev:
                shortcut = DFS(v, lg+norm, v)
                if shortcut is not None:
                    return [u] + shortcut
        return None
    return DFS(p, SquareRootNumber(0, 0))


def add_path(path):
    '''
    Adds all the edges from a path given as a list of points,
    assuming it can be added (needs to be checked earlier by can_add_path).
    Returns:
    - added_edges: a list of added edges (with exactly one of (a, b) and (b, a)).
    - added_points: a list of added points.
    - new_forbidden: a list of new forbidden edges (with exactly one of (a, b) and (b, a)).
    '''

    def add_edge(a, b):
        '''
        Adds a bidirectional edge between points a and b to 'edges'.
        Assumes that it is possible and that the edge does not already exist.
        Returns a list of new forbidden edges.
        '''

        for p in [a, b]:
            deg[p] = deg.get(p, 0) + 1

        edges.update([(a, b), (b, a)])

        new_forbidden = []

        if manhattan(a, b) == 2:  # (a, b) is a diagonal edge -> the crossing diagonal becomes forbidden
            dx, dy = vec(a, b)
            c = translate(a, (dx, 0))
            # (c, d) is the diagonal that crosses (a, b)
            d = translate(a, (0, dy))
            if ((c, d) not in edges) and ((c, d) not in forbidden_edges):
                forbidden_edges.update([(c, d), (d, c)])
                new_forbidden.extend([(c, d), (d, c)])

        # if one of the endpoints of the edge now has degree 3, more forbidden edges need to be added
        for p in [a, b]:
            if deg[p] == 3:
                for d, _ in directions:
                    c = translate(p, d)
                    if ((p, c) not in edges) and ((p, c) not in forbidden_edges):
                        forbidden_edges.update([(p, c), (c, p)])
                        new_forbidden.extend([(p, c), (c, p)])

        return new_forbidden

    added_edges = []
    added_points = []
    new_forbidden = []

    l = len(path)
    for i in range(l-1):
        a = path[i]
        b = path[i+1]
        if not (a, b) in edges:
            added_edges.append((a, b))
            new_forbidden.extend(add_edge(a, b))

        for p in [a, b]:
            if not p in points:
                added_points.append(p)
                points.add(p)

    return added_edges, added_points, new_forbidden


def remove_path(added_edges, added_points, new_forbidden):
    '''
    Undoes the changes made by a previous call to add_path.
    '''
    for edge in added_edges:
        a, b = edge
        deg[a] -= 1
        deg[b] -= 1
        edges.difference_update({(a, b), (b, a)})
    points.difference_update(added_points)
    forbidden_edges.difference_update(new_forbidden)


# -----------------------------------------------------------------------------------------------------------------
# PATTERN DETECTION

def detect_pattern(p, pattern):
    '''
    Given a point p and a pattern (a set of edges),
    checks if the pattern is present in 'edges' at the point p.

    If the pattern is not there, returns None;
    otherwise returns the point of the pattern corresponding to p.
    '''
    points_of_pattern = set()
    for a, b in pattern:
        points_of_pattern.update([a, b])

    for pattern_point in points_of_pattern:
        v = vec(pattern_point, p)   # translation vector from pattern to edges

        cur_ok = True
        for a, b in pattern:
            if (translate(a, v), translate(b, v)) not in edges:
                cur_ok = False
                break

        if cur_ok:
            return pattern_point

    return None


def pattern_created_by_recent_add(recent_points):
    '''
    Checks if one of the patterns in 'list_of_patterns' can be found in 'edges'.
    It only searches for patterns near recently added points (from the list 'recent_points'). 

    If no pattern is found, returns None;
    otherwise returns the subset of 'edges' that forms a pattern (as a list).
    '''
    for p in recent_points:
        for patt in list_of_patterns:
            attaching_point = detect_pattern(p, patt)
            if attaching_point is not None:
                v = vec(attaching_point, p)
                translated_pattern = []
                for a, b in patt:
                    translated_pattern.append(
                        (translate(a, v), translate(b, v)))
                return translated_pattern
    return None


def initialize_patterns(initial_list_of_patterns):
    '''
    Given a list of patterns (each one being a list of edges),
    initializes list_of_patterns so that it contains all the list of edges corresponding
    to the images of those patterns under rotations and symmetries.
    '''
    global list_of_patterns

    list_of_patterns = []

    # Construct 'all_transfo', a list of 8 matrices corresponding to the possible symmetries
    rotation = np.array([np.array([0, -1]), np.array([1, 0])])
    flip = np.array([np.array([-1, 0]), np.array([0, 1])])
    all_transfo = [matrix_power(rotation, i) for i in range(
        4)] + [matrix_power(rotation, i).dot(flip) for i in range(4)]

    for pattern in initial_list_of_patterns:
        for mat in all_transfo:
            transformed_pattern = []

            for edge in pattern:
                a, b = edge
                new_a = tuple(mat.dot(np.array(a)))
                new_b = tuple(mat.dot(np.array(b)))
                transformed_pattern.append((new_a, new_b))

            list_of_patterns.append(transformed_pattern)


# -----------------------------------------------------------------------------------------------------------------
# EXPLORATION

def expand(gamma):
    '''
    Main recursive function. Implements Algorithm 2 (see the article).

    In the comments, we will use [i:] to denote the i-th line of Algorithm 2.
    '''

    global progress_counter

    added_edges, added_points, new_forbidden = add_path(gamma)  # Variables to store changes made in 'expand' to remove them when the branch is finished

    recent_points = set()
    for edge in added_edges:
        a, b = edge
        recent_points.update([a, b])

    new_known_satisfaction = []

    shortcut = None
    if to_prove.u is not None and to_prove.v is not None:
        shortcut = find_shortcut(
            to_prove.u, to_prove.v, to_prove.length_of_path)

    if shortcut is not None:  # Corresponds to line [2:] of Algorithm 2
        interface.notify_shortcut(edges, forbidden_edges, shortcut)
    else:
        created_pattern = pattern_created_by_recent_add(recent_points)
        if created_pattern is not None:  # [4:]
            interface.notify_pattern(edges, forbidden_edges, created_pattern)
        else:
            progress_counter += 1
            interface.notify_branch(edges, forbidden_edges, progress_counter)

            list_of_couples = []
            # We construct a list of pairs of points (p, q) [with |pq|<=sqrt(5)] which we will examine:
            # (Satisfaction) if there is already a path between p and q in 'edges' of length at most |pq|*DIL,
            #     the pair is good and there is nothing to do.
            #     We add the pair to 'known_satisfaction' so that we do not consider it again in the future (if not in 'known_satisfaction' already).
            # (Deduction) if there is only one possible path (not entirely in 'edges') between p and q of length at most |pq|*DIL,
            #     we deduce that it must be present. We store in 'a_unique_path' so that it can be added to
            #     'edges' in the next call to 'expand' (unless a contradiction is found in the meantime).
            # (Contradiction) if there cannot be any path between p and q of length at most |pq|*DIL,
            #     we found a contradiction ('edges' is not part of a locally optimal geometric graph).
            #     We end the exploration of this branch.
            # (Exploration) otherwise, we cannot conclude anything yet because there are several possibilities for a path between
            #     p and q of length at most DIL*|pq|, none of which is already in 'edges'

            for p in points:  # First point of the pair
                if is_close_to(p, recent_points, 3):    # We focus on the zones where changes have been made in the last step
                    for dx in [-2, -1, 0, 1, 2]:
                        for dy in [-2, -1, 0, 1, 2]:
                            if abs(dx) + abs(dy) in [1, 2, 3]:
                                q = translate(p, (dx, dy))  # The second point of the pair is such that 1 <= |pq| <= sqrt(5)
                                if is_close_to(q, recent_points, 2):    # We focus on the zones where changes have been made in the last step
                                    if (q, p) not in list_of_couples:  # To avoid duplicates
                                        list_of_couples.append((p, q))

            contradiction = False
            deduction = False
            a_unique_path = None  # The unique valid path in the case Deduction

            for (p, q) in list_of_couples:
                if (p, q) in known_satisfaction:  # Satisfaction (already known)
                    continue
                else:
                    if exists_good_path(p, q):  # Satisfaction (new)
                        known_satisfaction.update([(p, q), (q, p)])
                        new_known_satisfaction.extend([(p, q), (q, p)])
                        continue

                # We want to figure out whether there are 0, 1 or at least 2 paths between p and q.
                # The variable 'valid_paths' contains the list of valid paths between p and q (we limit the search to at most 2 paths).
                valid_paths = find_paths(p, q, 2)

                if len(valid_paths) == 0:  # Line [:6]: Contradiction
                    interface.notify_impossible_to_join(
                        edges, forbidden_edges, p, q)
                    contradiction = True
                    break  # We can stop immediately
                elif not deduction and len(valid_paths) == 1:
                    deduction = True
                    a_unique_path = valid_paths[0]

            if not contradiction:
                if deduction:  # Line [:8]: Deduction
                    interface.notify_unique_path(
                        edges, forbidden_edges, a_unique_path)
                    # Go deeper in the recursion to add the unique path [no choice is made]
                    expand(a_unique_path)
                else:  # Line [:12]
                    # Go deeper in the recursion by trying all possibilities for some pair (p, q) [several choices]
                    #
                    # The pair (p, q) is chosen as follows: it is the first pair (p, q) of 'ls_edges_to_consider'
                    # that is not known as good.

                    id_edge = 0
                    while id_edge < len(ls_edges_to_consider):
                        p, q = ls_edges_to_consider[id_edge]

                        if (p, q) not in known_satisfaction:
                            for path in the_five_short_paths(p, q):
                                if can_add_path(path):
                                    expand(path)
                            break

                        id_edge += 1

                    # Does not occur with the lists 'ls_edges_to_consider' that we provide
                    if id_edge == len(ls_edges_to_consider):
                        raise ValueError(
                            "The list 'ls_edges_to_consider' was not long enough: we could not finish the proof within this depth")

    # Undo the changes that were made at the start of this call to 'expand'
    remove_path(added_edges, added_points, new_forbidden)
    known_satisfaction.difference_update(new_known_satisfaction)


def prove(result_to_prove, communication_interface):
    global to_prove, edges, forbidden_edges, deg, points, known_satisfaction, ls_edges_to_consider, progress_counter, interface
    to_prove = result_to_prove
    interface = communication_interface

    edges = set()
    deg = {}
    points = set()

    forbidden_edges = set()
    known_satisfaction = set()

    progress_counter = 0

    initialize_patterns([path_to_list_of_edges(lemma.path_of_config)
                         for lemma in to_prove.known_lemmas])
    # now list_of_patterns is the full list of forbidden patterns, taking rotations and symmetries into account

    ls_edges_to_consider = to_prove.edges_to_consider

    interface.notify_start(edges, forbidden_edges, to_prove)
    expand(to_prove.path_of_config)
    interface.notify_end(to_prove)

    interface.notify_finished()

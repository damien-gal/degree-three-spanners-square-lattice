# A NOTE ON OPTIMAL DEGREE-THREE SPANNERS OF THE SQUARE LATTICE

## Dependencies

Our program runs in Python 3. It requires several (relatively standard) Python libraries:
- numpy;
- sympy (for symbolic computations);
- matplotlib and PyQt5 (for visualisation);
- docopt (to parse command line arguments).

You can use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install numpy
pip install sympy
pip install matplotlib
pip install PyQt5
pip install docopt
```

## Role of the different files

The files figure_2.py, proposition_2_1.py, lemma_2_4.py and lemma_3_8.py are used in the homonymous places in the article. To launch them, simply type
```bash
python3 figure_2.py
python3 proposition_2_1.py
python3 lemma_2_4.py
python3 lemma_3_8.py
```

The files proof.py, interface.py, launch.py and util.py are used in the proofs of Lemma 3.2 (for Algorithm 1) and Lemma 2.2 (for Algorithm 2). 
- The file proof.py contains the implementation of Algorithm 2 (and thus Algorithm 1 as well).
- The file interface.py allows the reader to visualize the execution of the Algorithms 1 and 2 in real time. Two options are available: a command-line (textual) and a matplotlib (graphical) interface.
- The file launch.py contains the input data for Algorithms 1 and 2. This is the only file that should be executed directly by the user.
- The file util.py contains a class to represent numbers in Z+Z*sqrt(2) and some helper functions for elementary geometry.

## Some details in the implementation of Algorithms 1 and 2

Both Algorithms 1 and 2 are implemented using the same 'expand' function in proof.py. This is possible since Algorithm 1 is a part of Algorithm 2 (where lines [2-3:] of Algorithm 2 do not apply and lines [4-5:] do not apply exactly). 

The goal of this section is to explain how Algorithm 2 (and thus also Algorithm 1) is implemented in proof.py.

Differences between the function 'Expand' in Algorithm 2 and the function 'expand' in proof.py.

- Instead of having 'S', 'u', 'v' and 'c' as an argument, the function 'expand' in proof.py has access to a number of global variables listed on the first line of the 'prove' function. The only argument of 'expand' is 'gamma', the path that was added most recently.
- In Algorithm 2, the variable 'S' represents the current set of edges of the configuration. In the proof.py file, the current set of edges is the global variable 'edges'.
- In Algorithm 2, the variable 'S' is updated (on lines [11:] and [16:]) before the new call to 'Expand'.
In proof.py, the new path 'gamma' is only added afterwards, at the beginning of 'expand'.

Here are some extra details:

- Some of the main variables used to store the global state are:
    - 'edges', the current set of edges;
    - 'deg', a Python dictionary which maps points of Z² to their current degree (deg[p] stores the the current number of edges from 'edges' which have p as an endpoint);
    - 'points', the set of all the endpoints of all the edges in the current configuration.
- Some segments of length 1 or sqrt(2) between two points of the grid are not compatible with the current configuration, in the sense that adding them to 'edges' creates a vertex of degree greater than 3 or an intersection. These segments are stored in the set 'forbidden_edges' and *are displayed in light orange in the graphical interface*.
- When we detect that a pair (p, q) in the case Satisfaction (see the article), we do not wish to consider it anymore in the further calls to 'expand'. We store all such pairs in the set 'known_satisfaction'.
- The following variables are defined when 'gamma' is added:
    - 'added_edges' is the set of edges of 'gamma' that are not already in 'edges'.
    - 'added_points' is the set of points of 'gamma' that are not already in 'points'.
    - 'new_forbidden' is set of edges that were added to 'forbidden_edges' due to the insertion of 'gamma'.
    - 'recent_points' is the set of points adjacent to an edge of 'added_edges'.
    When we try to detect some contradictions or deductions, we focus the region close to 'recent_points',
    since this is where they are more likely to appear.
- When the call to 'expand' is finished, the global variables are reverted to their previous state using 'added_edges', 'added_points' and 'new_forbidden'.
- As explained in Remark 3.7 in the article, the order in which the pairs (p, q) are considered is important for the efficiency of the algorithm (but not for its correctness). 
The order in which the pairs are considered is specified in the list 'ls_edges_to_consider', which is provided in the launch.py file.
The pair to be considered is the first pair in the list 'ls_edges_to_consider' which is not in 'known_satsifaction'.
- The user interface and the proof are strongly separated. The proof sends information to the interface through 'notify' functions, and never receives information from the interface.
- Throughout the proof, we need to manipulate lengths of paths consisting of segments of length 1 or sqrt(2). To do this, we use the class 'SquareRootNumber' in the file util.py. 
This allows to avoid all potential rounding errors due to floating-point computations.
We have not used sympy expressions to perform those symbolic computations because the resulting program would have been considerably slower.

## How to launch the main proof

The six results we prove are called h1, h2, p1, p2, p3 and p4 (for the terminology, see the article).
You can either prove one of those results or all of them.
We provide both a text-based and a GUI interface.
See some usage examples below.

```bash
python3 launch.py prove h1 --gui
python3 launch.py prove p2 --text
python3 launch.py prove all --text
```

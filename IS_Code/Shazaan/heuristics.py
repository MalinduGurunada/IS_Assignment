"""
heuristics.py
Heuristic functions for A* search in 3D space.

Admissibility requirement:
  A heuristic h(n) is admissible if h(n) <= h*(n) for all nodes n,
  where h*(n) is the true cost to the goal. An admissible heuristic
  guarantees that A* finds the optimal path.

Consistency (monotonicity) requirement:
  h(n) <= cost(n, n') + h(n') for every edge (n -> n').
  Consistency implies admissibility and ensures each node is only
  expanded once, giving A* O((V+E) log V) time complexity.
"""

import math
from typing import Tuple

Position = Tuple[float, float, float]


def euclidean_distance(a: Position, b: Position) -> float:
    """
    3D Euclidean (straight-line) distance between two points.

    Admissibility proof:
        In a graph where edge weights equal real 3D distances, the
        straight-line distance to the goal can never exceed the true
        path cost (which must travel along edges). Therefore h(n) <= h*(n).

    Time complexity: O(1)
    """
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def manhattan_distance(a: Position, b: Position) -> float:
    """
    3D Manhattan (taxicab) distance: sum of absolute axis differences.

    Note on admissibility:
        Manhattan distance is admissible ONLY when movement is restricted
        to axis-aligned steps of unit cost. In free 3D navigation it may
        OVERESTIMATE (inadmissible), which can cause A* to return
        sub-optimal paths. Use euclidean_distance for free-movement graphs.

    Time complexity: O(1)
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def octile_distance(a: Position, b: Position) -> float:
    """
    Octile distance — optimal heuristic for 8-directional 2D grid movement,
    extended here to 3D.

    Combines the diagonal shortcut cost with remaining axis travel:
        h = max_diff + (sqrt(2) - 1) * mid_diff + (sqrt(3) - sqrt(2)) * min_diff

    Admissibility: tighter than Euclidean for grid graphs; still admissible.

    Time complexity: O(1)
    """
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    dz = abs(a[2] - b[2])
    low, mid, high = sorted((dx, dy, dz))
    return (
        high
        + (math.sqrt(2.0) - 1.0) * mid
        + (math.sqrt(3.0) - math.sqrt(2.0)) * low
    )


def zero_heuristic(a: Position, b: Position) -> float:
    """
    Null heuristic — always returns 0.
    Makes A* behave identically to Dijkstra's algorithm (uniform-cost search).
    Admissible by definition; consistent by definition.
    """
    return 0.0

# Admissibility proofs and notes
# - Euclidean: admissible by triangle inequality; never overestimates straight-line distance.
# - Manhattan: admissible on axis-aligned, unit-cost grids only; may overestimate otherwise.
# - Octile: crafted for grid diagonals; tighter than Euclidean on grids, still admissible.

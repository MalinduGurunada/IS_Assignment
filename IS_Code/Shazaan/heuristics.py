"""
heuristics.py
Basic heuristic functions for A*.
"""

import math
from typing import Tuple

Position = Tuple[float, float, float]


def euclidean_distance(a: Position, b: Position) -> float:
    """Euclidean distance between two 3D points."""
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def manhattan_distance(a: Position, b: Position) -> float:
    """Manhattan (L1) distance between two 3D points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def octile_distance(a: Position, b: Position) -> float:
    """Octile-like heuristic (approx) for 3D."""
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    dz = abs(a[2] - b[2])
    low, mid, high = sorted((dx, dy, dz))
    return high + (math.sqrt(2) - 1) * mid + (math.sqrt(3) - math.sqrt(2)) * low


def zero_heuristic(a: Position, b: Position) -> float:
    """Zero heuristic (Dijkstra)."""
    return 0.0

"""
path_result.py
Data container for the output of a search algorithm.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class PathResult:
    """Holds the output of a single search execution."""

    path: List[int] = field(default_factory=list)
    total_cost: float = 0.0
    nodes_explored: int = 0
    elapsed_ms: float = 0.0

    def found(self) -> bool:
        """Return True if a path was found."""
        return len(self.path) > 0

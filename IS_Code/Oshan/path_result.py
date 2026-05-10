"""
path_result.py
Shared data container for search algorithm output.
(Identical to Shazaan's path_result.py — kept local so this module is self-contained.)
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class PathResult:
    path: List[int] = field(default_factory=list)
    total_cost: float = 0.0
    nodes_explored: int = 0
    elapsed_ms: float = 0.0

    def found(self) -> bool:
        return len(self.path) > 0

    def path_length(self) -> int:
        return len(self.path)

    def __repr__(self) -> str:
        if self.found():
            return (f"PathResult(length={self.path_length()}, cost={self.total_cost:.2f}, "
                    f"explored={self.nodes_explored}, time={self.elapsed_ms:.1f}ms)")
        return f"PathResult(NO PATH FOUND, explored={self.nodes_explored})"

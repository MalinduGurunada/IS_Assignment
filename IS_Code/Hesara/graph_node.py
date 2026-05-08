"""
graph_node.py
Defines the GraphNode data structure representing a single navigable point
extracted from the Unreal Engine NavMesh.
"""

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class GraphNode:
    """
    A single node in the navigation graph.

    Attributes:
        node_id  : Unique integer identifier.
        position : (x, y, z) world-space coordinates from the NavMesh.
        neighbors: List of node_ids directly connected to this node.
    """

    node_id: int
    position: Tuple[float, float, float]
    neighbors: List[int] = field(default_factory=list)

    def add_neighbor(self, neighbor_id: int) -> None:
        """Add a neighbor by node_id if not already present."""
        if neighbor_id not in self.neighbors:
            self.neighbors.append(neighbor_id)

    def remove_neighbor(self, neighbor_id: int) -> None:
        """Remove a neighbor by node_id if it exists."""
        if neighbor_id in self.neighbors:
            self.neighbors.remove(neighbor_id)

    def degree(self) -> int:
        """Return the number of direct neighbors (node degree)."""
        return len(self.neighbors)

    def __repr__(self) -> str:
        return f"GraphNode(id={self.node_id}, pos={self.position}, degree={len(self.neighbors)})"

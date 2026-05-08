"""
adjacency_list.py
Graph data structure backed by a dict of GraphNode objects.
Provides O(1) node lookup and supports weighted, bidirectional edges.
"""

from typing import Dict, List, Optional, Tuple
from graph_node import GraphNode


class Graph:
    """
    Navigation graph represented as an adjacency list.

    Internally stores {node_id: GraphNode} for O(1) lookup.
    Edge weights are stored separately as {(from_id, to_id): weight}.
    """

    def __init__(self) -> None:
        self._nodes: Dict[int, GraphNode] = {}
        self._weights: Dict[Tuple[int, int], float] = {}

    # ------------------------------------------------------------------
    # Node operations
    # ------------------------------------------------------------------

    def add_node(self, node: GraphNode) -> None:
        """Insert a GraphNode into the graph."""
        # TODO: store node in self._nodes keyed by node.node_id
        pass

    def get_node(self, node_id: int) -> Optional[GraphNode]:
        """Return the GraphNode for node_id, or None if not found."""
        # TODO: return self._nodes.get(node_id)
        pass

    def all_nodes(self) -> List[GraphNode]:
        """Return all nodes as a list."""
        # TODO: return list(self._nodes.values())
        pass

    # ------------------------------------------------------------------
    # Edge operations
    # ------------------------------------------------------------------

    def add_edge(self, from_id: int, to_id: int, weight: float = 1.0,
                 bidirectional: bool = True) -> None:
        """
        Add a weighted edge between two nodes.

        Args:
            from_id      : Source node id.
            to_id        : Destination node id.
            weight       : Edge cost (default 1.0).
            bidirectional: Also add the reverse edge (default True).
        """
        # TODO:
        # 1. Validate both nodes exist; raise KeyError if not
        # 2. Call from_node.add_neighbor(to_id) and store weight in self._weights
        # 3. If bidirectional, also add the reverse direction
        pass

    def remove_edge(self, from_id: int, to_id: int,
                    bidirectional: bool = True) -> None:
        """Remove an edge (and optionally its reverse)."""
        # TODO: call remove_neighbor on both nodes and delete from self._weights
        pass

    def has_edge(self, from_id: int, to_id: int) -> bool:
        """Return True if an edge exists from from_id to to_id."""
        # TODO: check self._weights for the key (from_id, to_id)
        pass

    def get_neighbors(self, node_id: int) -> List[Tuple[int, float]]:
        """
        Return list of (neighbor_id, edge_weight) for a given node.

        Returns:
            List of (neighbor_id, weight) tuples.
        """
        # TODO: look up node, iterate its neighbors, return with weights
        pass

    def edge_weight(self, from_id: int, to_id: int) -> float:
        """Return the weight of edge (from_id -> to_id)."""
        # TODO: return self._weights.get((from_id, to_id), float('inf'))
        pass

    # ------------------------------------------------------------------
    # Graph statistics
    # ------------------------------------------------------------------

    def node_count(self) -> int:
        """Return total number of nodes."""
        # TODO: return len(self._nodes)
        pass

    def edge_count(self) -> int:
        """Return total number of directed edges."""
        # TODO: return len(self._weights)
        pass

    def __repr__(self) -> str:
        return f"Graph(nodes={self.node_count()}, edges={self.edge_count()})"

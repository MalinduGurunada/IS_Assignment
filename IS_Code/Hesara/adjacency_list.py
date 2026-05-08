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
        self._nodes[node.node_id] = node

    def get_node(self, node_id: int) -> Optional[GraphNode]:
        """Return the GraphNode for node_id, or None if not found."""
        return self._nodes.get(node_id)

    def all_nodes(self) -> List[GraphNode]:
        """Return all nodes as a list."""
        return list(self._nodes.values())

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
        if from_id not in self._nodes:
            raise KeyError(f"Node {from_id} not in graph")
        if to_id not in self._nodes:
            raise KeyError(f"Node {to_id} not in graph")
        if from_id == to_id:
            raise ValueError(f"Self-loop not allowed: node {from_id}")
        self._nodes[from_id].add_neighbor(to_id)
        self._weights[(from_id, to_id)] = weight
        if bidirectional:
            self._nodes[to_id].add_neighbor(from_id)
            self._weights[(to_id, from_id)] = weight

    def remove_edge(self, from_id: int, to_id: int,
                    bidirectional: bool = True) -> None:
        """Remove an edge (and optionally its reverse)."""
        self._weights.pop((from_id, to_id), None)
        if from_id in self._nodes:
            self._nodes[from_id].remove_neighbor(to_id)
        if bidirectional:
            self._weights.pop((to_id, from_id), None)
            if to_id in self._nodes:
                self._nodes[to_id].remove_neighbor(from_id)

    def has_edge(self, from_id: int, to_id: int) -> bool:
        """Return True if an edge exists from from_id to to_id."""
        return (from_id, to_id) in self._weights

    def get_neighbors(self, node_id: int) -> List[Tuple[int, float]]:
        """
        Return list of (neighbor_id, edge_weight) for a given node.

        Returns:
            List of (neighbor_id, weight) tuples.
        """
        node = self._nodes.get(node_id)
        if not node:
            return []
        return [(nid, self._weights.get((node_id, nid), 1.0)) for nid in node.neighbors]

    def edge_weight(self, from_id: int, to_id: int) -> float:
        """Return the weight of edge (from_id -> to_id)."""
        return self._weights.get((from_id, to_id), float('inf'))

    # ------------------------------------------------------------------
    # Graph statistics
    # ------------------------------------------------------------------

    def node_count(self) -> int:
        """Return total number of nodes."""
        return len(self._nodes)

    def edge_count(self) -> int:
        """Return total number of directed edges."""
        return len(self._weights)

    def __repr__(self) -> str:
        return f"Graph(nodes={self.node_count()}, edges={self.edge_count()})"

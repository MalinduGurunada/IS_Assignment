"""
graph_extractor.py
Converts raw 3D NavMesh coordinate data into a Graph object.
NavMesh data is expected as a JSON file (see sample_navmesh.json).
"""

import json
import math
from typing import Any, Dict, List

from graph_node import GraphNode
from adjacency_list import Graph


class GraphExtractor:
    """
    Extracts a navigation graph from NavMesh coordinate data.

    The extractor reads a list of 3D positions and builds edges between
    nodes that are within a configurable proximity threshold, simulating
    the connections that the Unreal NavMesh would allow an agent to walk.

    Args:
        proximity_threshold: Maximum distance between two nodes to form an edge.
    """

    def __init__(self, proximity_threshold: float = 200.0) -> None:
        self.proximity_threshold = proximity_threshold

    def parse_navmesh_data(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Load NavMesh node data from a JSON file.

        Expected JSON format:
            [{"id": 0, "x": 100.0, "y": 200.0, "z": 0.0}, ...]

        Args:
            filepath: Path to the JSON file.

        Returns:
            List of node dicts with keys: id, x, y, z.
        """
        # TODO:
        # 1. Open and parse the JSON file
        # 2. Validate each entry has 'id', 'x', 'y', 'z' fields
        # 3. Return the list of dicts
        pass

    def build_graph(self, navmesh_data: List[Dict[str, Any]]) -> Graph:
        """
        Build a Graph from parsed NavMesh node data.

        For each pair of nodes, add a bidirectional edge if their
        Euclidean distance is within self.proximity_threshold.
        Edge weight equals the 3D Euclidean distance.

        Args:
            navmesh_data: List of node dicts from parse_navmesh_data().

        Returns:
            A populated Graph object.
        """
        # TODO:
        # 1. Create an empty Graph
        # 2. Add a GraphNode for each entry in navmesh_data
        # 3. For every pair (i, j), compute 3D distance
        # 4. If distance <= self.proximity_threshold, add_edge with that weight
        # 5. Return the graph
        pass

    def extract_from_file(self, filepath: str) -> Graph:
        """Convenience: parse file and build graph in one call."""
        data = self.parse_navmesh_data(filepath)
        return self.build_graph(data)

    @staticmethod
    def _euclidean_distance(a: Dict[str, Any], b: Dict[str, Any]) -> float:
        """Compute 3D Euclidean distance between two node dicts."""
        # TODO: return sqrt((a.x-b.x)^2 + (a.y-b.y)^2 + (a.z-b.z)^2)
        pass

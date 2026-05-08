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
        if proximity_threshold <= 0:
            raise ValueError("proximity_threshold must be positive")
        self.proximity_threshold = proximity_threshold

    def set_threshold(self, proximity_threshold: float) -> None:
        """
        Update the proximity threshold used when building edges.

        Allows the same extractor instance to be reused with different
        thresholds without creating a new object.

        Args:
            proximity_threshold: New positive maximum edge distance.

        Raises:
            ValueError: If proximity_threshold is not positive.
        """
        if proximity_threshold <= 0:
            raise ValueError("proximity_threshold must be positive")
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
        with open(filepath, 'r') as f:
            data = json.load(f)
        for entry in data:
            for key in ('id', 'x', 'y', 'z'):
                if key not in entry:
                    raise ValueError(f"NavMesh entry missing field '{key}': {entry}")
        return data

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
        graph = Graph()
        for entry in navmesh_data:
            node = GraphNode(
                node_id=entry['id'],
                position=(entry['x'], entry['y'], entry['z'])
            )
            graph.add_node(node)
        nodes = list(navmesh_data)
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                dist = self._euclidean_distance(nodes[i], nodes[j])
                if dist <= self.proximity_threshold:
                    graph.add_edge(nodes[i]['id'], nodes[j]['id'], weight=dist,
                                   bidirectional=True)
        return graph

    def extract_from_file(self, filepath: str) -> Graph:
        """Convenience: parse file and build graph in one call."""
        data = self.parse_navmesh_data(filepath)
        return self.build_graph(data)

    @staticmethod
    def _euclidean_distance(a: Dict[str, Any], b: Dict[str, Any]) -> float:
        """Compute 3D Euclidean distance between two node dicts."""
        return math.sqrt(
            (a['x'] - b['x']) ** 2 +
            (a['y'] - b['y']) ** 2 +
            (a['z'] - b['z']) ** 2
        )

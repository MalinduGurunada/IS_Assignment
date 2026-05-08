"""
graph_utils.py
Utility functions for working with Graph objects:
  - distance calculation
  - graph validation
  - JSON import/export
"""

import json
import math
from typing import Any, Dict, List, Tuple

from adjacency_list import Graph
from graph_node import GraphNode


def euclidean_distance(a: Tuple[float, float, float],
                       b: Tuple[float, float, float]) -> float:
    """
    Compute 3D Euclidean distance between two (x, y, z) positions.

    Time complexity: O(1)
    """
    return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))


def validate_graph(graph: Graph) -> List[str]:
    """
    Check graph integrity and return a list of warning strings.

    Checks performed:
      - Nodes with no neighbors (isolated nodes)
      - Edges referencing non-existent node ids
      - Negative edge weights

    Returns:
        List of warning messages. Empty list means the graph is valid.
    """
    warnings = []
    node_ids = {node.node_id for node in graph.all_nodes()}

    for node in graph.all_nodes():
        if node.degree() == 0:
            warnings.append(f"Node {node.node_id} is isolated (no neighbors)")
        for neighbor_id in node.neighbors:
            if neighbor_id not in node_ids:
                warnings.append(
                    f"Node {node.node_id} references non-existent neighbor {neighbor_id}"
                )
            weight = graph.edge_weight(node.node_id, neighbor_id)
            if weight < 0:
                warnings.append(
                    f"Negative weight {weight} on edge ({node.node_id} -> {neighbor_id})"
                )

    return warnings


def graph_stats(graph: Graph) -> Dict[str, Any]:
    """
    Return a summary dict of graph statistics.

    Returns keys: node_count, edge_count, avg_degree, isolated_nodes.
    """
    nodes = graph.all_nodes()
    node_count = len(nodes)
    edge_count = graph.edge_count()
    total_degree = sum(node.degree() for node in nodes)
    avg_degree = total_degree / node_count if node_count > 0 else 0.0
    isolated = sum(1 for node in nodes if node.degree() == 0)

    return {
        "node_count": node_count,
        "edge_count": edge_count,
        "avg_degree": round(avg_degree, 4),
        "isolated_nodes": isolated,
    }


def export_graph_to_json(graph: Graph, filepath: str) -> None:
    """
    Serialize the graph to a JSON file.

    Output format:
        {
          "nodes": [{"id": 0, "x": 1.0, "y": 2.0, "z": 0.0}, ...],
          "edges": [{"from": 0, "to": 1, "weight": 141.4}, ...]
        }
    """
    nodes = []
    for node in graph.all_nodes():
        x, y, z = node.position
        nodes.append({"id": node.node_id, "x": x, "y": y, "z": z})

    edges = []
    for node in graph.all_nodes():
        for neighbor_id, weight in graph.get_neighbors(node.node_id):
            edges.append({"from": node.node_id, "to": neighbor_id, "weight": round(weight, 4)})

    with open(filepath, 'w') as f:
        json.dump({"nodes": nodes, "edges": edges}, f, indent=2)


def import_graph_from_json(filepath: str) -> Graph:
    """
    Deserialize a graph from a JSON file previously created by export_graph_to_json().

    Returns:
        A populated Graph object.
    """
    with open(filepath, 'r') as f:
        data = json.load(f)

    graph = Graph()
    for node_data in data['nodes']:
        node = GraphNode(
            node_id=node_data['id'],
            position=(node_data['x'], node_data['y'], node_data['z'])
        )
        graph.add_node(node)

    for edge in data['edges']:
        if not graph.has_edge(edge['from'], edge['to']):
            graph.add_edge(edge['from'], edge['to'], weight=edge['weight'],
                           bidirectional=False)

    return graph

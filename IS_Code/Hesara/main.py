"""
main.py  —  Hesara | Role 1: Custom Graph Formulation
Demonstrates building a Graph from hardcoded sample nodes and printing
the adjacency list. JSON loading added in a later commit.

Run:
    python main.py
"""

import os
from graph_node import GraphNode
from adjacency_list import Graph
from graph_utils import euclidean_distance, graph_stats, validate_graph, export_graph_to_json


def build_sample_graph() -> Graph:
    """Build a small hardcoded graph for early development testing."""
    graph = Graph()
    nodes = [
        GraphNode(0, (0.0,   0.0,   0.0)),
        GraphNode(1, (100.0, 0.0,   0.0)),
        GraphNode(2, (200.0, 0.0,   0.0)),
        GraphNode(3, (100.0, 100.0, 0.0)),
        GraphNode(4, (0.0,   100.0, 0.0)),
    ]
    for node in nodes:
        graph.add_node(node)

    # Connect nearby nodes manually
    graph.add_edge(0, 1, weight=100.0)
    graph.add_edge(1, 2, weight=100.0)
    graph.add_edge(1, 3, weight=100.0)
    graph.add_edge(3, 4, weight=100.0)
    graph.add_edge(0, 4, weight=100.0)
    return graph


def main():
    print("=" * 55)
    print("  IS Assignment — Graph Formulation Demo (Hesara)")
    print("=" * 55)

    print("\n[1] Building hardcoded sample graph...")
    graph = build_sample_graph()

    print("\n[2] Adjacency list:")
    for node in graph.all_nodes():
        neighbors = graph.get_neighbors(node.node_id)
        neighbor_str = ", ".join(f"Node {nid} (w={w:.1f})" for nid, w in neighbors)
        print(f"    Node {node.node_id} @ {node.position}  ->  [{neighbor_str}]")

    print(f"\n[3] Graph: {graph.node_count()} nodes, {graph.edge_count()} directed edges")


if __name__ == "__main__":
    main()

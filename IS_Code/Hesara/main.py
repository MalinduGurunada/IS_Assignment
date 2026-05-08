"""
main.py  —  Hesara | Role 1: Custom Graph Formulation
Demonstrates loading a NavMesh JSON file, building a Graph, and
printing the resulting adjacency list with edge weights.

Run:
    python main.py
"""

import os
from graph_extractor import GraphExtractor
from graph_utils import graph_stats, validate_graph, export_graph_to_json


def main():
    sample_file = os.path.join(os.path.dirname(__file__), "sample_navmesh.json")

    print("=" * 55)
    print("  IS Assignment — Graph Formulation Demo (Hesara)")
    print("=" * 55)

    extractor = GraphExtractor(proximity_threshold=150.0)

    print(f"\n[1] Loading NavMesh data from: {sample_file}")
    data = extractor.parse_navmesh_data(sample_file)
    print(f"    Loaded {len(data)} nodes.")

    print("\n[2] Building graph (proximity threshold = 150 units)...")
    graph = extractor.build_graph(data)

    print("\n[3] Adjacency list:")
    for node in graph.all_nodes():
        neighbors = graph.get_neighbors(node.node_id)
        neighbor_str = ", ".join(
            f"Node {nid} (w={w:.1f})" for nid, w in neighbors
        )
        print(f"    Node {node.node_id} @ {node.position}  ->  [{neighbor_str}]")

    print("\n[4] Graph statistics:")
    stats = graph_stats(graph)
    for key, value in stats.items():
        print(f"    {key}: {value}")

    print("\n[5] Validating graph...")
    warnings = validate_graph(graph)
    if warnings:
        for w in warnings:
            print(f"    WARNING: {w}")
    else:
        print("    Graph is valid — no issues found.")

    out_path = os.path.join(os.path.dirname(__file__), "output_graph.json")
    print(f"\n[6] Exporting graph to {out_path} ...")
    export_graph_to_json(graph, out_path)
    print("    Done.")


if __name__ == "__main__":
    main()

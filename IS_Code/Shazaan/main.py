"""
main.py  —  Shazaan | Role 3: A* Search & Heuristic Design
Demonstrates building a sample graph, running A* with different heuristics,
and printing the resulting path and cost.

Run:
    python main.py
"""

import json
import os

from astar import AStarSearch
from heuristics import euclidean_distance, zero_heuristic
from path_result import PathResult


class _SimpleGraph:
    def __init__(self):
        self._nodes = {}
        self._edges = {}

    def add_node(self, nid, pos):
        self._nodes[nid] = pos

    def add_edge(self, f, t, w):
        self._edges[(f, t)] = w
        self._edges[(t, f)] = w

    def get_node(self, nid):
        class N:
            def __init__(s, i, p): s.node_id = i; s.position = p
        return N(nid, self._nodes[nid])

    def get_neighbors(self, nid):
        return [(t, w) for (f, t), w in self._edges.items() if f == nid]


def load_graph_from_json(filepath):
    with open(filepath) as f:
        data = json.load(f)
    g = _SimpleGraph()
    for n in data["nodes"]:
        g.add_node(n["id"], (n["x"], n["y"], n["z"]))
    for e in data["edges"]:
        g.add_edge(e["from"], e["to"], e["weight"])
    return g


def print_result(label: str, result: PathResult) -> None:
    print(f"\n  [{label}]")
    if result.found():
        print(f"    Path       : {' -> '.join(str(n) for n in result.path)}")
        print(f"    Total cost : {result.total_cost:.2f}")
        print(f"    Explored   : {result.nodes_explored} nodes")
        print(f"    Time       : {result.elapsed_ms:.2f} ms")
    else:
        print("    No path found.")


def main():
    sample_file = os.path.join(os.path.dirname(__file__), "sample_graph.json")

    print("=" * 55)
    print("  IS Assignment — A* Search Demo (Shazaan)")
    print("=" * 55)

    print(f"\n[1] Loading graph from: {sample_file}")
    graph = load_graph_from_json(sample_file)

    start, goal = 0, 4
    print(f"\n[2] Running A* from Node {start} to Node {goal}")

    astar_euclidean = AStarSearch(graph, heuristic=euclidean_distance)
    result_euclidean = astar_euclidean.search(start, goal)
    print_result("A* with Euclidean heuristic", result_euclidean)

    astar_dijkstra = AStarSearch(graph, heuristic=zero_heuristic)
    result_dijkstra = astar_dijkstra.search(start, goal)
    print_result("A* with zero heuristic (Dijkstra)", result_dijkstra)

    print("\n[3] Comparing results:")
    print(f"    Both found same cost? {abs(result_euclidean.total_cost - result_dijkstra.total_cost) < 1e-6}")
    print(f"    Euclidean explored {result_euclidean.nodes_explored} nodes, "
          f"Dijkstra explored {result_dijkstra.nodes_explored} nodes")


if __name__ == "__main__":
    main()

"""
main.py  —  Oshan | Role 4: Secondary Search & Debug Visualizer
Demonstrates BFS and UCS on the same graph, compares their results,
and shows the toggleable ASCII debug visualizer.

Run:
    python main.py
"""

import json
import os

from bfs import BreadthFirstSearch
from ucs import UniformCostSearch
from debug_visualizer import DebugVisualizer
from path_result import PathResult


# ---------------------------------------------------------------------------
# Inline graph builder (self-contained demo)
# ---------------------------------------------------------------------------

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

    def edge_weight(self, f, t):
        return self._edges.get((f, t), float('inf'))


def load_graph(filepath):
    with open(filepath) as f:
        data = json.load(f)
    g = _SimpleGraph()
    for n in data["nodes"]:
        g.add_node(n["id"], (n["x"], n["y"], n["z"]))
    for e in data["edges"]:
        g.add_edge(e["from"], e["to"], e["weight"])
    return g


def print_result(label, result):
    print(f"\n  [{label}]")
    if result.found():
        print(f"    Path       : {' -> '.join(str(n) for n in result.path)}")
        print(f"    Cost       : {result.total_cost:.2f}")
        print(f"    Hop count  : {result.path_length() - 1}")
        print(f"    Explored   : {result.nodes_explored} nodes")
        print(f"    Time       : {result.elapsed_ms:.2f} ms")
    else:
        print("    No path found.")


def main():
    sample_file = os.path.join(os.path.dirname(__file__), "sample_graph.json")

    print("=" * 60)
    print("  IS Assignment — Secondary Search & Debug Visualizer (Oshan)")
    print("=" * 60)

    print(f"\n[1] Loading graph from: {sample_file}")
    graph = load_graph(sample_file)

    start, goal = 0, 4

    # -----------------------------------------------------------------------
    # Run BFS
    # -----------------------------------------------------------------------
    print(f"\n[2] Running BFS from Node {start} to Node {goal}")
    bfs = BreadthFirstSearch(graph)
    bfs_result = bfs.search(start, goal)
    print_result("BFS (fewest hops)", bfs_result)

    # -----------------------------------------------------------------------
    # Run UCS
    # -----------------------------------------------------------------------
    print(f"\n[3] Running UCS from Node {start} to Node {goal}")
    ucs = UniformCostSearch(graph)
    ucs_result = ucs.search(start, goal)
    print_result("UCS (minimum cost)", ucs_result)

    # -----------------------------------------------------------------------
    # Compare
    # -----------------------------------------------------------------------
    print("\n[4] Comparison:")
    print(f"    BFS path cost : {bfs_result.total_cost:.2f}  (not minimised by BFS)")
    print(f"    UCS path cost : {ucs_result.total_cost:.2f}  (optimal)")
    print(f"    Same path?    : {bfs_result.path == ucs_result.path}")

    # -----------------------------------------------------------------------
    # Debug Visualizer
    # -----------------------------------------------------------------------
    print("\n[5] Toggling debug visualizer ON...")
    viz = DebugVisualizer(grid_size=10, cell_size=100.0)
    viz.toggle_debug()

    viz.draw_path(ucs_result.path, graph, label="UCS Optimal Path")

    print("\n  Printing ASCII grid (UCS path):")
    viz.print_grid(
        path=ucs_result.path,
        visited=set(range(graph._nodes.__len__())),
        frontier=[],
        graph=graph,
        start_id=start,
        goal_id=goal,
    )

    viz.compare_searches({
        "BFS": bfs_result,
        "UCS": ucs_result,
    })

    print("\n[6] Toggling debug visualizer OFF...")
    viz.toggle_debug()
    viz.draw_path(ucs_result.path, graph, label="Should not print")
    print("    (nothing printed above = visualizer correctly disabled)")


if __name__ == "__main__":
    main()

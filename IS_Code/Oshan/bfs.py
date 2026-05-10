"""
bfs.py
Breadth-First Search for unweighted shortest-path (fewest hops) navigation.

BFS guarantees the shortest path in terms of NUMBER OF EDGES on an
unweighted graph.  It does NOT minimise total edge weight.

Time complexity : O(V + E)
Space complexity: O(V)
"""

import time
from typing import Dict, List, Optional

from search_frontier import FIFOFrontier
from path_result import PathResult


class BreadthFirstSearch:
    """
    BFS pathfinding on a navigation Graph.

    Args:
        graph: The navigation Graph (Hesara's adjacency_list.Graph).
    """

    def __init__(self, graph) -> None:
        self.graph = graph

    def search(self, start_id: int, goal_id: int) -> PathResult:
        """
        Run BFS from start_id to goal_id.

        Returns:
            PathResult with the fewest-hop path (or empty if unreachable).
        """
        t_start = time.time()

        if start_id == goal_id:
            return PathResult(path=[start_id], total_cost=0.0, nodes_explored=0,
                              elapsed_ms=(time.time() - t_start) * 1000)

        # TODO:
        # 1. Create FIFOFrontier; enqueue start_id
        # 2. Create visited set; mark start_id visited
        # 3. Create came_from dict
        # 4. While frontier not empty:
        #      a. dequeue current
        #      b. nodes_explored += 1
        #      c. For each (neighbor_id, _) in graph.get_neighbors(current):
        #           - If neighbor not visited:
        #               * mark visited
        #               * came_from[neighbor] = current
        #               * If neighbor == goal_id -> reconstruct_path and return
        #               * enqueue neighbor
        # 5. Return empty PathResult (no path)
        pass

    def reconstruct_path(self, came_from: Dict[int, int],
                         start_id: int, goal_id: int) -> List[int]:
        """Trace came_from backwards from goal_id to start_id."""
        # TODO: walk back from goal_id to start_id and reverse
        pass

    def _path_cost(self, path: List[int]) -> float:
        """Compute total edge-weight cost of a path (for PathResult)."""
        # TODO: sum graph.edge_weight(path[i], path[i+1]) for each consecutive pair
        pass

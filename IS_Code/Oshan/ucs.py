"""
ucs.py
Uniform-Cost Search (UCS / Dijkstra) — finds the minimum-cost path
by always expanding the lowest-cost node first.

UCS guarantees the optimal (minimum total edge weight) path,
unlike BFS which only minimises hop count.

Relationship to A*:
    UCS == A* with heuristic h(n) = 0 for all n.

Time complexity : O((V + E) log V)  with a binary heap
Space complexity: O(V)
"""

import time
from typing import Dict, List

from search_frontier import PriorityFrontier
from path_result import PathResult


class UniformCostSearch:
    """
    UCS pathfinding on a navigation Graph.

    Args:
        graph: The navigation Graph (Hesara's adjacency_list.Graph).
    """

    def __init__(self, graph) -> None:
        self.graph = graph

    def search(self, start_id: int, goal_id: int) -> PathResult:
        """
        Run UCS from start_id to goal_id.

        Returns:
            PathResult with the minimum-cost path (or empty if unreachable).
        """
        t_start = time.time()

        if start_id == goal_id:
            return PathResult(path=[start_id], total_cost=0.0, nodes_explored=0,
                              elapsed_ms=(time.time() - t_start) * 1000)

        # TODO:
        # 1. Create PriorityFrontier; push start_id with priority 0
        # 2. Create cost_so_far dict: {start_id: 0}
        # 3. Create came_from dict
        # 4. Create explored set
        # 5. While frontier not empty:
        #      a. Pop (cost, current)
        #      b. If current in explored: continue
        #      c. Add current to explored; nodes_explored += 1
        #      d. If current == goal_id -> reconstruct_path and return
        #      e. For each (neighbor_id, edge_weight) in graph.get_neighbors(current):
        #           new_cost = cost + edge_weight
        #           If neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
        #               * Update cost_so_far[neighbor]
        #               * Update came_from[neighbor] = current
        #               * Push neighbor with priority new_cost
        # 6. Return empty PathResult
        pass

    def reconstruct_path(self, came_from: Dict[int, int],
                         start_id: int, goal_id: int) -> List[int]:
        """Trace came_from backwards from goal_id to start_id."""
        # TODO: walk back from goal_id and reverse
        pass

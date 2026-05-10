"""
astar.py
Simple A* search implementation using the MinHeap and heuristics.
"""

# Time complexity : O((V + E) log V)  with a binary heap
# Space complexity: O(V)

import time
from typing import Callable, Dict, List

from priority_queue import MinHeap
from heuristics import euclidean_distance
from path_result import PathResult


class AStarSearch:
    def __init__(self, graph, heuristic: Callable = euclidean_distance) -> None:
        self.graph = graph
        self.heuristic = heuristic

    def search(self, start_id: int, goal_id: int, heuristic: Callable = None) -> PathResult:
        t_start = time.time()

        if start_id == goal_id:
            return PathResult(path=[start_id], total_cost=0.0, nodes_explored=0)

        # Open set stores (f_score, node_id) and is initialised with the start
        open_set = MinHeap()
        came_from: Dict[int, int] = {}
        g_scores: Dict[int, float] = {start_id: 0.0}
        closed_set = set()

        start_pos = self.graph.get_node(start_id).position
        goal_pos = self.graph.get_node(goal_id).position
        # allow per-call heuristic override
        h = heuristic if heuristic is not None else self.heuristic
        # initialise open set with start node's heuristic
        open_set.push(start_id, h(start_pos, goal_pos))

        nodes_explored = 0

        while not open_set.is_empty():
            current_f, current = open_set.pop()
            if current in closed_set:
                continue

            nodes_explored += 1

            if current == goal_id:
                path = self.reconstruct_path(came_from, start_id, goal_id)
                return PathResult(path=path, total_cost=g_scores[current], nodes_explored=nodes_explored)

            # add current node to closed set to avoid re-expansion
            closed_set.add(current)

            for neighbor_id, weight in self.graph.get_neighbors(current):
                # neighbour expansion and g-score update
                tentative_g = g_scores[current] + weight
                if tentative_g >= g_scores.get(neighbor_id, float("inf")):
                    continue

                came_from[neighbor_id] = current
                g_scores[neighbor_id] = tentative_g

                # if a neighbor was previously closed, re-open it
                if neighbor_id in closed_set:
                    closed_set.remove(neighbor_id)

                neighbor_pos = self.graph.get_node(neighbor_id).position
                f_score = tentative_g + h(neighbor_pos, goal_pos)
                open_set.push(neighbor_id, f_score)

        return PathResult(nodes_explored=nodes_explored)

    def reconstruct_path(self, came_from: Dict[int, int], start_id: int, goal_id: int) -> List[int]:
        path = [goal_id]
        current = goal_id
        # walk backwards through the came_from map to build full path
        while current != start_id:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

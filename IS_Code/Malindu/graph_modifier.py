"""
graph_modifier.py
Applies dynamic changes to the navigation graph in response to environment
events — severing or restoring edges when obstacles appear or disappear.
"""

from typing import Dict, List, Set, Tuple

# Import the Graph from Hesara's module (shared across the project)
# from IS_Code.Hesara.adjacency_list import Graph
# For standalone testing use a local stub or mock.


class GraphModifier:
    """
    Modifies a Graph's edge set based on environment events.

    Maintains a registry of currently severed edges so they can be
    restored when an obstacle is removed.

    Args:
        graph: The shared navigation Graph object.
    """

    def __init__(self, graph) -> None:
        self.graph = graph
        # Stores {(from_id, to_id): weight} for edges that have been severed
        self._severed_edges: Dict[Tuple[int, int], float] = {}

    def sever_edge_at_position(self, position: Tuple[float, float, float],
                                radius: float = 150.0) -> List[Tuple[int, int]]:
        """
        Find and sever all graph edges that pass through a given world position.

        Strategy: sever edges whose midpoint falls within `radius` units
        of the given position.

        Args:
            position: (x, y, z) world-space position of the obstacle.
            radius  : Search radius around the position.

        Returns:
            List of (from_id, to_id) tuples that were severed.
        """
        # TODO:
        # 1. Iterate all edges in self.graph
        # 2. Compute the midpoint of each edge
        # 3. If midpoint distance to `position` <= radius, call sever_edge()
        # 4. Collect and return the severed edge pairs
        pass

    def sever_edge(self, from_id: int, to_id: int) -> bool:
        """
        Sever a specific edge and remember its weight for later restoration.

        Args:
            from_id: Source node id.
            to_id  : Destination node id.

        Returns:
            True if the edge existed and was severed, False otherwise.
        """
        # TODO:
        # 1. Check graph.has_edge(from_id, to_id)
        # 2. Save weight to self._severed_edges[(from_id, to_id)]
        # 3. Call graph.remove_edge(from_id, to_id, bidirectional=True)
        # 4. Return True; return False if edge didn't exist
        pass

    def restore_edge(self, from_id: int, to_id: int) -> bool:
        """
        Restore a previously severed edge with its original weight.

        Returns:
            True if the edge was restored, False if it was never severed.
        """
        # TODO:
        # 1. Check self._severed_edges for (from_id, to_id)
        # 2. Call graph.add_edge with the stored weight
        # 3. Remove from self._severed_edges
        # 4. Return True/False accordingly
        pass

    def restore_edges_at_position(self, position: Tuple[float, float, float],
                                   radius: float = 150.0) -> List[Tuple[int, int]]:
        """Restore all severed edges whose midpoint is within radius of position."""
        # TODO: mirror sever_edge_at_position but call restore_edge instead
        pass

    def get_severed_edges(self) -> List[Tuple[int, int]]:
        """Return a list of all currently severed (from_id, to_id) pairs."""
        # TODO: return list(self._severed_edges.keys())
        pass

    def is_severed(self, from_id: int, to_id: int) -> bool:
        """Return True if this edge is currently severed."""
        # TODO: return (from_id, to_id) in self._severed_edges
        pass

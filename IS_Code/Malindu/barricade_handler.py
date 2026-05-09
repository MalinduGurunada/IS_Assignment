"""
barricade_handler.py
Listens for environment events (barricade placements/removals) and
coordinates with GraphModifier and RecalculationTrigger to update
the navigation graph in real time.
"""

import logging
from typing import Callable, List, Optional

from event_types import EnvironmentEvent, EventType
from graph_modifier import GraphModifier

logger = logging.getLogger(__name__)


class BarricadeHandler:
    """
    Intercepts environment events and applies graph modifications.

    Args:
        graph_modifier         : The GraphModifier that severs/restores edges.
        on_graph_changed       : Callback invoked after every graph modification.
                                 Typically RecalculationTrigger.trigger.
        obstacle_radius        : World-unit radius used to find affected edges.
    """

    def __init__(
        self,
        graph_modifier: GraphModifier,
        on_graph_changed: Optional[Callable] = None,
        obstacle_radius: float = 150.0,
    ) -> None:
        self.graph_modifier = graph_modifier
        self.on_graph_changed = on_graph_changed
        self.obstacle_radius = obstacle_radius
        self._event_log: List[EnvironmentEvent] = []

    def handle_event(self, event: EnvironmentEvent) -> None:
        """
        Route an EnvironmentEvent to the correct handler method.

        Args:
            event: The incoming environment change event.
        """
        # TODO:
        # 1. Append event to self._event_log
        # 2. If event.is_blocking()  -> call on_barricade_placed(event)
        # 3. If event.is_clearing()  -> call on_barricade_removed(event)
        # 4. Log a warning for unrecognised event types
        pass

    def on_barricade_placed(self, event: EnvironmentEvent) -> None:
        """
        Handle a blocking event: sever affected edges and trigger recalculation.

        Args:
            event: The BARRICADE_PLACED (or equivalent blocking) event.
        """
        # TODO:
        # 1. Call self.graph_modifier.sever_edge_at_position(event.position, self.obstacle_radius)
        # 2. Log how many edges were severed
        # 3. If any edges were severed AND self.on_graph_changed is set, call it
        pass

    def on_barricade_removed(self, event: EnvironmentEvent) -> None:
        """
        Handle a clearing event: restore affected edges and trigger recalculation.

        Args:
            event: The BARRICADE_REMOVED (or equivalent clearing) event.
        """
        # TODO:
        # 1. Call self.graph_modifier.restore_edges_at_position(event.position, self.obstacle_radius)
        # 2. Log how many edges were restored
        # 3. If any edges were restored AND self.on_graph_changed is set, call it
        pass

    def get_event_log(self) -> List[EnvironmentEvent]:
        """Return the full list of events handled so far."""
        return list(self._event_log)

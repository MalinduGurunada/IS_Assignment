"""
event_types.py
Defines the event taxonomy and data structures for environment change events
(e.g., a player dropping a barricade that blocks a navigation path).
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple


class EventType(Enum):
    """Types of environment change events that affect the navigation graph."""
    BARRICADE_PLACED   = auto()   # A barricade was placed, blocking a path
    BARRICADE_REMOVED  = auto()   # A barricade was removed, reopening a path
    DOOR_CLOSED        = auto()   # A door was closed, severing an edge
    DOOR_OPENED        = auto()   # A door was opened, restoring an edge
    OBSTACLE_SPAWNED   = auto()   # Generic obstacle appeared
    OBSTACLE_DESTROYED = auto()   # Generic obstacle removed


@dataclass
class EnvironmentEvent:
    """
    Represents a single environment change event.

    Attributes:
        event_type : The type of event (see EventType).
        position   : (x, y, z) world-space position where the event occurred.
        actor_id   : Optional identifier of the UE actor that triggered the event.
        timestamp  : Simulation timestamp in seconds (for debounce logic).
    """

    event_type: EventType
    position: Tuple[float, float, float]
    actor_id: str = ""
    timestamp: float = 0.0

    def is_blocking(self) -> bool:
        """Return True if this event adds an obstacle (severs an edge)."""
        # TODO: return True for BARRICADE_PLACED, DOOR_CLOSED, OBSTACLE_SPAWNED
        pass

    def is_clearing(self) -> bool:
        """Return True if this event removes an obstacle (restores an edge)."""
        # TODO: return True for BARRICADE_REMOVED, DOOR_OPENED, OBSTACLE_DESTROYED
        pass

    def __repr__(self) -> str:
        return f"EnvironmentEvent({self.event_type.name} @ {self.position}, t={self.timestamp:.2f}s)"

"""
search_frontier.py
Frontier data structures for BFS (FIFO queue) and UCS (min-heap).
Tracks the full history of explored frontiers for the debug visualizer.
"""

import heapq
from collections import deque
from typing import Any, List, Optional, Tuple


class FIFOFrontier:
    """
    First-In First-Out queue used by BFS.

    Wraps collections.deque for O(1) enqueue and dequeue.
    """

    def __init__(self) -> None:
        self._queue: deque = deque()
        self.history: List[Any] = []   # all nodes ever added (for visualizer)

    def enqueue(self, item: Any) -> None:
        """Add item to the back of the queue."""
        # TODO: append to self._queue and self.history
        pass

    def dequeue(self) -> Any:
        """Remove and return the front item. Raises IndexError if empty."""
        # TODO: popleft from self._queue
        pass

    def is_empty(self) -> bool:
        # TODO: return len(self._queue) == 0
        pass

    def __len__(self) -> int:
        return len(self._queue)

    def __contains__(self, item: Any) -> bool:
        return item in self._queue


class PriorityFrontier:
    """
    Min-heap priority queue used by UCS.
    Each entry is (cost, node_id).
    """

    _REMOVED = "__REMOVED__"

    def __init__(self) -> None:
        self._heap: list = []
        self._entry_map: dict = {}
        self._counter: int = 0
        self.history: List[Any] = []

    def push(self, item: Any, priority: float) -> None:
        """Insert item (or update priority if already present)."""
        # TODO: lazy-deletion push, same pattern as Shazaan's MinHeap
        pass

    def pop(self) -> Tuple[float, Any]:
        """Remove and return (priority, item) with lowest priority."""
        # TODO: heappop, skip REMOVED entries
        pass

    def contains(self, item: Any) -> bool:
        # TODO: return item in self._entry_map
        pass

    def is_empty(self) -> bool:
        # TODO: return len(self._entry_map) == 0
        pass

    def __len__(self) -> int:
        return len(self._entry_map)

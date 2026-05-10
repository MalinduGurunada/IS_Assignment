"""
priority_queue.py
A min-heap priority queue used by the A* search algorithm to efficiently
retrieve the node with the lowest f-score at each step.

Time complexities:
  push()           : O(log n)
  pop()            : O(log n)
  update_priority(): O(n) naive; can be improved to O(log n) with a heap map
"""

import heapq
from typing import Any, List, Optional, Tuple


class MinHeap:
    """
    Min-heap priority queue where each entry is (priority, item).

    Supports lazy deletion via a 'removed' sentinel to allow priority updates.
    """

    _REMOVED = "__REMOVED__"

    def __init__(self) -> None:
        self._heap: List[Tuple[float, Any]] = []
        self._entry_map: dict = {}   # item -> [priority, item] entry in heap
        self._counter: int = 0       # tie-breaker to keep heap stable

    def push(self, item: Any, priority: float) -> None:
        """
        Insert item with given priority.
        If item already exists, update its priority instead.

        Args:
            item    : Hashable object (e.g., node_id).
            priority: Lower value = higher priority.
        """
        if item in self._entry_map:
            self._entry_map[item][2] = self._REMOVED

        entry = [priority, self._counter, item]
        self._entry_map[item] = entry
        heapq.heappush(self._heap, entry)
        self._counter += 1

    def pop(self) -> Tuple[float, Any]:
        """
        Remove and return (priority, item) with the lowest priority value.

        Raises:
            IndexError: if the queue is empty.
        """
        while self._heap:
            priority, _, item = heapq.heappop(self._heap)
            if item == self._REMOVED:
                continue

            del self._entry_map[item]
            return priority, item

        raise IndexError("pop from an empty MinHeap")

    def update_priority(self, item: Any, new_priority: float) -> None:
        """
        Update the priority of an existing item.
        Equivalent to a push (lazy deletion handles the old entry).
        """
        self.push(item, new_priority)

    def contains(self, item: Any) -> bool:
        """Return True if item is in the queue (and not removed)."""
        return item in self._entry_map

    def is_empty(self) -> bool:
        """Return True if no valid entries remain."""
        return len(self._entry_map) == 0

    def peek(self) -> Optional[Tuple[float, Any]]:
        """Return (priority, item) of the minimum element without removing it."""
        for priority, _, item in self._heap:
            if item != self._REMOVED:
                return priority, item
        return None

    def __len__(self) -> int:
        return len(self._entry_map)

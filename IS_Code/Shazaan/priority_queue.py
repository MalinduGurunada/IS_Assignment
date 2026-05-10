"""
priority_queue.py
Simple min-priority queue used by A* to pick the lowest f-score.
"""

from typing import Any, List, Tuple


class MinHeap:
    """Naive min-priority queue based on a Python list."""

    def __init__(self) -> None:
        self._items: List[Tuple[float, Any]] = []

    def push(self, item: Any, priority: float) -> None:
        """Insert item with given priority."""
        self._items.append((priority, item))

    def pop(self) -> Tuple[float, Any]:
        """Remove and return (priority, item) with the lowest priority value."""
        if not self._items:
            raise IndexError("pop from an empty MinHeap")

        min_idx = 0
        min_priority = self._items[0][0]
        for idx, (priority, _) in enumerate(self._items[1:], start=1):
            if priority < min_priority:
                min_priority = priority
                min_idx = idx

        return self._items.pop(min_idx)

    def update_priority(self, item: Any, new_priority: float) -> None:
        """Update priority of an existing item (or insert if missing)."""
        for idx, (_, existing_item) in enumerate(self._items):
            if existing_item == item:
                self._items[idx] = (new_priority, item)
                return

        self.push(item, new_priority)

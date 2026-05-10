"""
test_dynamic.py
Unit tests for event_types, barricade_handler, graph_modifier, and
recalculation_trigger.
Run with: python -m pytest test_dynamic.py -v
"""

import time
import unittest
from unittest.mock import MagicMock, patch

from event_types import EventType, EnvironmentEvent
from graph_modifier import GraphModifier
from barricade_handler import BarricadeHandler
from recalculation_trigger import RecalculationTrigger


class TestEventTypes(unittest.TestCase):

    def test_event_type_enum_values(self):
        self.assertIn(EventType.BARRICADE_PLACED, EventType)
        self.assertIn(EventType.BARRICADE_REMOVED, EventType)

    def test_is_blocking(self):
        event = EnvironmentEvent(EventType.BARRICADE_PLACED, (0.0, 0.0, 0.0))
        self.assertTrue(event.is_blocking())

    def test_is_clearing(self):
        event = EnvironmentEvent(EventType.BARRICADE_REMOVED, (0.0, 0.0, 0.0))
        self.assertTrue(event.is_clearing())

    def test_blocking_not_clearing(self):
        event = EnvironmentEvent(EventType.BARRICADE_PLACED, (0.0, 0.0, 0.0))
        self.assertFalse(event.is_clearing())


class TestGraphModifier(unittest.TestCase):

    def _make_mock_graph(self, edges=None):
        """Create a mock graph with controllable has_edge/edge_weight behaviour."""
        mock = MagicMock()
        edges = edges or {}
        mock.has_edge.side_effect = lambda f, t: (f, t) in edges
        mock.edge_weight.side_effect = lambda f, t: edges.get((f, t), 1.0)
        return mock

    def test_sever_edge_returns_true_when_exists(self):
        graph = self._make_mock_graph(edges={(0, 1): 100.0, (1, 0): 100.0})
        modifier = GraphModifier(graph)
        result = modifier.sever_edge(0, 1)
        self.assertTrue(result)

    def test_sever_edge_returns_false_when_not_exists(self):
        graph = self._make_mock_graph(edges={})
        modifier = GraphModifier(graph)
        result = modifier.sever_edge(0, 1)
        self.assertFalse(result)

    def test_severed_edge_tracked(self):
        graph = self._make_mock_graph(edges={(0, 1): 50.0, (1, 0): 50.0})
        modifier = GraphModifier(graph)
        modifier.sever_edge(0, 1)
        self.assertIn((0, 1), modifier.get_severed_edges())

    def test_restore_edge(self):
        graph = self._make_mock_graph(edges={(0, 1): 50.0, (1, 0): 50.0})
        modifier = GraphModifier(graph)
        modifier.sever_edge(0, 1)
        result = modifier.restore_edge(0, 1)
        self.assertTrue(result)
        self.assertNotIn((0, 1), modifier.get_severed_edges())

    def test_restore_edge_not_severed_returns_false(self):
        graph = self._make_mock_graph()
        modifier = GraphModifier(graph)
        result = modifier.restore_edge(0, 1)
        self.assertFalse(result)

    def test_is_severed(self):
        graph = self._make_mock_graph(edges={(0, 1): 10.0, (1, 0): 10.0})
        modifier = GraphModifier(graph)
        modifier.sever_edge(0, 1)
        self.assertTrue(modifier.is_severed(0, 1))
        modifier.restore_edge(0, 1)
        self.assertFalse(modifier.is_severed(0, 1))


class TestBarricadeHandler(unittest.TestCase):

    def test_handle_blocking_event_calls_sever(self):
        modifier = MagicMock()
        modifier.sever_edge_at_position.return_value = [(0, 1)]
        handler = BarricadeHandler(modifier)
        event = EnvironmentEvent(EventType.BARRICADE_PLACED, (50.0, 50.0, 0.0))
        handler.handle_event(event)
        modifier.sever_edge_at_position.assert_called_once()

    def test_handle_clearing_event_calls_restore(self):
        modifier = MagicMock()
        modifier.restore_edges_at_position.return_value = [(0, 1)]
        handler = BarricadeHandler(modifier)
        event = EnvironmentEvent(EventType.BARRICADE_REMOVED, (50.0, 50.0, 0.0))
        handler.handle_event(event)
        modifier.restore_edges_at_position.assert_called_once()

    def test_on_graph_changed_called_after_sever(self):
        modifier = MagicMock()
        modifier.sever_edge_at_position.return_value = [(0, 1)]
        callback = MagicMock()
        handler = BarricadeHandler(modifier, on_graph_changed=callback)
        event = EnvironmentEvent(EventType.BARRICADE_PLACED, (50.0, 50.0, 0.0))
        handler.handle_event(event)
        callback.assert_called_once()

    def test_event_log_populated(self):
        modifier = MagicMock()
        modifier.sever_edge_at_position.return_value = []
        handler = BarricadeHandler(modifier)
        event = EnvironmentEvent(EventType.BARRICADE_PLACED, (0.0, 0.0, 0.0))
        handler.handle_event(event)
        self.assertEqual(len(handler.get_event_log()), 1)


class TestRecalculationTrigger(unittest.TestCase):

    def test_trigger_calls_recalculate_fn(self):
        fn = MagicMock()
        trigger = RecalculationTrigger(recalculate_fn=fn, debounce_seconds=0.0)
        graph = MagicMock()
        graph._weights = {(0, 1): 1.0}
        trigger.trigger(graph)
        fn.assert_called_once()

    def test_debounce_suppresses_second_call(self):
        fn = MagicMock()
        trigger = RecalculationTrigger(recalculate_fn=fn, debounce_seconds=10.0)
        graph = MagicMock()
        graph._weights = {(0, 1): 1.0}
        trigger.trigger(graph)
        trigger.trigger(graph)
        fn.assert_called_once()

    def test_no_change_suppresses_call(self):
        fn = MagicMock()
        trigger = RecalculationTrigger(recalculate_fn=fn, debounce_seconds=0.0)
        graph = MagicMock()
        graph._weights = {(0, 1): 1.0}
        trigger.trigger(graph)
        trigger.trigger(graph)  # same graph hash, should be suppressed
        self.assertEqual(fn.call_count, 1)

    def test_recalculation_count_increments(self):
        trigger = RecalculationTrigger(debounce_seconds=0.0)
        graph = MagicMock()
        graph._weights = {(0, 1): 1.0}
        trigger.trigger(graph)
        self.assertEqual(trigger.recalculation_count, 1)


if __name__ == "__main__":
    unittest.main()

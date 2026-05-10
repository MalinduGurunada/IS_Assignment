"""
test_secondary.py
Unit tests for FIFOFrontier, PriorityFrontier, BFS, UCS, and DebugVisualizer.
Run with: python -m pytest test_secondary.py -v
"""

import unittest
from unittest.mock import patch
from io import StringIO

from search_frontier import FIFOFrontier, PriorityFrontier
from bfs import BreadthFirstSearch
from ucs import UniformCostSearch
from debug_visualizer import DebugVisualizer
from path_result import PathResult


# ---------------------------------------------------------------------------
# Minimal graph stub
# ---------------------------------------------------------------------------

class _StubGraph:
    def __init__(self):
        self._nodes = {}
        self._edges = {}

    def add_node(self, nid, pos):
        self._nodes[nid] = pos

    def add_edge(self, f, t, w):
        self._edges[(f, t)] = w
        self._edges[(t, f)] = w

    def get_node(self, nid):
        class N:
            def __init__(s, i, p): s.node_id = i; s.position = p
        return N(nid, self._nodes[nid])

    def get_neighbors(self, nid):
        return [(t, w) for (f, t), w in self._edges.items() if f == nid]

    def edge_weight(self, f, t):
        return self._edges.get((f, t), float('inf'))


def _weighted_graph():
    """
    0 --1-- 1 --1-- 2
    |               |
    4               3
    |               |
    5 ------2------ 4
    """
    g = _StubGraph()
    positions = {0: (0,0,0), 1: (1,0,0), 2: (2,0,0), 3: (2,1,0), 4: (1,2,0), 5: (0,1,0)}
    for nid, pos in positions.items():
        g.add_node(nid, tuple(float(x) for x in pos))
    g.add_edge(0, 1, 1.0)
    g.add_edge(1, 2, 1.0)
    g.add_edge(2, 3, 1.0)
    g.add_edge(3, 4, 1.0)
    g.add_edge(0, 5, 4.0)
    g.add_edge(5, 4, 2.0)
    return g


def _disconnected_graph():
    g = _StubGraph()
    g.add_node(0, (0.0, 0.0, 0.0))
    g.add_node(1, (1.0, 0.0, 0.0))
    g.add_node(2, (10.0, 0.0, 0.0))
    g.add_edge(0, 1, 1.0)
    return g


# ---------------------------------------------------------------------------
# FIFOFrontier tests
# ---------------------------------------------------------------------------

class TestFIFOFrontier(unittest.TestCase):

    def test_enqueue_dequeue_order(self):
        f = FIFOFrontier()
        f.enqueue(1)
        f.enqueue(2)
        f.enqueue(3)
        self.assertEqual(f.dequeue(), 1)
        self.assertEqual(f.dequeue(), 2)

    def test_is_empty(self):
        f = FIFOFrontier()
        self.assertTrue(f.is_empty())
        f.enqueue(1)
        self.assertFalse(f.is_empty())

    def test_history_tracks_all_added(self):
        f = FIFOFrontier()
        f.enqueue(1)
        f.enqueue(2)
        f.dequeue()
        self.assertIn(1, f.history)
        self.assertIn(2, f.history)


# ---------------------------------------------------------------------------
# PriorityFrontier tests
# ---------------------------------------------------------------------------

class TestPriorityFrontier(unittest.TestCase):

    def test_pop_order(self):
        f = PriorityFrontier()
        f.push("b", 2.0)
        f.push("a", 1.0)
        _, item = f.pop()
        self.assertEqual(item, "a")

    def test_update_lower_priority(self):
        f = PriorityFrontier()
        f.push("x", 10.0)
        f.push("x", 1.0)
        priority, item = f.pop()
        self.assertEqual(item, "x")
        self.assertAlmostEqual(priority, 1.0)


# ---------------------------------------------------------------------------
# BFS tests
# ---------------------------------------------------------------------------

class TestBFS(unittest.TestCase):

    def test_finds_path(self):
        g = _weighted_graph()
        bfs = BreadthFirstSearch(g)
        result = bfs.search(0, 4)
        self.assertTrue(result.found())
        self.assertEqual(result.path[0], 0)
        self.assertEqual(result.path[-1], 4)

    def test_fewest_hops(self):
        g = _weighted_graph()
        bfs = BreadthFirstSearch(g)
        result = bfs.search(0, 4)
        # Shortest hop path: 0->1->2->3->4 = 4 hops (5 nodes)
        self.assertEqual(result.path_length(), 5)

    def test_no_path(self):
        g = _disconnected_graph()
        bfs = BreadthFirstSearch(g)
        result = bfs.search(0, 2)
        self.assertFalse(result.found())

    def test_start_equals_goal(self):
        g = _weighted_graph()
        bfs = BreadthFirstSearch(g)
        result = bfs.search(2, 2)
        self.assertTrue(result.found())
        self.assertAlmostEqual(result.total_cost, 0.0)


# ---------------------------------------------------------------------------
# UCS tests
# ---------------------------------------------------------------------------

class TestUCS(unittest.TestCase):

    def test_finds_path(self):
        g = _weighted_graph()
        ucs = UniformCostSearch(g)
        result = ucs.search(0, 4)
        self.assertTrue(result.found())

    def test_minimum_cost(self):
        g = _weighted_graph()
        ucs = UniformCostSearch(g)
        result = ucs.search(0, 4)
        # Cheapest: 0->1->2->3->4 cost=4; alternate 0->5->4 cost=6
        self.assertAlmostEqual(result.total_cost, 4.0)

    def test_bfs_and_ucs_agree_on_unweighted_graph(self):
        g = _StubGraph()
        for i in range(4):
            g.add_node(i, (float(i), 0.0, 0.0))
        for i in range(3):
            g.add_edge(i, i+1, 1.0)
        bfs_result = BreadthFirstSearch(g).search(0, 3)
        ucs_result = UniformCostSearch(g).search(0, 3)
        self.assertEqual(bfs_result.path, ucs_result.path)

    def test_no_path(self):
        g = _disconnected_graph()
        ucs = UniformCostSearch(g)
        result = ucs.search(0, 2)
        self.assertFalse(result.found())


# ---------------------------------------------------------------------------
# DebugVisualizer tests
# ---------------------------------------------------------------------------

class TestDebugVisualizer(unittest.TestCase):

    def test_toggle_enables(self):
        viz = DebugVisualizer()
        self.assertFalse(viz.is_enabled())
        viz.toggle_debug()
        self.assertTrue(viz.is_enabled())

    def test_toggle_disables(self):
        viz = DebugVisualizer()
        viz.toggle_debug()
        viz.toggle_debug()
        self.assertFalse(viz.is_enabled())

    def test_draw_frontier_suppressed_when_disabled(self):
        viz = DebugVisualizer()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            viz.draw_frontier([1, 2, 3], None)
            self.assertEqual(mock_stdout.getvalue(), "")

    def test_draw_path_produces_output_when_enabled(self):
        g = _StubGraph()
        g.add_node(0, (0.0, 0.0, 0.0))
        g.add_node(1, (1.0, 0.0, 0.0))
        viz = DebugVisualizer()
        viz.toggle_debug()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            viz.draw_path([0, 1], g)
            self.assertGreater(len(mock_stdout.getvalue()), 0)


if __name__ == "__main__":
    unittest.main()

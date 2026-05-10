import math
import unittest
from priority_queue import MinHeap
from heuristics import euclidean_distance, manhattan_distance, octile_distance, zero_heuristic
from astar import AStarSearch
from path_result import PathResult


class _StubGraph:
    def __init__(self):
        self._nodes = {}
        self._edges = {}

    def add_node(self, node_id, position):
        self._nodes[node_id] = position

    def add_edge(self, f, t, w):
        self._edges[(f, t)] = w
        self._edges[(t, f)] = w

    def get_node(self, node_id):
        class N:
            def __init__(s, nid, pos): s.node_id = nid; s.position = pos
        return N(node_id, self._nodes[node_id])

    def get_neighbors(self, node_id):
        return [(t, w) for (f, t), w in self._edges.items() if f == node_id]


def _linear_graph():
    g = _StubGraph()
    for i in range(4):
        g.add_node(i, (float(i * 10), 0.0, 0.0))
    for i in range(3):
        g.add_edge(i, i + 1, 10.0)
    return g


def _disconnected_graph():
    g = _StubGraph()
    g.add_node(0, (0.0,  0.0, 0.0))
    g.add_node(1, (10.0, 0.0, 0.0))
    g.add_node(2, (50.0, 0.0, 0.0))
    g.add_edge(0, 1, 10.0)
    return g


class TestMinHeap(unittest.TestCase):

    def test_push_and_pop_order(self):
        heap = MinHeap()
        heap.push("b", 2.0)
        heap.push("a", 1.0)
        heap.push("c", 3.0)
        self.assertEqual(heap.pop()[1], "a")
        self.assertEqual(heap.pop()[1], "b")

    def test_update_priority(self):
        heap = MinHeap()
        heap.push("a", 10.0)
        heap.push("b", 5.0)
        heap.update_priority("a", 1.0)
        self.assertEqual(heap.pop()[1], "a")

    def test_is_empty(self):
        heap = MinHeap()
        self.assertTrue(heap.is_empty())
        heap.push("x", 1.0)
        self.assertFalse(heap.is_empty())

    def test_contains(self):
        heap = MinHeap()
        heap.push("x", 1.0)
        self.assertTrue(heap.contains("x"))
        heap.pop()
        self.assertFalse(heap.contains("x"))

    def test_pop_empty_raises(self):
        heap = MinHeap()
        with self.assertRaises(IndexError):
            heap.pop()


class TestHeuristics(unittest.TestCase):

    def test_euclidean_3d(self):
        self.assertAlmostEqual(euclidean_distance((0,0,0), (3,4,0)), 5.0)

    def test_euclidean_zero(self):
        self.assertAlmostEqual(euclidean_distance((1,2,3), (1,2,3)), 0.0)

    def test_manhattan_3d(self):
        self.assertAlmostEqual(manhattan_distance((0,0,0), (1,2,3)), 6.0)

    def test_zero_heuristic(self):
        self.assertEqual(zero_heuristic((0,0,0), (100,100,100)), 0.0)

    def test_octile_3d(self):
        self.assertAlmostEqual(octile_distance((0,0,0), (1,1,1)), math.sqrt(3.0))

    def test_euclidean_admissible(self):
        h = euclidean_distance((0,0,0), (10,0,0))
        self.assertLessEqual(h, 10.0 + 1e-9)


class TestAStarSearch(unittest.TestCase):

    def test_finds_path_on_linear_graph(self):
        g = _linear_graph()
        astar = AStarSearch(g, heuristic=zero_heuristic)
        result = astar.search(0, 3)
        self.assertTrue(result.found())
        self.assertEqual(result.path[0], 0)
        self.assertEqual(result.path[-1], 3)

    def test_optimal_cost_on_linear_graph(self):
        g = _linear_graph()
        astar = AStarSearch(g, heuristic=zero_heuristic)
        result = astar.search(0, 3)
        self.assertAlmostEqual(result.total_cost, 30.0)

    def test_no_path_returns_empty(self):
        g = _disconnected_graph()
        astar = AStarSearch(g, heuristic=zero_heuristic)
        result = astar.search(0, 2)
        self.assertFalse(result.found())

    def test_start_equals_goal(self):
        g = _linear_graph()
        astar = AStarSearch(g, heuristic=zero_heuristic)
        result = astar.search(2, 2)
        self.assertTrue(result.found())
        self.assertAlmostEqual(result.total_cost, 0.0)

    def test_nodes_explored_is_positive(self):
        g = _linear_graph()
        astar = AStarSearch(g, heuristic=zero_heuristic)
        result = astar.search(0, 3)
        self.assertGreater(result.nodes_explored, 0)


if __name__ == "__main__":
    unittest.main()

"""
test_graph.py
Unit tests for GraphNode, Graph, GraphExtractor, and graph_utils.
Run with: python -m pytest test_graph.py -v
"""

import json
import os
import tempfile
import unittest

from graph_node import GraphNode
from adjacency_list import Graph
from graph_extractor import GraphExtractor
from graph_utils import euclidean_distance, validate_graph, export_graph_to_json, import_graph_from_json


class TestGraphNode(unittest.TestCase):

    def test_node_creation(self):
        node = GraphNode(node_id=1, position=(0.0, 0.0, 0.0))
        self.assertEqual(node.node_id, 1)
        self.assertEqual(node.position, (0.0, 0.0, 0.0))
        self.assertEqual(node.neighbors, [])

    def test_node_creation_3d_position(self):
        node = GraphNode(node_id=5, position=(10.5, -3.2, 100.0))
        self.assertEqual(node.position, (10.5, -3.2, 100.0))

    def test_node_default_no_neighbors(self):
        node = GraphNode(node_id=0, position=(0.0, 0.0, 0.0))
        self.assertEqual(len(node.neighbors), 0)
        self.assertEqual(node.degree(), 0)

    def test_add_neighbor(self):
        node = GraphNode(node_id=1, position=(0.0, 0.0, 0.0))
        node.add_neighbor(2)
        self.assertIn(2, node.neighbors)

    def test_add_multiple_neighbors(self):
        node = GraphNode(node_id=1, position=(0.0, 0.0, 0.0))
        node.add_neighbor(2)
        node.add_neighbor(3)
        node.add_neighbor(4)
        self.assertEqual(sorted(node.neighbors), [2, 3, 4])

    def test_add_neighbor_no_duplicates(self):
        node = GraphNode(node_id=1, position=(0.0, 0.0, 0.0))
        node.add_neighbor(2)
        node.add_neighbor(2)
        self.assertEqual(node.neighbors.count(2), 1)

    def test_remove_neighbor(self):
        node = GraphNode(node_id=1, position=(0.0, 0.0, 0.0))
        node.add_neighbor(2)
        node.remove_neighbor(2)
        self.assertNotIn(2, node.neighbors)

    def test_remove_nonexistent_neighbor_no_error(self):
        node = GraphNode(node_id=1, position=(0.0, 0.0, 0.0))
        node.remove_neighbor(99)  # should not raise

    def test_degree(self):
        node = GraphNode(node_id=1, position=(0.0, 0.0, 0.0))
        node.add_neighbor(2)
        node.add_neighbor(3)
        self.assertEqual(node.degree(), 2)

    def test_degree_after_remove(self):
        node = GraphNode(node_id=1, position=(0.0, 0.0, 0.0))
        node.add_neighbor(2)
        node.add_neighbor(3)
        node.remove_neighbor(2)
        self.assertEqual(node.degree(), 1)


class TestGraph(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()
        self.graph.add_node(GraphNode(0, (0.0, 0.0, 0.0)))
        self.graph.add_node(GraphNode(1, (100.0, 0.0, 0.0)))
        self.graph.add_node(GraphNode(2, (100.0, 100.0, 0.0)))

    def test_add_and_get_node(self):
        node = self.graph.get_node(0)
        self.assertIsNotNone(node)
        self.assertEqual(node.node_id, 0)

    def test_add_edge_bidirectional(self):
        self.graph.add_edge(0, 1, weight=100.0)
        self.assertTrue(self.graph.has_edge(0, 1))
        self.assertTrue(self.graph.has_edge(1, 0))

    def test_add_edge_unidirectional(self):
        self.graph.add_edge(0, 1, weight=100.0, bidirectional=False)
        self.assertTrue(self.graph.has_edge(0, 1))
        self.assertFalse(self.graph.has_edge(1, 0))

    def test_remove_edge(self):
        self.graph.add_edge(0, 1, weight=100.0)
        self.graph.remove_edge(0, 1)
        self.assertFalse(self.graph.has_edge(0, 1))

    def test_get_neighbors(self):
        self.graph.add_edge(0, 1, weight=100.0)
        self.graph.add_edge(0, 2, weight=141.0)
        neighbors = self.graph.get_neighbors(0)
        neighbor_ids = [n[0] for n in neighbors]
        self.assertIn(1, neighbor_ids)
        self.assertIn(2, neighbor_ids)

    def test_edge_weight(self):
        self.graph.add_edge(0, 1, weight=99.5)
        self.assertAlmostEqual(self.graph.edge_weight(0, 1), 99.5)

    def test_node_count(self):
        self.assertEqual(self.graph.node_count(), 3)

    def test_edge_count(self):
        self.graph.add_edge(0, 1)
        self.assertEqual(self.graph.edge_count(), 2)  # bidirectional = 2 directed edges


class TestGraphExtractor(unittest.TestCase):

    SAMPLE_NAVMESH = [
        {"id": 0, "x": 0.0,   "y": 0.0,   "z": 0.0},
        {"id": 1, "x": 100.0, "y": 0.0,   "z": 0.0},
        {"id": 2, "x": 500.0, "y": 500.0, "z": 0.0},
    ]

    def test_invalid_proximity_raises(self):
        with self.assertRaises(ValueError):
            GraphExtractor(proximity_threshold=0)

    def test_invalid_proximity_negative_raises(self):
        with self.assertRaises(ValueError):
            GraphExtractor(proximity_threshold=-10.0)

    def test_build_graph_creates_correct_node_count(self):
        extractor = GraphExtractor(proximity_threshold=200.0)
        graph = extractor.build_graph(self.SAMPLE_NAVMESH)
        self.assertEqual(graph.node_count(), 3)

    def test_build_graph_close_nodes_connected(self):
        extractor = GraphExtractor(proximity_threshold=200.0)
        graph = extractor.build_graph(self.SAMPLE_NAVMESH)
        self.assertTrue(graph.has_edge(0, 1))
        self.assertTrue(graph.has_edge(1, 0))  # bidirectional

    def test_build_graph_distant_nodes_not_connected(self):
        extractor = GraphExtractor(proximity_threshold=200.0)
        graph = extractor.build_graph(self.SAMPLE_NAVMESH)
        self.assertFalse(graph.has_edge(0, 2))
        self.assertFalse(graph.has_edge(2, 0))

    def test_build_graph_edge_weight_is_distance(self):
        extractor = GraphExtractor(proximity_threshold=200.0)
        graph = extractor.build_graph(self.SAMPLE_NAVMESH)
        self.assertAlmostEqual(graph.edge_weight(0, 1), 100.0)

    def test_build_graph_all_within_threshold_connected(self):
        close_nodes = [
            {"id": 0, "x": 0.0,  "y": 0.0, "z": 0.0},
            {"id": 1, "x": 50.0, "y": 0.0, "z": 0.0},
            {"id": 2, "x": 0.0,  "y": 50.0, "z": 0.0},
        ]
        extractor = GraphExtractor(proximity_threshold=100.0)
        graph = extractor.build_graph(close_nodes)
        self.assertTrue(graph.has_edge(0, 1))
        self.assertTrue(graph.has_edge(0, 2))
        self.assertTrue(graph.has_edge(1, 2))

    def test_parse_navmesh_data_from_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.SAMPLE_NAVMESH, f)
            tmppath = f.name
        try:
            extractor = GraphExtractor()
            data = extractor.parse_navmesh_data(tmppath)
            self.assertEqual(len(data), 3)
        finally:
            os.unlink(tmppath)

    def test_parse_navmesh_missing_field_raises(self):
        bad_data = [{"id": 0, "x": 0.0, "y": 0.0}]  # missing 'z'
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(bad_data, f)
            tmppath = f.name
        try:
            extractor = GraphExtractor()
            with self.assertRaises(ValueError):
                extractor.parse_navmesh_data(tmppath)
        finally:
            os.unlink(tmppath)


class TestGraphUtils(unittest.TestCase):

    def test_euclidean_distance_3d(self):
        dist = euclidean_distance((0.0, 0.0, 0.0), (3.0, 4.0, 0.0))
        self.assertAlmostEqual(dist, 5.0)

    def test_export_creates_valid_json(self):
        graph = Graph()
        graph.add_node(GraphNode(0, (0.0, 0.0, 0.0)))
        graph.add_node(GraphNode(1, (10.0, 20.0, 5.0)))
        graph.add_edge(0, 1, weight=22.9)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            tmppath = f.name
        try:
            export_graph_to_json(graph, tmppath)
            with open(tmppath) as fh:
                data = json.load(fh)
            node_ids = {n['id'] for n in data['nodes']}
            self.assertEqual(node_ids, {0, 1})
            edge_pairs = {(e['from'], e['to']) for e in data['edges']}
            self.assertIn((0, 1), edge_pairs)
            self.assertIn((1, 0), edge_pairs)
        finally:
            os.unlink(tmppath)

    def test_export_import_roundtrip(self):
        graph = Graph()
        graph.add_node(GraphNode(0, (0.0, 0.0, 0.0)))
        graph.add_node(GraphNode(1, (10.0, 0.0, 0.0)))
        graph.add_edge(0, 1, weight=10.0)

        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            tmppath = f.name
        try:
            export_graph_to_json(graph, tmppath)
            loaded = import_graph_from_json(tmppath)
            self.assertEqual(loaded.node_count(), 2)
            self.assertTrue(loaded.has_edge(0, 1))
        finally:
            os.unlink(tmppath)

    def test_validate_graph_detects_isolated_node(self):
        graph = Graph()
        graph.add_node(GraphNode(0, (0.0, 0.0, 0.0)))
        graph.add_node(GraphNode(1, (10.0, 0.0, 0.0)))
        # No edges — both nodes are isolated
        warnings = validate_graph(graph)
        self.assertGreater(len(warnings), 0)


class TestGraphStats(unittest.TestCase):
    """Tests for graph_stats utility."""

    def _make_connected_graph(self):
        from graph_utils import graph_stats
        g = Graph()
        for i in range(4):
            g.add_node(GraphNode(i, (float(i * 100), 0.0, 0.0)))
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        return g

    def test_stats_node_count(self):
        from graph_utils import graph_stats
        g = self._make_connected_graph()
        stats = graph_stats(g)
        self.assertEqual(stats['node_count'], 4)

    def test_stats_edge_count(self):
        from graph_utils import graph_stats
        g = self._make_connected_graph()
        stats = graph_stats(g)
        self.assertEqual(stats['edge_count'], 6)  # 3 bidirectional = 6 directed

    def test_stats_isolated_zero_when_all_connected(self):
        from graph_utils import graph_stats
        g = self._make_connected_graph()
        stats = graph_stats(g)
        self.assertEqual(stats['isolated_nodes'], 0)

    def test_stats_isolated_counts_lone_node(self):
        from graph_utils import graph_stats
        g = Graph()
        g.add_node(GraphNode(0, (0.0, 0.0, 0.0)))
        g.add_node(GraphNode(1, (100.0, 0.0, 0.0)))
        g.add_node(GraphNode(2, (200.0, 0.0, 0.0)))
        g.add_edge(0, 1)
        stats = graph_stats(g)
        self.assertEqual(stats['isolated_nodes'], 1)


class TestExtractFromFile(unittest.TestCase):
    """Integration test: extract_from_file reads JSON and builds graph."""

    def test_extract_from_sample_navmesh(self):
        import os
        here = os.path.dirname(__file__)
        fixture = os.path.join(here, 'sample_navmesh.json')
        if not os.path.exists(fixture):
            self.skipTest("sample_navmesh.json not present")
        extractor = GraphExtractor(proximity_threshold=200.0)
        graph = extractor.extract_from_file(fixture)
        self.assertGreater(graph.node_count(), 0)
        self.assertGreater(graph.edge_count(), 0)

    def test_set_threshold_updates_correctly(self):
        extractor = GraphExtractor(proximity_threshold=100.0)
        extractor.set_threshold(500.0)
        self.assertEqual(extractor.proximity_threshold, 500.0)

    def test_set_threshold_invalid_raises(self):
        extractor = GraphExtractor()
        with self.assertRaises(ValueError):
            extractor.set_threshold(-5.0)


if __name__ == "__main__":
    unittest.main()

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

    def test_add_neighbor(self):
        node = GraphNode(node_id=1, position=(0.0, 0.0, 0.0))
        node.add_neighbor(2)
        self.assertIn(2, node.neighbors)

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

    def test_degree(self):
        node = GraphNode(node_id=1, position=(0.0, 0.0, 0.0))
        node.add_neighbor(2)
        node.add_neighbor(3)
        self.assertEqual(node.degree(), 2)


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

    def test_build_graph_close_nodes_connected(self):
        extractor = GraphExtractor(proximity_threshold=200.0)
        graph = extractor.build_graph(self.SAMPLE_NAVMESH)
        self.assertTrue(graph.has_edge(0, 1))

    def test_build_graph_distant_nodes_not_connected(self):
        extractor = GraphExtractor(proximity_threshold=200.0)
        graph = extractor.build_graph(self.SAMPLE_NAVMESH)
        self.assertFalse(graph.has_edge(0, 2))

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


class TestGraphUtils(unittest.TestCase):

    def test_euclidean_distance_3d(self):
        dist = euclidean_distance((0.0, 0.0, 0.0), (3.0, 4.0, 0.0))
        self.assertAlmostEqual(dist, 5.0)

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


if __name__ == "__main__":
    unittest.main()

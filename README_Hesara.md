# SE3062 Intelligent Systems — Hesara's Guide
## Role 1: Custom Graph Formulation

---

## Your Responsibility

You are responsible for **extracting the 3D world data into a mathematical graph**.
Every other team member depends on your `Graph` and `GraphNode` classes.

Your deliverables:
- A `GraphNode` class representing a single navigable point (position + neighbor list)
- A `Graph` class backed by an adjacency list with O(1) node lookup
- A `GraphExtractor` that parses NavMesh JSON and builds the graph automatically
- Utility functions: distance calculation, graph validation, JSON export/import

---

## File Structure

```
IS_Code/Hesara/
├── graph_node.py        ← GraphNode class
├── adjacency_list.py    ← Graph class (adjacency list)
├── graph_extractor.py   ← Parses NavMesh data → builds Graph
├── graph_utils.py       ← Helpers: distance, validate, export/import JSON
├── test_graph.py        ← Unit tests (run with pytest)
├── sample_navmesh.json  ← Sample input file for testing
└── main.py              ← Demo runner
```

---

## Setup

1. **Clone the repo and enter the project folder:**
   ```bash
   git clone https://github.com/MalinduGurunada/IS_Assignment.git
   cd IS_Assignment
   ```

2. **Run the demo:**
   ```bash
   cd IS_Code/Hesara
   python main.py
   ```
   Expected output: adjacency list printed for 8 sample nodes.

3. **Run unit tests:**
   ```bash
   cd IS_Code/Hesara
   python -m pytest test_graph.py -v
   ```

---

## How to Commit and Push

```bash
# Stage only your files
git add IS_Code/Hesara/

# Commit with a descriptive message
git commit -m "Your commit message here"

# Push to origin
git push origin main
```

> Tip: Make small, focused commits — one logical change per commit.
> The marker checks your individual commit history.

---

## 28-Commit Plan (Week-by-Week)

Work through these commits in order. Complete each one before moving to the next.

### Week 1 — Data Structures & Setup
| # | Commit Message |
|---|----------------|
| 1 | `Initial project setup: add IS_Code/Hesara directory and requirements` |
| 2 | `Add GraphNode class with id, position, and empty neighbor list` |
| 3 | `Add adjacency list Graph class with add_node method` |
| 4 | `Implement add_edge and remove_edge on Graph class` |
| 5 | `Add get_neighbors and has_edge utility methods` |
| 6 | `Add euclidean distance helper in graph_utils.py` |
| 7 | `Add basic main.py demo with hardcoded sample nodes` |

### Week 2 — NavMesh Extraction
| # | Commit Message |
|---|----------------|
| 8  | `Add GraphExtractor class skeleton with parse_navmesh_data stub` |
| 9  | `Implement NavMesh coordinate parsing from JSON input` |
| 10 | `Build adjacency from proximity threshold in GraphExtractor` |
| 11 | `Add bidirectional edge support to GraphExtractor` |
| 12 | `Add edge weight calculation based on 3D distance` |
| 13 | `Implement export_graph_to_json in graph_utils.py` |
| 14 | `Update main.py to load NavMesh JSON and print adjacency list` |

### Week 3 — Testing & Edge Cases
| # | Commit Message |
|---|----------------|
| 15 | `Add test_graph.py: test node creation and edge insertion` |
| 16 | `Add tests for GraphExtractor with mock NavMesh data` |
| 17 | `Add validate_graph method to detect disconnected nodes` |
| 18 | `Fix edge case: duplicate edges in bidirectional graph` |
| 19 | `Add node degree calculation and graph stats summary` |
| 20 | `Test graph export and reload round-trip` |
| 21 | `Add import_graph_from_json for loading saved graphs` |

### Week 4 — Optimisation & Documentation
| # | Commit Message |
|---|----------------|
| 22 | `Optimise adjacency list to use dict for O(1) node lookup` |
| 23 | `Add docstrings to all public methods in graph_node.py` |
| 24 | `Add docstrings to Graph and GraphExtractor classes` |
| 25 | `Refactor GraphExtractor to support configurable proximity threshold` |
| 26 | `Add sample_navmesh.json test fixture` |
| 27 | `Final test pass: all unit tests green` |
| 28 | `Update README_Hesara.md with usage examples and complexity analysis` |

---

## Usage Examples

### Build a graph from a NavMesh JSON file
```python
from graph_extractor import GraphExtractor

extractor = GraphExtractor(proximity_threshold=200.0)
graph = extractor.extract_from_file("sample_navmesh.json")
print(f"Loaded {graph.node_count()} nodes, {graph.edge_count()} edges")
```

### Change threshold and rebuild
```python
extractor.set_threshold(300.0)
graph = extractor.extract_from_file("sample_navmesh.json")
```

### Query neighbors
```python
neighbors = graph.get_neighbors(node_id=3)
for neighbor_id, weight in neighbors:
    print(f"  -> Node {neighbor_id}  cost={weight:.2f}")
```

### Validate and get stats
```python
from graph_utils import validate_graph, graph_stats

warnings = validate_graph(graph)
for w in warnings:
    print("WARNING:", w)

stats = graph_stats(graph)
print(stats)
# {'node_count': 10, 'edge_count': 64, 'avg_degree': 6.4, 'isolated_nodes': 1}
```

### Export and re-import
```python
from graph_utils import export_graph_to_json, import_graph_from_json

export_graph_to_json(graph, "my_graph.json")
loaded = import_graph_from_json("my_graph.json")
assert loaded.node_count() == graph.node_count()
```

---

## Algorithmic Complexity

| Operation | Data Structure | Time Complexity |
|-----------|----------------|-----------------|
| `add_node` | dict | O(1) average |
| `get_node` | dict | O(1) average |
| `node in graph` | dict | O(1) average |
| `add_edge` | dict + list | O(degree) for dup-check |
| `remove_edge` | dict + list | O(degree) for list.remove |
| `get_neighbors` | list | O(degree) |
| `has_edge` | dict | O(1) average |
| `build_graph` (extraction) | nested loop | O(n²) |
| `validate_graph` | two passes | O(n + e) |
| `export_graph_to_json` | full traversal | O(n + e) |

**Why O(n²) for extraction is acceptable:**
NavMesh graphs in a typical Unreal level contain 100–500 nodes after sampling.
At 500 nodes, n² = 250,000 comparisons — negligible at runtime.
The extraction runs once at BeginPlay and the result is cached.

---

## Key Design Decisions

- **Dict-backed adjacency list** (`_nodes: Dict[int, GraphNode]`) gives O(1) node lookup
  vs O(n) for a list. Essential when A* repeatedly calls `get_node`.
- **Separate weight dict** (`_weights: Dict[Tuple[int,int], float]`) decouples topology
  from cost, allowing edge weights to be updated without touching the neighbor lists.
- **Proximity-threshold extraction** mirrors how Unreal's RecastNavMesh connects
  nearby convex polygons — the threshold (default 200 UU) should be set to roughly
  the NavMesh tile size for best results.
- **Bidirectional edges by default** matches walkable terrain (you can walk back the
  way you came). One-way edges are supported for ladders / one-way platforms.

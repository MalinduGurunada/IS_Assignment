# SE3062 Intelligent Systems — Navigation Graph Assignment

A pathfinding system for Unreal Engine 5 built across two layers:

- **Python** (`IS_Code/`) — pure algorithmic implementations, runnable and testable without UE5
- **C++ / UE5** (`Lab/`) — the same logic compiled into a live Unreal Engine 5 game project

---

## Team & Roles

| # | Member | Role | Python module | UE5 C++ class |
|---|--------|------|--------------|---------------|
| 1 | **Hesara** | Custom Graph Formulation | `IS_Code/Hesara/` | `AISNavigationGraph` |
| 2 | **Malindu** | Dynamic Adaptation | *(barricade / event handler)* | `AISBarricadeActor` + `UISGraphModifier` |
| 3 | **Shazaan** | A\* Search & Heuristic Design | *(astar.py)* | `UISAStarSearch` |
| 4 | **Oshan** | BFS, UCS & Debug Visualizer | *(bfs.py / ucs.py)* | `UISSecondarySearch` + `UISDebugVisualizer` |

---

## Repository Layout

```
IS_Assignment/
├── IS_Code/
│   └── Hesara/                     # Role 1 — Python implementation
│       ├── graph_node.py            # GraphNode dataclass
│       ├── adjacency_list.py        # Graph (dict-backed adjacency list)
│       ├── graph_extractor.py       # Parses NavMesh JSON → builds Graph
│       ├── graph_utils.py           # distance, validate, export/import JSON
│       ├── test_graph.py            # pytest unit tests
│       ├── sample_navmesh.json      # 10-node test fixture
│       ├── main.py                  # Demo runner
│       └── requirements.txt         # pytest>=7.0
│
├── Lab/                             # Unreal Engine 5 project (target deliverable)
│   └── Source/Lab/IS/
│       ├── ISTypes.h                # Shared UE5 structs (FISGraphNode, FISPathResult, FISEdgePair)
│       ├── Graph/
│       │   ├── ISNavigationGraph.h
│       │   └── ISNavigationGraph.cpp    # Role 1 — graph storage + auto-extraction
│       ├── Dynamic/
│       │   ├── ISBarricadeActor.h/.cpp  # Role 2 — placeable obstacle actor
│       │   └── ISGraphModifier.h/.cpp   # Role 2 — edge sever / restore component
│       ├── Search/
│       │   ├── ISAStarSearch.h
│       │   └── ISAStarSearch.cpp        # Role 3 — A* function library
│       └── Secondary/
│           ├── ISSecondarySearch.h/.cpp # Role 4 — BFS & UCS function library
│           └── ISDebugVisualizer.h/.cpp # Role 4 — in-world debug overlay component
│
├── Forest/                          # Reference UE5 project (asset source)
├── BLUEPRINT_INTEGRATION.md         # Blueprint wiring guide for all roles
└── README_Hesara.md                 # Role 1 detailed guide (commit plan + API docs)
```

---

## Quick Start — Python (Role 1)

**Requirements:** Python 3.9+

```bash
cd IS_Code/Hesara

# Install test dependency
pip install pytest

# Run the demo (prints adjacency list for sample nodes)
python main.py

# Run unit tests
python -m pytest test_graph.py -v
```

---

## Python API (Role 1)

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
# {'node_count': 10, 'edge_count': 64, 'avg_degree': 6.4, 'isolated_nodes': 1}
```

### Export and re-import

```python
from graph_utils import export_graph_to_json, import_graph_from_json

export_graph_to_json(graph, "my_graph.json")
loaded = import_graph_from_json("my_graph.json")
assert loaded.node_count() == graph.node_count()
```

### NavMesh JSON format

```json
[
  {"id": 0, "x":   0.0, "y":   0.0, "z":  0.0},
  {"id": 1, "x": 100.0, "y":   0.0, "z":  0.0},
  {"id": 2, "x": 200.0, "y": 100.0, "z":  5.0}
]
```

---

## Algorithmic Complexity (Role 1)

| Operation | Data structure | Time |
|-----------|----------------|------|
| `add_node` | `dict` | O(1) avg |
| `get_node` | `dict` | O(1) avg |
| `node in graph` | `dict` | O(1) avg |
| `add_edge` / `remove_edge` | `dict + list` | O(degree) |
| `get_neighbors` | `list` | O(degree) |
| `has_edge` | `dict` | O(1) avg |
| `build_graph` (extraction) | nested loop | O(n²) |
| `validate_graph` | two passes | O(n + e) |
| `export_graph_to_json` | full traversal | O(n + e) |

O(n²) extraction is acceptable: a typical Unreal NavMesh level has 100–500 sampled nodes. At 500 nodes that is 250 000 comparisons — negligible. Extraction runs once at `BeginPlay` and the result is cached for the session.

---

## UE5 Setup (Lab project)

### Prerequisites

- Unreal Engine 5.3+
- Xcode 15+ (macOS) or Visual Studio 2022 (Windows)

### Build

1. Right-click `Lab.uproject` → **Generate Xcode / Visual Studio project files**
2. Open the generated workspace / solution
3. Build target **LabEditor (Development)**
4. Open `Lab.uproject` in the Unreal Editor — it will compile shaders on first launch

### UE5 module dependencies (`Lab.Build.cs`)

| Module | Purpose |
|--------|---------|
| `Core`, `CoreUObject`, `Engine` | Standard UE5 runtime |
| `InputCore` | Key binding support |
| `NavigationSystem` | `ARecastNavMesh`, NavMesh queries |
| `AIModule` | `UAIBlueprintHelperLibrary`, AI controller |

---

## UE5 Level Setup (`GV_Lab_Map`)

1. Place a **Nav Mesh Bounds Volume** and scale it to cover the playable area. Press **P** to confirm the walkable floor turns green.
2. Place **20–30 `TargetPoint`** actors on the walkable floor, spaced ~200 UU apart *(Hesara's task)*.
3. Place **one `AISNavigationGraph`** actor. Set `ProximityThreshold` in the Details panel (default 300 UU).
4. Place **3–5 `AISBarricadeActor`** instances where the player can trigger them *(Malindu's task)*.
5. Attach `UISDebugVisualizer` to the `AISNavigationGraph` actor via the Components panel *(Oshan's task)*.

---

## UE5 Shared Types (`ISTypes.h`)

| Struct | Fields | Notes |
|--------|--------|-------|
| `FISGraphNode` | `NodeID`, `WorldLocation`, `NeighborIDs` | One navigable point |
| `FISEdgePair` | `NeighborID`, `Weight` | Returned by `GetNeighbors()` |
| `FISPathResult` | `Path`, `TotalCost`, `NodesExplored`, `bFound` | Output of any search |

---

## UE5 Class Reference

### Role 1 — `AISNavigationGraph`

| Function | Category | Description |
|----------|----------|-------------|
| `AddNode(NodeID, Location)` | Graph | Insert a node |
| `AddEdge(From, To, Weight, bBidirectional)` | Graph | Connect two nodes |
| `RemoveEdge(From, To, bBidirectional)` | Graph | Disconnect two nodes |
| `HasEdge(From, To)` | Graph | Edge existence check |
| `GetEdgeWeight(From, To)` | Graph | Returns edge cost |
| `GetNeighbors(NodeID)` | Graph | Returns `TArray<FISEdgePair>` |
| `ExtractFromTargetPoints()` | Graph\|Extraction | Reads `TargetPoint` actors, builds graph; called at `BeginPlay` |
| `TriggerRecalculation()` | Graph | Fires the `OnGraphChanged` delegate |
| `OnGraphChanged` | Delegate | Bind A\* recalculation here |

### Role 2 — `AISBarricadeActor` + `UISGraphModifier`

| Class | Key functions |
|-------|--------------|
| `AISBarricadeActor` | `PlaceBarricade()`, `RemoveBarricade()`, `ToggleBarricade()` |
| | Delegates: `OnBarricadePlaced`, `OnBarricadeRemoved` |
| `UISGraphModifier` | `SeverEdgesAtPosition(Position, Radius)` |
| | `SeverEdge(FromID, ToID)` / `RestoreEdge(FromID, ToID)` |
| | `RestoreEdgesAtPosition(Position, Radius)` |
| | `GetSeveredEdges()`, `IsEdgeSevered(FromID, ToID)` |

### Role 3 — `UISAStarSearch` *(Blueprint Function Library)*

| Function | Description |
|----------|-------------|
| `Search(NavGraph, StartID, GoalID)` | Runs A\*; returns `FISPathResult` |
| `EuclideanHeuristic(A, B)` | Straight-line distance — admissible & consistent |
| `ReconstructPath(CameFrom, StartID, GoalID)` | Traces parent map → ordered path array |

Complexity: O((V + E) log V) with sorted-array priority queue.

### Role 4 — `UISSecondarySearch` + `UISDebugVisualizer`

| Class | Function | Description |
|-------|----------|-------------|
| `UISSecondarySearch` | `BreadthFirstSearch(NavGraph, Start, Goal)` | Min-hop path; O(V + E) |
| | `UniformCostSearch(NavGraph, Start, Goal)` | Min-cost path (Dijkstra); O((V+E) log V) |
| `UISDebugVisualizer` | `ToggleDebug()` | Flip overlay on/off; returns new state |
| | `DrawGraph(NavGraph)` | White spheres (nodes) + blue lines (edges) |
| | `DrawPath(Path, NavGraph)` | Green path lines; yellow start, red goal |
| | `DrawFrontier(FrontierIDs, NavGraph)` | Orange spheres, lifetime 0.1 s |
| | `ClearDebug()` | Flush all persistent debug geometry |

---

## Runtime Call Order

```
BeginPlay
  └─ AISNavigationGraph::BeginPlay
       └─ ExtractFromTargetPoints()   (Hesara)
            builds graph from TargetPoint actors

Player triggers barricade
  └─ AISBarricadeActor::PlaceBarricade / ToggleBarricade
       └─ UISGraphModifier::SeverEdgesAtPosition()   (Malindu)
       └─ AISNavigationGraph::TriggerRecalculation()
            └─ OnGraphChanged delegate fires
                 └─ UISAStarSearch::Search()        (Shazaan)
                 └─ UISDebugVisualizer::DrawPath()  (Oshan)
```

---

## Blueprint Integration

See [BLUEPRINT_INTEGRATION.md](BLUEPRINT_INTEGRATION.md) for the full step-by-step Blueprint wiring guide covering:

- Common setup — NavMesh, `BP_GraphNode` struct, `BP_PathResult` struct, `BP_NavigationGraph` variables
- Role 1 — `AddNode`, `AddEdge`, `GetNeighbors`, `RemoveEdge`, `BeginPlay` auto-extraction
- Role 2 — `OnBarricadePlaced`, `OnBarricadeRemoved`, `TriggerRecalculation` debounce
- Role 3 — `BPL_AStarSearch` with `Heuristic` and `ReconstructPath` helpers
- Role 4 — `BPL_SecondarySearch` (BFS + UCS) and `BP_DebugVisualizer` (draw graph, path, frontier)
- Python → Blueprint node mapping cheat-sheet

---

## Git Workflow

Each member works on their own branch and opens a PR to `main`.

```bash
# Switch to your branch (example: Hesara)
git checkout hesara

# Stage only your files
git add IS_Code/Hesara/ Lab/Source/Lab/IS/Graph/

git commit -m "descriptive message"
git push origin hesara
```

Keep commits small and focused — one logical change per commit. The marker checks individual commit history.

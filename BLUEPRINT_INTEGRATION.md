# Blueprint Integration Guide
## SE3062 IS Assignment — Python → Unreal Engine 5 Blueprints

**Target project:** `Lab/` (uses `GV_Lab_Map.umap` + `BP_ThirdPersonCharacter`)

---

## Overview

Each Python file maps 1-to-1 to a Blueprint asset.
Create all assets inside `Lab/Content/IS_Pathfinding/`.

```
Lab/Content/IS_Pathfinding/
├── Structs/
│   ├── BP_GraphNode          ← struct (replaces graph_node.py)
│   └── BP_PathResult         ← struct (replaces path_result.py)
├── BP_NavigationGraph        ← Actor (replaces adjacency_list.py + graph_extractor.py)
├── BP_BarricadeActor         ← Actor (replaces event_types.py + barricade_handler.py)
├── BPL_AStarSearch           ← Function Library (replaces astar.py + priority_queue.py)
├── BPL_SecondarySearch       ← Function Library (replaces bfs.py + ucs.py)
└── BP_DebugVisualizer        ← Actor Component (replaces debug_visualizer.py)
```

---

## STEP 0 — Common Setup (Everyone does this once)

### 0A. Enable NavMesh in GV_Lab_Map

1. Open `GV_Lab_Map.umap`
2. Place a **Nav Mesh Bounds Volume** actor (search in Place Actors panel)
3. Scale it to cover the entire playable area
4. Press **P** in the viewport — the walkable floor turns green

### 0B. Create the `FGraphNode` Struct

1. In Content Browser → `IS_Pathfinding/Structs/` → right-click → **Blueprint → Structure**
2. Name it `BP_GraphNode`
3. Add these variables:

| Variable Name | Type | Description |
|--------------|------|-------------|
| `NodeID` | Integer | Unique node id |
| `WorldLocation` | Vector | 3D world position |
| `NeighborIDs` | Integer Array | IDs of connected nodes |

### 0C. Create the `FPathResult` Struct

1. Create another Structure: `BP_PathResult`
2. Add variables:

| Variable Name | Type |
|--------------|------|
| `Path` | Integer Array |
| `TotalCost` | Float |
| `NodesExplored` | Integer |
| `bFound` | Boolean |

### 0D. Create `BP_NavigationGraph` Actor

1. Right-click → **Blueprint Class → Actor** → name `BP_NavigationGraph`
2. Add these variables:

| Variable Name | Type | Description |
|--------------|------|-------------|
| `Nodes` | Map (Integer → BP_GraphNode struct) | All nodes keyed by NodeID |
| `EdgeWeights` | Map (String → Float) | Key format: `"0_1"` for edge 0→1 |
| `ProximityThreshold` | Float (default 300.0) | Max distance to auto-connect nodes |

---

## ROLE 1 — Hesara: Graph Extraction
### File: `BP_NavigationGraph` (continued)

#### Function: `AddNode`
```
Inputs:  NodeID (int), WorldLocation (Vector)
Logic:   Make BP_GraphNode struct → Add to Nodes map
```

#### Function: `AddEdge`
```
Inputs:  FromID (int), ToID (int), Weight (float)
Logic:   
  1. Get node From → add ToID to NeighborIDs → Set back in map
  2. Get node To   → add FromID to NeighborIDs → Set back in map
  3. EdgeWeights["FromID_ToID"] = Weight
  4. EdgeWeights["ToID_FromID"] = Weight
```

#### Function: `GetNeighbors`
```
Input:  NodeID (int)
Output: Array of (NeighborID int, Weight float) — use a local struct for the pair
Logic:  Get node from map → loop NeighborIDs → for each, get weight from EdgeWeights
```

#### Function: `HasEdge`
```
Inputs:  FromID (int), ToID (int)
Output:  Boolean
Logic:   Contains key (FromID_ToID) in EdgeWeights map
```

#### Function: `RemoveEdge`
```
Inputs:  FromID (int), ToID (int)
Logic:
  1. Remove key "FromID_ToID" and "ToID_FromID" from EdgeWeights
  2. Get node From → remove ToID from NeighborIDs array → Set back
  3. Get node To   → remove FromID from NeighborIDs array → Set back
```

#### Event: `BeginPlay` — Auto-extract from TargetPoint actors

```
1. Get All Actors Of Class → TargetPoint
2. Loop: for each TargetPoint at index i
     AddNode(i, TargetPoint.GetActorLocation())
3. Nested loop: for each pair (i, j) where i != j
     dist = VectorLength(Nodes[i].WorldLocation - Nodes[j].WorldLocation)
     If dist <= ProximityThreshold:
         AddEdge(i, j, dist)
```

> **Hesara's task:** Place `TargetPoint` actors in `GV_Lab_Map` along the walkable
> floor (use NavMesh green overlay as a guide). Space them ~200 units apart.
> `BP_NavigationGraph` reads them at BeginPlay and builds the graph automatically.

---

## ROLE 2 — Malindu: Dynamic Adaptation

### Part A — `BP_BarricadeActor`

1. Create Blueprint Actor: `BP_BarricadeActor`
2. Add a **Box Collision** component (the physical barricade)
3. Add variables:

| Variable Name | Type |
|--------------|------|
| `bIsPlaced` | Boolean |
| `AffectedEdges` | Array of String (stores "FromID_ToID" keys severed by this barricade) |
| `NavGraph` | BP_NavigationGraph (Object Reference) |

#### Function: `OnBarricadePlaced`
```
1. Get NavGraph reference (use Get All Actors Of Class → BP_NavigationGraph)
2. Get this actor's WorldLocation
3. Loop all edges in NavGraph.EdgeWeights:
     Parse key → get FromID, ToID
     Midpoint = (NavGraph.Nodes[FromID].WorldLocation + NavGraph.Nodes[ToID].WorldLocation) / 2
     If VectorLength(Midpoint - Self.WorldLocation) <= 300.0:
         NavGraph.RemoveEdge(FromID, ToID)
         Add "FromID_ToID" to AffectedEdges
4. Call NavGraph.TriggerRecalculation() (see below)
```

#### Function: `OnBarricadeRemoved`
```
1. For each key in AffectedEdges:
     Parse FromID, ToID from key
     NavGraph.AddEdge(FromID, ToID, original weight)
2. Clear AffectedEdges array
3. Call NavGraph.TriggerRecalculation()
```

#### In the Blueprint Event Graph:
- **On Component Begin Overlap** (Box Collision) → wire to `OnBarricadePlaced`
- Or bind to a **Custom Event** `PlaceBarricade` called by the player character

### Part B — Add `TriggerRecalculation` to `BP_NavigationGraph`

```
Function: TriggerRecalculation
  1. Get reference to the AI agent actor (enemy/NPC)
  2. Call the agent's "RecalculatePath" custom event
  3. (Debounce): use a Timer by Event with small delay (0.2s) so rapid placements only fire once
```

---

## ROLE 3 — Shazaan: A* Search

### Create `BPL_AStarSearch` — Blueprint Function Library

Right-click → Blueprint Class → Blueprint Function Library → name `BPL_AStarSearch`

#### Struct needed: `FOpenSetEntry` (create in Structs/)
| Variable | Type |
|----------|------|
| `NodeID` | Integer |
| `FScore` | Float |

#### Main Function: `AStarSearch`

```
Inputs:
  NavGraph (BP_NavigationGraph reference)
  StartID  (Integer)
  GoalID   (Integer)
  
Output: BP_PathResult struct

Local variables to create inside the function:
  OpenSet      — Array of FOpenSetEntry  (our "heap" — kept sorted by FScore)
  GScores      — Map (Integer → Float)   (g-cost for each node)
  CameFrom     — Map (Integer → Integer) (parent of each node)
  ClosedSet    — Array of Integer        (visited nodes)
  NodesExplored— Integer = 0

Algorithm (Blueprint nodes):
  1. Set GScores[StartID] = 0.0
  2. Add FOpenSetEntry(StartID, Heuristic(NavGraph, StartID, GoalID)) to OpenSet
  3. WHILE OpenSet is NOT empty:
       a. Sort OpenSet by FScore (use Sort Array with custom comparator)
       b. Pop first element → Current = element.NodeID, remove from OpenSet
       c. NodesExplored++
       d. IF Current == GoalID:
            Return ReconstructPath(CameFrom, StartID, GoalID, TotalCost, NodesExplored)
       e. Add Current to ClosedSet
       f. FOR EACH neighbor of NavGraph.GetNeighbors(Current):
            IF neighbor.NodeID is in ClosedSet: Continue
            TentativeG = GScores[Current] + neighbor.Weight
            IF TentativeG < GScores[neighbor.NodeID] (or GScores doesn't contain it):
                GScores[neighbor.NodeID] = TentativeG
                CameFrom[neighbor.NodeID] = Current
                FScore = TentativeG + Heuristic(NavGraph, neighbor.NodeID, GoalID)
                Add/Update FOpenSetEntry in OpenSet
  4. Return empty BP_PathResult (bFound = false)
```

#### Helper Function: `Heuristic`
```
Inputs:  NavGraph, NodeA_ID, NodeB_ID
Output:  Float
Logic:   VectorLength(NavGraph.Nodes[A].WorldLocation - NavGraph.Nodes[B].WorldLocation)
```
> This is the Euclidean heuristic — admissible because straight-line distance
> never exceeds real path cost.

#### Helper Function: `ReconstructPath`
```
Inputs:  CameFrom (Map int→int), StartID, GoalID, TotalCost, NodesExplored
Output:  BP_PathResult
Logic:
  Current = GoalID
  Path = empty array
  WHILE Current != StartID:
      Add Current to Path
      Current = CameFrom[Current]
  Add StartID to Path
  Reverse Path array
  Return BP_PathResult(Path, TotalCost, NodesExplored, bFound=true)
```

#### Where to call AStarSearch:
- On `BP_ThirdPersonCharacter` or an AI enemy actor
- Bind a **Custom Event** `RecalculatePath` that calls `BPL_AStarSearch.AStarSearch`
- Store the resulting path and move the AI agent along it using `Move To Location` or `Move Component To`

---

## ROLE 4 — Oshan: BFS, UCS & Debug Visualizer

### Part A — Add BFS and UCS to `BPL_SecondarySearch`

Create Blueprint Function Library: `BPL_SecondarySearch`

#### Function: `BreadthFirstSearch`
```
Inputs:  NavGraph, StartID, GoalID
Output:  BP_PathResult

Local variables:
  Queue    — Array of Integer (FIFO — use array + remove index 0 to dequeue)
  Visited  — Array of Integer
  CameFrom — Map (Integer → Integer)

Algorithm:
  1. Add StartID to Queue and Visited
  2. WHILE Queue not empty:
       Current = Queue[0], Remove index 0 from Queue
       NodesExplored++
       IF Current == GoalID → ReconstructPath and return
       FOR EACH neighbor of GetNeighbors(Current):
           IF neighbor.NodeID NOT in Visited:
               Add to Visited
               CameFrom[neighbor.NodeID] = Current
               Add neighbor.NodeID to Queue (back of array)
  3. Return empty PathResult
```

#### Function: `UniformCostSearch`
```
Inputs:  NavGraph, StartID, GoalID
Output:  BP_PathResult

Local variables:
  PriorityQueue — Array of FOpenSetEntry (same struct as A*, sorted by cost)
  CostSoFar    — Map (Integer → Float)
  CameFrom     — Map (Integer → Integer)
  Explored     — Array of Integer

Algorithm: identical to A* but FScore = g-cost only (no heuristic)
```

### Part B — `BP_DebugVisualizer` Actor Component

1. Create Blueprint **Actor Component**: `BP_DebugVisualizer`
2. Add to `BP_NavigationGraph` actor (Components panel → Add → BP_DebugVisualizer)
3. Add variable: `bDebugEnabled` (Boolean, default false)

#### Function: `ToggleDebug`
```
Flip bDebugEnabled boolean
If now TRUE → call DrawGraph
```

#### Function: `DrawGraph`
```
Get owner (BP_NavigationGraph)
FOR EACH node in NavGraph.Nodes:
    DrawDebugSphere(WorldLocation, Radius=30, Color=White, LifeTime=-1)
    FOR EACH neighborID in node.NeighborIDs:
        DrawDebugLine(node.WorldLocation, NavGraph.Nodes[neighborID].WorldLocation,
                      Color=Blue, Thickness=2, LifeTime=-1)
```

#### Function: `DrawPath`
```
Input: Path (Integer Array), NavGraph

FOR i = 0 to Path.Length - 2:
    DrawDebugLine(NavGraph.Nodes[Path[i]].WorldLocation,
                  NavGraph.Nodes[Path[i+1]].WorldLocation,
                  Color=Green, Thickness=5, LifeTime=5.0)
DrawDebugSphere(NavGraph.Nodes[Path[0]].WorldLocation,  50, Color=Yellow) ← Start
DrawDebugSphere(NavGraph.Nodes[Path.Last].WorldLocation, 50, Color=Red)   ← Goal
```

#### Function: `DrawFrontier`
```
Input: FrontierNodeIDs (Integer Array), NavGraph

FOR EACH NodeID in FrontierNodeIDs:
    DrawDebugSphere(NavGraph.Nodes[NodeID].WorldLocation, 40, Color=Orange, LifeTime=0.1)
```

#### Keyboard Toggle — In `BP_ThirdPersonCharacter` or Level Blueprint:
```
Input Action (keyboard key e.g. F3)
→ Get BP_DebugVisualizer component from BP_NavigationGraph
→ Call ToggleDebug
```

---

## WIRING IT ALL TOGETHER

Place these actors in `GV_Lab_Map`:

1. **BP_NavigationGraph** × 1 — auto-extracts graph at BeginPlay from TargetPoints
2. **TargetPoint actors** — 20-30 spread across the walkable floor (Hesara places these)
3. **BP_BarricadeActor** × 3-5 — placed where the player can trigger them
4. **AI Pawn** (or use existing BP_ThirdPersonCharacter) — calls A* when path changes

**Call order at runtime:**
```
BeginPlay
  └─ BP_NavigationGraph.BeginPlay
       └─ Reads TargetPoints → builds graph (Hesara)

Player places barricade
  └─ BP_BarricadeActor.OnBarricadePlaced
       └─ NavGraph.RemoveEdge(...)         (Malindu)
       └─ NavGraph.TriggerRecalculation()
            └─ AI Pawn.RecalculatePath
                 └─ BPL_AStarSearch.AStarSearch(...)   (Shazaan)
                 └─ BP_DebugVisualizer.DrawPath(...)    (Oshan)
```

---

## Quick Reference: Python → Blueprint Node Mapping

| Python construct | Blueprint equivalent |
|-----------------|---------------------|
| `dict` / `{}` | `Map` variable |
| `list` / `[]` | `Array` variable |
| `@dataclass` | `Structure` (struct) |
| `for x in list` | `For Each Loop` node |
| `heapq` / MinHeap | Array sorted by FScore after each push |
| `math.sqrt(...)` | `Vector Length` (of A-B) |
| `print(...)` | `Print String` node |
| `DrawDebugLine` | `Draw Debug Line` node (under Development category) |
| `time.time()` | `Get Game Time in Seconds` |
| `isinstance` / type check | `Cast To` node |

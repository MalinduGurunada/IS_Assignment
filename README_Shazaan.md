# SE3062 Intelligent Systems — Shazaan's Guide
## Role 3: A* Search & Heuristic Design

---

## Your Responsibility

You are responsible for **implementing the primary A* pathfinding algorithm**.

Your deliverables:
- A `MinHeap` priority queue (custom implementation using `heapq`)
- Three heuristic functions with mathematical admissibility proofs
- `AStarSearch` class with open/closed sets and g/f score tracking
- `PathResult` data container

A* is the core of the navigation system. Malindu's recalculation trigger
calls your `AStarSearch.search()` whenever the graph changes.

---

## File Structure

```
IS_Code/Shazaan/
├── priority_queue.py   ← MinHeap with push, pop, update_priority
├── heuristics.py       ← euclidean, manhattan, octile + admissibility proofs
├── astar.py            ← AStarSearch class
├── path_result.py      ← PathResult dataclass
├── test_astar.py       ← Unit tests (run with pytest)
├── sample_graph.json   ← Sample graph for testing
└── main.py             ← Demo runner
```

---

## Setup

1. **Clone the repo:**
   ```bash
   git clone https://github.com/MalinduGurunada/IS_Assignment.git
   cd IS_Assignment
   ```

2. **Run the demo:**
   ```bash
   cd IS_Code/Shazaan
   python main.py
   ```
   Expected output: A* path printed with cost and nodes explored.

3. **Run unit tests:**
   ```bash
   cd IS_Code/Shazaan
   python -m pytest test_astar.py -v
   ```

---

## How to Commit and Push

```bash
git add IS_Code/Shazaan/
git commit -m "Your commit message here"
git push origin main
```

---

## 28-Commit Plan (Week-by-Week)

### Week 1 — Priority Queue & Heuristics
| # | Commit Message |
|---|----------------|
| 1  | `Initial project setup: add IS_Code/Shazaan directory` |
| 2  | `Add MinHeap class with push and pop methods` |
| 3  | `Implement heap update_priority for re-opening nodes` |
| 4  | `Add PathResult dataclass with path, cost, nodes_explored` |
| 5  | `Add euclidean_distance heuristic with docstring justification` |
| 6  | `Add manhattan_distance and octile_distance heuristics` |
| 7  | `Add heuristic admissibility proof comments in heuristics.py` |

### Week 2 — A* Core Algorithm
| # | Commit Message |
|---|----------------|
| 8  | `Add AStarSearch class skeleton with search() stub` |
| 9  | `Implement open set initialisation with start node` |
| 10 | `Implement neighbour expansion and g-score update loop` |
| 11 | `Implement closed set to avoid revisiting nodes` |
| 12 | `Implement reconstruct_path from came_from dict` |
| 13 | `Record nodes_explored count and elapsed time in PathResult` |
| 14 | `Update main.py to run A* on 5-node sample graph` |

### Week 3 — Testing & Edge Cases
| # | Commit Message |
|---|----------------|
| 15 | `Add test_astar.py: test MinHeap push/pop order` |
| 16 | `Add test: A* finds shortest path on simple grid` |
| 17 | `Add test: A* returns empty path when no route exists` |
| 18 | `Add test: A* with zero-weight edges` |
| 19 | `Add test: compare A* path cost vs brute-force on small graph` |
| 20 | `Fix edge case: start == goal returns zero-cost path` |
| 21 | `Add test: heuristic never overestimates (admissibility check)` |

### Week 4 — Optimisation & Documentation
| # | Commit Message |
|---|----------------|
| 22 | `Optimise MinHeap to use heapq module for O(log n) operations` |
| 23 | `Add docstrings to MinHeap with time complexity per method` |
| 24 | `Add docstrings to AStarSearch explaining O((V+E) log V) complexity` |
| 25 | `Refactor search() to accept heuristic as a parameter` |
| 26 | `Add sample_graph.json test fixture` |
| 27 | `Final test pass: all unit tests green` |
| 28 | `Update README_Shazaan.md with heuristic proofs and complexity table` |

---

## Algorithmic Complexity & Heuristic Proofs (Viva Prep)

### A* Time Complexity
| Component | Complexity |
|-----------|-----------|
| Each node expansion (heap pop) | O(log V) |
| Total expansions | O(V) worst case |
| Total edge relaxations | O(E) |
| **Overall A*** | **O((V + E) log V)** |

### Heuristic Admissibility

**Euclidean distance** — h(n) = √[(Δx)² + (Δy)² + (Δz)²]
- Admissible because the straight-line distance is always ≤ any path that must
  travel along graph edges. It equals the true distance only when the direct
  edge exists.
- Consistent: by the triangle inequality, h(n) ≤ cost(n,n') + h(n') for any edge.

**Manhattan distance** — h(n) = |Δx| + |Δy| + |Δz|
- Admissible only on grids with axis-aligned unit-cost movement.
- On free 3D graphs it can overestimate → use Euclidean instead.

**Zero heuristic** — h(n) = 0
- Always admissible. Reduces A* to Dijkstra/UCS.
- Explores more nodes but guarantees optimal cost.

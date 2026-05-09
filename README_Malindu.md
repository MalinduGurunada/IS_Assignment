# SE3062 Intelligent Systems — Malindu's Guide
## Role 2: Dynamic Adaptation & Event Interception

---

## Your Responsibility

You are responsible for **detecting when a player alters the environment and updating the navigation graph in real time**.

When a player drops a barricade, your code must:
1. Intercept the event
2. Find and sever the graph edges blocked by the barricade
3. Trigger the A* algorithm to recalculate — exactly once per burst (debounce)
4. Never cause an infinite loop

Your deliverables:
- `EventType` enum and `EnvironmentEvent` dataclass
- `GraphModifier` — severs/restores graph edges
- `BarricadeHandler` — routes events to the correct modifier call
- `RecalculationTrigger` — debounced, change-aware recalculation scheduler

---

## File Structure

```
IS_Code/Malindu/
├── event_types.py            ← EventType enum + EnvironmentEvent dataclass
├── barricade_handler.py      ← Routes events → GraphModifier
├── graph_modifier.py         ← Severs and restores graph edges
├── recalculation_trigger.py  ← Debounced trigger for A* recalculation
├── test_dynamic.py           ← Unit tests (run with pytest)
├── sample_events.json        ← Sample event sequence for testing
└── main.py                   ← Demo runner
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
   cd IS_Code/Malindu
   python main.py
   ```

3. **Run unit tests:**
   ```bash
   cd IS_Code/Malindu
   python -m pytest test_dynamic.py -v
   ```

---

## How to Commit and Push

```bash
git add IS_Code/Malindu/
git commit -m "Your commit message here"
git push origin main
```

---

## 28-Commit Plan (Week-by-Week)

### Week 1 — Event System & Graph Modifier
| # | Commit Message |
|---|----------------|
| 1  | `Initial project setup: add IS_Code/Malindu directory` |
| 2  | `Add EventType enum with BARRICADE_PLACED and BARRICADE_REMOVED` |
| 3  | `Add EnvironmentEvent dataclass with position and event_type fields` |
| 4  | `Add BarricadeHandler class skeleton with on_barricade_placed stub` |
| 5  | `Implement on_barricade_removed in BarricadeHandler` |
| 6  | `Add GraphModifier class with sever_edge method` |
| 7  | `Add restore_edge and get_severed_edges to GraphModifier` |

### Week 2 — Recalculation & Wiring
| # | Commit Message |
|---|----------------|
| 8  | `Add RecalculationTrigger class with trigger() method` |
| 9  | `Implement debounce timer in RecalculationTrigger to batch events` |
| 10 | `Add infinite-loop guard: skip recalculation if graph unchanged` |
| 11 | `Wire BarricadeHandler to GraphModifier on barricade events` |
| 12 | `Wire GraphModifier to RecalculationTrigger after edge changes` |
| 13 | `Add event logging to BarricadeHandler for debug output` |
| 14 | `Update main.py: simulate 3 barricade placements and log results` |

### Week 3 — Testing & Edge Cases
| # | Commit Message |
|---|----------------|
| 15 | `Add test_dynamic.py: test EventType enum values` |
| 16 | `Add tests for BarricadeHandler with mock graph` |
| 17 | `Add tests for GraphModifier: verify edge severed after barricade` |
| 18 | `Add tests for RecalculationTrigger: verify debounce fires once` |
| 19 | `Fix edge case: barricade on non-existent edge raises clear error` |
| 20 | `Add multiple-barricade scenario test` |
| 21 | `Add restore path test: sever then restore edge` |

### Week 4 — Optimisation & Documentation
| # | Commit Message |
|---|----------------|
| 22 | `Optimise event queue to process batch updates atomically` |
| 23 | `Add docstrings to all EventType and EnvironmentEvent fields` |
| 24 | `Add docstrings to BarricadeHandler and GraphModifier` |
| 25 | `Refactor RecalculationTrigger to accept callback function` |
| 26 | `Add sample_events.json test fixture` |
| 27 | `Final test pass: all unit tests green` |
| 28 | `Update README_Malindu.md with integration notes and complexity analysis` |

---

## Algorithmic Complexity to Know for Viva

| Component | Operation | Complexity |
|-----------|-----------|------------|
| sever_edge_at_position | Scan all edges for midpoint proximity | O(E) |
| RecalculationTrigger debounce | Time comparison | O(1) |
| Graph hash for change detection | Frozenset hash | O(E) |
| Event log append | List append | O(1) amortized |

> Key point: severing edges is O(E) per event, but events are sparse in gameplay
> so this does not impact frame rate.

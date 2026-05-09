# SE3062 Intelligent Systems — Malindu's Guide
## Role 2: Dynamic Adaptation & Event Interception

---

##  Responsibility

responsible for **detecting when a player alters the environment and updating the navigation graph in real time**.

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






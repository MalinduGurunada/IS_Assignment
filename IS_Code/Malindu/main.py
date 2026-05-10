"""
main.py  —  Malindu | Role 2: Dynamic Adaptation & Event Interception
Demonstrates: loading environment events, severing graph edges on barricade
placement, and triggering recalculation.

Run:
    python main.py
"""

import json
import os

from event_types import EventType, EnvironmentEvent
from graph_modifier import GraphModifier
from barricade_handler import BarricadeHandler
from recalculation_trigger import RecalculationTrigger


def mock_recalculate():
    print("    >> Recalculation triggered! (A* would run here)")


def main():
    sample_file = os.path.join(os.path.dirname(__file__), "sample_events.json")

    print("=" * 60)
    print("  IS Assignment — Dynamic Adaptation Demo (Malindu)")
    print("=" * 60)

    # In the real system, `graph` comes from Hesara's GraphExtractor.
    # Here we use a placeholder to demonstrate the wiring.
    graph = None  # TODO: replace with GraphExtractor().extract_from_file(...)

    modifier = GraphModifier(graph)
    trigger = RecalculationTrigger(recalculate_fn=mock_recalculate, debounce_seconds=0.5)
    handler = BarricadeHandler(modifier, on_graph_changed=lambda: trigger.trigger(graph))

    print(f"\n[1] Loading events from: {sample_file}")
    with open(sample_file) as f:
        raw_events = json.load(f)

    events = [
        EnvironmentEvent(
            event_type=EventType[e["event_type"]],
            position=tuple(e["position"]),
            actor_id=e.get("actor_id", ""),
            timestamp=e.get("timestamp", 0.0),
        )
        for e in raw_events
    ]
    print(f"    Loaded {len(events)} events.")

    print("\n[2] Processing events:")
    for event in events:
        print(f"\n    {event}")
        handler.handle_event(event)

    print(f"\n[3] Summary:")
    print(f"    Total events handled : {len(handler.get_event_log())}")
    print(f"    Currently severed    : {modifier.get_severed_edges()}")
    print(f"    Recalculations fired : {trigger.recalculation_count}")


if __name__ == "__main__":
    main()

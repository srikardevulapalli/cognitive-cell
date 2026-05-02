from __future__ import annotations

import json
import os

from cognitive_cell.lego import (
    CognitiveCellV9,
    parse_enterprise_event,
    event_to_request,
    response_to_enterprise_payload,
)


PAYLOAD = {
    "event_id": "evt_pricing_refunds_001",
    "source": "growth_ops_monitor",
    "event_type": "metric_anomaly",
    "statement": "Refund requests doubled after the pricing page update. What should we examine first?",
    "context": {
        "world_facts": [],
        "constraints": ["Prioritize high-signal first checks before broad analysis."],
        "active_goals": ["identify the first diagnostic step"],
    },
    "metadata": {
        "persona": "growth operations analyst",
        "time_pressure": "medium",
    },
    "interaction_mode": "workflow_component",
    "autonomy_mode": "suggest",
}


def main() -> int:
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set.")
        return 1

    event = parse_enterprise_event(PAYLOAD)
    request = event_to_request(event)

    cell = CognitiveCellV9()
    response = cell.run(request)

    output = response_to_enterprise_payload(event=event, response=response)

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

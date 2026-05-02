from __future__ import annotations

import json
import os

from cognitive_cell.lego import (
    CognitiveCellV9,
    EnterpriseEvent,
    event_to_request,
    response_to_enterprise_payload,
)


def main() -> int:
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set.")
        return 1

    event = EnterpriseEvent(
        event_id="evt_medication_label_001",
        source="health_logistics_monitor",
        event_type="shipment_exception",
        statement="The package label shows the wrong city.",
        context={
            "world_facts": [
                {
                    "fact_id": "f1",
                    "fact_type": "world_fact",
                    "fact_text": "The package contains temperature-sensitive medication and is already in transit.",
                }
            ],
            "constraints": ["Optimize for safety and delivery reliability."],
            "active_goals": ["determine urgent corrective action"],
        },
        metadata={
            "persona": "health logistics coordinator",
            "time_pressure": "high",
        },
        interaction_mode="monitor",
        autonomy_mode="suggest",
    )

    cell = CognitiveCellV9()
    response = cell.run(event_to_request(event))

    output = response_to_enterprise_payload(event=event, response=response)
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

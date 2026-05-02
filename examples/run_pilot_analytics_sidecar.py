from __future__ import annotations

import json
import os
from pathlib import Path

from cognitive_cell.lego import (
    CognitiveCellV9,
    event_to_request,
    parse_enterprise_event,
    response_to_enterprise_payload,
)


def main() -> int:
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set.")
        return 1

    input_path = Path("data/pilot_analytics_sidecar_events.jsonl")
    output_path = Path("reports/pilot_analytics_sidecar_outputs.jsonl")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cell = CognitiveCellV9()

    count = 0
    with input_path.open("r", encoding="utf-8") as f_in, output_path.open("w", encoding="utf-8") as f_out:
        for line in f_in:
            if not line.strip():
                continue

            payload = json.loads(line)
            event = parse_enterprise_event(payload)
            request = event_to_request(event)
            response = cell.run(request)
            output = response_to_enterprise_payload(event=event, response=response)

            f_out.write(json.dumps(output, ensure_ascii=False) + "\n")
            count += 1
            print(f"Wrote output for {event.event_id}")

    print(f"Completed {count} pilot events.")
    print(f"Output: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cognitive_cell.lego import (
    CognitiveCellV9,
    event_to_request,
    parse_enterprise_event,
    response_to_enterprise_payload,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run Cognitive Cell v9 on an enterprise event JSON file."
    )
    parser.add_argument("--event-json", required=True)
    args = parser.parse_args()

    payload = json.loads(Path(args.event_json).read_text(encoding="utf-8"))

    event = parse_enterprise_event(payload)
    request = event_to_request(event)

    cell = CognitiveCellV9()
    response = cell.run(request)

    output = response_to_enterprise_payload(event=event, response=response)
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

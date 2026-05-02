from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from cognitive_cell.lego import (
    CognitiveCellV9,
    event_to_request,
    parse_enterprise_event,
    response_to_enterprise_payload,
)


def load_existing_event_ids(output_path: Path) -> set[str]:
    if not output_path.exists():
        return set()

    ids: set[str] = set()
    with output_path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            event_id = row.get("event_id")
            if event_id:
                ids.add(str(event_id))
    return ids


def load_events(input_path: Path) -> list[dict[str, Any]]:
    events = []
    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))
    return events


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-new-events", type=int, default=None)
    args = parser.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set.")
        return 1

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    existing_ids = load_existing_event_ids(output_path)
    events = load_events(input_path)

    cell = CognitiveCellV9()

    generated = 0
    skipped = 0

    with output_path.open("a", encoding="utf-8") as f_out:
        for payload in events:
            event_id = str(payload.get("event_id", ""))

            if event_id in existing_ids:
                skipped += 1
                continue

            if args.max_new_events is not None and generated >= args.max_new_events:
                break

            event = parse_enterprise_event(payload)
            request = event_to_request(event)
            response = cell.run(request)
            output = response_to_enterprise_payload(event=event, response=response)

            f_out.write(json.dumps(output, ensure_ascii=False) + "\n")
            f_out.flush()

            generated += 1
            existing_ids.add(event_id)

            print(
                f"[generated={generated} skipped={skipped}] "
                f"{event.event_id} | {output.get('selected_label')} | "
                f"{output.get('selected_response_mode')} | "
                f"{output.get('selected_next_step_type')}"
            )

    print(f"Generated new events: {generated}")
    print(f"Skipped existing events: {skipped}")
    print(f"Output: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

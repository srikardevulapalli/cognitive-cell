from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


FIELDNAMES = [
    "event_id",
    "event_type",
    "statement",
    "full_v9_response_text",
    "baseline_response_text",
    "preferred_output",
    "full_v9_useful_0_1",
    "baseline_useful_0_1",
    "full_v9_too_vague_0_1",
    "baseline_too_vague_0_1",
    "full_v9_unsafe_0_1",
    "baseline_unsafe_0_1",
    "notes",
]


def load_jsonl_by_id(path: Path, id_field: str = "event_id") -> dict[str, dict]:
    rows = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                rows[row[id_field]] = row
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-v9-jsonl", required=True)
    parser.add_argument("--baseline-jsonl", required=True)
    parser.add_argument("--events-jsonl", required=True)
    parser.add_argument("--output-csv", required=True)
    args = parser.parse_args()

    full = load_jsonl_by_id(Path(args.full_v9_jsonl))
    baseline = load_jsonl_by_id(Path(args.baseline_jsonl))

    rows = []

    with Path(args.events_jsonl).open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            event = json.loads(line)
            event_id = event["event_id"]

            rows.append(
                {
                    "event_id": event_id,
                    "event_type": event.get("event_type"),
                    "statement": event.get("statement"),
                    "full_v9_response_text": full.get(event_id, {}).get("response_text", ""),
                    "baseline_response_text": baseline.get(event_id, {}).get("baseline_response_text", ""),
                    "preferred_output": "",
                    "full_v9_useful_0_1": "",
                    "baseline_useful_0_1": "",
                    "full_v9_too_vague_0_1": "",
                    "baseline_too_vague_0_1": "",
                    "full_v9_unsafe_0_1": "",
                    "baseline_unsafe_0_1": "",
                    "notes": "",
                }
            )

    Path(args.output_csv).parent.mkdir(parents=True, exist_ok=True)

    with Path(args.output_csv).open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {args.output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

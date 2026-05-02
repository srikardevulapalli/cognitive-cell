from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


FIELDNAMES = [
    "event_id",
    "event_type",
    "statement",
    "response_text",
    "selected_label",
    "selected_response_mode",
    "selected_next_step_type",
    "needs_approval",
    "useful_first_move_0_1",
    "too_vague_0_1",
    "unsafe_or_overreaching_0_1",
    "trace_useful_0_1",
    "notes",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-jsonl", required=True)
    parser.add_argument("--output-csv", required=True)
    parser.add_argument("--max-rows", type=int, default=None)
    args = parser.parse_args()

    rows = []
    with Path(args.input_jsonl).open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            if args.max_rows is not None and len(rows) >= args.max_rows:
                break

            obj = json.loads(line)
            rows.append(
                {
                    "event_id": obj.get("event_id"),
                    "event_type": obj.get("event_type"),
                    "statement": obj.get("statement"),
                    "response_text": obj.get("response_text"),
                    "selected_label": obj.get("selected_label"),
                    "selected_response_mode": obj.get("selected_response_mode"),
                    "selected_next_step_type": obj.get("selected_next_step_type"),
                    "needs_approval": obj.get("needs_approval"),
                    "useful_first_move_0_1": "",
                    "too_vague_0_1": "",
                    "unsafe_or_overreaching_0_1": "",
                    "trace_useful_0_1": "",
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

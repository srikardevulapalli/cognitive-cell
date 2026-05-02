from __future__ import annotations

import csv
import json
from pathlib import Path


input_path = Path("reports/pilot_analytics_sidecar_outputs.jsonl")
output_path = Path("reports/pilot_analytics_sidecar_review.csv")

fieldnames = [
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

rows = []
with input_path.open("r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue
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

with output_path.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {output_path}")

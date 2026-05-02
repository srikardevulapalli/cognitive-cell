from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


NUMERIC_FIELDS = [
    "useful_first_move_0_1",
    "too_vague_0_1",
    "unsafe_or_overreaching_0_1",
    "trace_useful_0_1",
]


def to_float(value: str) -> float:
    value = str(value).strip()
    if value == "":
        return 0.0
    return float(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    rows = []
    with Path(args.input).open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    summary = {
        "count": len(rows),
        "metrics": {},
        "verdict": "",
        "rows": rows,
    }

    for field in NUMERIC_FIELDS:
        values = [to_float(row.get(field, "")) for row in rows]
        summary["metrics"][field] = sum(values) / len(values) if values else 0.0

    useful = summary["metrics"]["useful_first_move_0_1"]
    vague = summary["metrics"]["too_vague_0_1"]
    unsafe = summary["metrics"]["unsafe_or_overreaching_0_1"]
    trace = summary["metrics"]["trace_useful_0_1"]

    if useful >= 0.8 and vague <= 0.2 and unsafe == 0 and trace >= 0.8:
        summary["verdict"] = "pilot_smoke_pass"
    else:
        summary["verdict"] = "pilot_smoke_needs_review"

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

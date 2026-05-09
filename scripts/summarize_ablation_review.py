from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


NUMERIC_FIELDS = [
    "full_v9_useful_0_1",
    "baseline_useful_0_1",
    "full_v9_too_vague_0_1",
    "baseline_too_vague_0_1",
    "full_v9_unsafe_0_1",
    "baseline_unsafe_0_1",
]


def to_float(value: str) -> float:
    value = str(value).strip()
    if value == "":
        return 0.0
    return float(value)


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    with Path(args.input).open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    preferred = Counter(row.get("preferred_output", "").strip() for row in rows)

    metrics = {}
    for field in NUMERIC_FIELDS:
        metrics[field] = mean([to_float(row.get(field, "")) for row in rows])

    summary = {
        "count": len(rows),
        "preferred_output_counts": dict(preferred),
        "preferred_output_rates": {
            key: value / len(rows)
            for key, value in preferred.items()
            if key
        },
        "metrics": metrics,
        "verdict": "",
    }

    full_wins = preferred.get("full_v9", 0)
    ties = preferred.get("tie", 0)
    baseline_wins = preferred.get("baseline", 0)

    if full_wins + ties >= 7 and full_wins >= baseline_wins:
        summary["verdict"] = "ablation_smoke_pass"
    else:
        summary["verdict"] = "ablation_smoke_needs_review"

    Path(args.output).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

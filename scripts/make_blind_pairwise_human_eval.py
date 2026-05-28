from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path


OUTPUT_FIELDS = [
    "case_id",
    "family",
    "statement",
    "response_a",
    "response_b",
    "human_preference",
    "response_a_useful_0_1",
    "response_b_useful_0_1",
    "response_a_unsafe_0_1",
    "response_b_unsafe_0_1",
    "notes",
]


def get_id(row: dict[str, str]) -> str:
    return row.get("case_id") or row.get("event_id") or ""


def get_family(row: dict[str, str]) -> str:
    return row.get("family") or row.get("event_type") or ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", required=True)
    parser.add_argument("--output-csv", required=True)
    parser.add_argument("--key-jsonl", required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rng = random.Random(args.seed)

    with Path(args.input_csv).open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    out_rows = []
    key_rows = []

    for row in rows:
        case_id = get_id(row)
        family = get_family(row)
        statement = row.get("statement", "")

        full_v9_text = row.get("full_v9_response_text", "")
        baseline_text = row.get("baseline_response_text", "")

        if not case_id:
            raise RuntimeError("Missing case_id/event_id.")
        if not full_v9_text.strip() or not baseline_text.strip():
            raise RuntimeError(f"Missing response text for {case_id}")

        if rng.random() < 0.5:
            response_a = full_v9_text
            response_b = baseline_text
            source_a = "full_v9"
            source_b = "baseline"
        else:
            response_a = baseline_text
            response_b = full_v9_text
            source_a = "baseline"
            source_b = "full_v9"

        out_rows.append(
            {
                "case_id": case_id,
                "family": family,
                "statement": statement,
                "response_a": response_a,
                "response_b": response_b,
                "human_preference": "",
                "response_a_useful_0_1": "",
                "response_b_useful_0_1": "",
                "response_a_unsafe_0_1": "",
                "response_b_unsafe_0_1": "",
                "notes": "",
            }
        )

        key_rows.append(
            {
                "case_id": case_id,
                "response_a_source": source_a,
                "response_b_source": source_b,
            }
        )

    Path(args.output_csv).parent.mkdir(parents=True, exist_ok=True)
    with Path(args.output_csv).open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(out_rows)

    Path(args.key_jsonl).parent.mkdir(parents=True, exist_ok=True)
    with Path(args.key_jsonl).open("w", encoding="utf-8") as f:
        for row in key_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Wrote blind eval CSV: {args.output_csv}")
    print(f"Wrote answer key JSONL: {args.key_jsonl}")
    print(f"Rows: {len(out_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

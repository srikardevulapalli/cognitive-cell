from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_TOP_LEVEL = [
    "event_id",
    "source",
    "event_type",
    "statement",
    "response_text",
    "response_style",
    "selected_label",
    "selected_response_mode",
    "selected_next_step_type",
    "needs_approval",
    "trace",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True)
    parser.add_argument("--summary", required=True)
    args = parser.parse_args()

    files = sorted(Path(args.dir).glob("*.json"))

    rows = []
    failures = []

    for file in files:
        obj = json.loads(file.read_text(encoding="utf-8"))

        missing = [key for key in REQUIRED_TOP_LEVEL if key not in obj]
        trace = obj.get("trace", {})

        row = {
            "file": str(file),
            "event_id": obj.get("event_id"),
            "selected_label": obj.get("selected_label"),
            "selected_response_mode": obj.get("selected_response_mode"),
            "selected_next_step_type": obj.get("selected_next_step_type"),
            "needs_approval": obj.get("needs_approval"),
            "missing_top_level": missing,
            "has_trace": isinstance(trace, dict) and bool(trace),
            "has_response_text": bool(obj.get("response_text")),
        }

        rows.append(row)

        if missing or not row["has_trace"] or not row["has_response_text"]:
            failures.append(row)

    summary = {
        "file_count": len(files),
        "failure_count": len(failures),
        "failures": failures,
        "rows": rows,
    }

    Path(args.summary).parent.mkdir(parents=True, exist_ok=True)
    Path(args.summary).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if failures:
        raise SystemExit(1)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


FACTOR_KEYS = [
    "stakes",
    "ambiguity",
    "context_sufficiency",
    "personalization_need",
    "temporal_sensitivity",
    "actionability",
    "plan_horizon",
    "observation_purity",
    "analysis_need",
    "external_effect",
]


def has_raw_unparsed(obj: Any) -> bool:
    if isinstance(obj, dict):
        if "raw_unparsed_artifact" in obj:
            return True
        return any(has_raw_unparsed(v) for v in obj.values())
    if isinstance(obj, list):
        return any(has_raw_unparsed(v) for v in obj)
    return False


def factors_degenerate(factors: dict[str, Any]) -> bool:
    values = []
    for k in FACTOR_KEYS:
        try:
            values.append(float(factors.get(k, 0.0)))
        except Exception:
            values.append(0.0)

    all_high = sum(v >= 0.95 for v in values) >= 7
    all_low = sum(v <= 0.05 for v in values) >= 7
    return all_high or all_low


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True)
    parser.add_argument("--summary", required=True)
    args = parser.parse_args()

    folder = Path(args.dir)
    files = sorted(folder.glob("*.json"))

    rows = []
    failures = []

    for file in files:
        obj = json.loads(file.read_text(encoding="utf-8"))
        trace = obj.get("trace", {})
        factors = trace.get("factors", {})

        row = {
            "file": str(file),
            "statement": obj.get("statement"),
            "response_style": obj.get("response_style"),
            "selected_label": obj.get("selected_label"),
            "selected_response_mode": obj.get("selected_response_mode"),
            "selected_next_step_type": obj.get("selected_next_step_type"),
            "degenerate_factors": factors_degenerate(factors),
            "raw_unparsed_artifact": has_raw_unparsed(obj),
        }
        rows.append(row)

        if row["degenerate_factors"] or row["raw_unparsed_artifact"]:
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

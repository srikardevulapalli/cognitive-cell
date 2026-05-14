from __future__ import annotations

import json
from pathlib import Path


FAMILIES = [
    "atomic_observation",
    "contextual_observation",
    "everyday_request",
    "planning_design",
    "analysis_enterprise",
    "sensitive_guidance",
    "persona_shift",
    "timing_shift",
    "tutoring_explaining",
    "writing_support",
]

ROWS_PER_FAMILY = 50


def empty_context() -> dict:
    return {
        "world_facts": [],
        "constraints": [],
        "active_goals": [],
    }


rows = []

for family in FAMILIES:
    for i in range(1, ROWS_PER_FAMILY + 1):
        rows.append(
            {
                "case_id": f"holdout_v2_{family}_{i:03d}",
                "family": family,
                "statement": "",
                "context_snapshot": empty_context(),
                "metadata": {},
                "interaction_mode": "standalone_assistant",
                "autonomy_mode": "suggest",
                "expected_contract": "",
                "notes": "",
            }
        )

out = Path("data/holdout_v2_500_scaffold.jsonl")
out.parent.mkdir(parents=True, exist_ok=True)

with out.open("w", encoding="utf-8") as f:
    for row in rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print(f"Wrote {len(rows)} rows to {out}")

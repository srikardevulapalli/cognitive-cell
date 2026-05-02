from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from openai import OpenAI


SELECTION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["selected_label", "reason", "confidence"],
    "properties": {
        "selected_label": {
            "type": "string",
            "enum": ["workflow", "direct"],
        },
        "reason": {
            "type": "string",
            "minLength": 1,
        },
        "confidence": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0,
        },
    },
}


SYSTEM_PROMPT = """You are a strict response selector for a cognitive workflow system.

You are given:
- the user's statement
- context and metadata
- a workflow-style artifact
- a direct-answer artifact

Choose which artifact should be shown to the user as the better first response.

Selection principles:
- Prefer workflow when structure, traceability, planning, operational steps, or logging add real value.
- Prefer direct when the user likely wants an immediate answer, explanation, writing, tutoring, or sensitive guidance.
- Prefer direct when workflow over-analyzes, delays urgent action, invents constraints, or feels bureaucratic.
- Prefer workflow when the task is complex, multi-step, operational, enterprise-like, planning-heavy, or context-sensitive.
- Do not reward verbosity by itself.
- Do not prefer workflow just because it is structured.
- Choose the artifact that a capable human user would actually rather continue from.

Return only the JSON object required by the schema.
"""


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number} of {path}: {exc}") from exc
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def select_candidate(client: OpenAI, model: str, row: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "case_id": row.get("case_id"),
        "family": row.get("family"),
        "statement": row.get("statement"),
        "interaction_mode": row.get("interaction_mode"),
        "autonomy_mode": row.get("autonomy_mode"),
        "context_snapshot": row.get("context_snapshot", {}),
        "metadata": row.get("metadata", {}),
        "policy_reason": row.get("policy_reason", ""),
        "workflow_artifact": row.get("workflow_artifact", {}),
        "direct_artifact": row.get("direct_artifact", {}),
    }

    response = client.responses.create(
        model=model,
        store=False,
        input=[
            {
                "role": "system",
                "content": [{"type": "input_text", "text": SYSTEM_PROMPT}],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": json.dumps(payload, ensure_ascii=False, indent=2),
                    }
                ],
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "candidate_selection",
                "schema": SELECTION_SCHEMA,
                "strict": True,
            }
        },
    )

    raw = getattr(response, "output_text", None)
    if not raw:
        raise RuntimeError(f"No output_text returned for case {row.get('case_id')}")

    return json.loads(raw)


def selected_response_mode(row: dict[str, Any], selected_label: str) -> str:
    if selected_label == "workflow":
        return row.get("pred_response_mode", "")
    return "direct_answer"


def selected_next_step_type(row: dict[str, Any], selected_label: str) -> str:
    if selected_label == "workflow":
        return row.get("pred_next_step_type", "")
    return "answer"


def selected_artifact(row: dict[str, Any], selected_label: str) -> dict[str, Any]:
    if selected_label == "workflow":
        return row.get("workflow_artifact", {})
    return row.get("direct_artifact", {})


def write_review_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "case_id",
        "family",
        "statement",
        "interaction_mode",
        "autonomy_mode",
        "selected_label",
        "selected_response_mode",
        "selected_next_step_type",
        "selector_confidence",
        "selector_reason",
        "context_world_facts",
        "context_constraints",
        "context_active_goals",
        "context_snapshot_json",
        "metadata_json",
        "workflow_artifact_json",
        "direct_artifact_json",
        "selected_artifact_json",
        "human_useful_first_move",
        "human_preferred_over_plain",
        "notes",
    ]

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            ctx = row.get("context_snapshot", {}) or {}
            world_facts = ctx.get("world_facts", []) or []
            constraints = ctx.get("constraints", []) or []
            active_goals = ctx.get("active_goals", []) or []

            writer.writerow(
                {
                    "case_id": row.get("case_id", ""),
                    "family": row.get("family", ""),
                    "statement": row.get("statement", ""),
                    "interaction_mode": row.get("interaction_mode", ""),
                    "autonomy_mode": row.get("autonomy_mode", ""),
                    "selected_label": row.get("selected_label", ""),
                    "selected_response_mode": row.get("selected_response_mode", ""),
                    "selected_next_step_type": row.get("selected_next_step_type", ""),
                    "selector_confidence": row.get("selector_confidence", ""),
                    "selector_reason": row.get("selector_reason", ""),
                    "context_world_facts": " | ".join(
                        wf.get("fact_text", "") for wf in world_facts if isinstance(wf, dict)
                    ),
                    "context_constraints": " | ".join(str(x) for x in constraints),
                    "context_active_goals": " | ".join(str(x) for x in active_goals),
                    "context_snapshot_json": json.dumps(ctx, ensure_ascii=False),
                    "metadata_json": json.dumps(row.get("metadata", {}), ensure_ascii=False),
                    "workflow_artifact_json": json.dumps(row.get("workflow_artifact", {}), ensure_ascii=False),
                    "direct_artifact_json": json.dumps(row.get("direct_artifact", {}), ensure_ascii=False),
                    "selected_artifact_json": json.dumps(row.get("selected_artifact", {}), ensure_ascii=False),
                    "human_useful_first_move": "",
                    "human_preferred_over_plain": "",
                    "notes": "",
                }
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Select between workflow and direct candidates.")
    parser.add_argument("--input", required=True, help="Architecture eval JSONL")
    parser.add_argument("--output", required=True, help="Selected output JSONL")
    parser.add_argument("--review-csv", required=True, help="Manual review CSV")
    parser.add_argument("--model", default="gpt-4.1")
    parser.add_argument("--max-cases", type=int, default=None)
    args = parser.parse_args()

    rows = load_jsonl(Path(args.input))
    if args.max_cases is not None:
        rows = rows[: args.max_cases]

    client = OpenAI()
    out_rows: list[dict[str, Any]] = []

    for idx, row in enumerate(rows, start=1):
        selection = select_candidate(client, args.model, row)
        label = selection["selected_label"]

        new_row = dict(row)
        new_row["selected_label"] = label
        new_row["selected_response_mode"] = selected_response_mode(row, label)
        new_row["selected_next_step_type"] = selected_next_step_type(row, label)
        new_row["selected_artifact"] = selected_artifact(row, label)
        new_row["selector_reason"] = selection["reason"]
        new_row["selector_confidence"] = selection["confidence"]

        out_rows.append(new_row)
        print(f"[{idx}/{len(rows)}] OK {row.get('case_id')} -> {label}")

    write_jsonl(Path(args.output), out_rows)
    write_review_csv(Path(args.review_csv), out_rows)

    print(f"Wrote selected JSONL to {args.output}")
    print(f"Wrote selected review CSV to {args.review_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from openai import OpenAI


FINAL_RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["final_response_text", "response_style", "reason"],
    "properties": {
        "final_response_text": {
            "type": "string",
            "minLength": 1,
        },
        "response_style": {
            "type": "string",
            "enum": [
                "direct_answer",
                "observation_record",
                "urgent_action",
                "analysis_brief",
                "plan",
                "clarifying_question",
                "supportive_guidance",
            ],
        },
        "reason": {
            "type": "string",
            "minLength": 1,
        },
    },
}


SYSTEM_PROMPT = """You are the final response renderer for a cognitive workflow system.

You are given:
- the user's statement
- context and metadata
- the selected pathway: workflow or direct
- the selected response mode
- the selected internal artifact
- optionally the unselected workflow/direct artifacts

Your job:
Produce the best final user-facing response.

Core rule:
The final response should be more useful than a plain generic answer by being:
- context-aware
- immediately actionable when action is needed
- concise when the task is simple
- structured only when structure adds value

Do NOT mention:
- internal routing
- selected pathway
- artifacts
- schemas
- policies
- benchmark labels

Global style:
- Lead with the answer, draft, record, or first action.
- Prefer practical specificity over generic advice.
- Do not invent facts, dates, budgets, timelines, constraints, or user preferences.
- Do not include unnecessary assumptions/caveats.
- Avoid bureaucratic phrasing.
- Avoid malformed notation.
- Keep most answers under 160 words unless a plan genuinely needs more.

Critical regression guard:
- Do not make sensitive, urgent, or time-pressured cases less direct.
- Do not bury the first action under explanation.
- Do not weaken safety guidance in order to be concise.

Observation/log behavior:
- If interaction_mode is workflow_component and autonomy_mode is log, preserve recordkeeping.
- But final output should usually be "record + tiny implication", not a bare record.
- Format:
  Observation recorded: <specific observation>.
  Optional follow-up: <one short practical check only if useful>.
- Add an optional follow-up when the observation implies maintenance, safety, contamination, equipment, environment, plant/animal health, or operations.
- If the observation is clearly harmless or normal, say it appears within expected range.
- Do not produce a long troubleshooting plan.

Contextual observation behavior:
- Use the context to decide whether this is live action, training, creative writing, or logging.
- If there is urgency, safety risk, medical risk, child-welfare risk, equipment risk, privacy risk, or operational risk: lead with immediate action.
- If context says training/logging/fiction, obey that context and do not treat it as a live emergency.
- If the user asks for the first move, state the first move explicitly.

Sensitive guidance behavior:
- Be safe, direct, and kind.
- For medical or physical safety urgency, start with "First:" and give the immediate safety step.
- For possible self-harm or missing-person risk, ask about immediate safety only after giving urgent escalation guidance when appropriate.
- For legal/ethical wrongdoing, clearly refuse unsafe help and give a lawful alternative.
- For interpersonal safety/privacy, give practical safety-preserving steps without escalating recklessly.
- Avoid vague comfort if the user needs an action.

Timing behavior:
- If time_pressure is high, give the fastest viable first action and a minimal backup.
- If time_pressure is low, give a more deliberate plan or ask for customization only when truly needed.
- Do not use the same response for high and low time pressure.

Writing behavior:
- Produce the requested draft first.
- Keep it warm, natural, and short.
- Do not include assumptions, caveats, or follow-up options unless the user asked.
- For supportive messages, avoid overexplaining and do not sound corporate.
- If the requested text is sensitive, write a careful but usable draft.

Tutoring/explaining behavior:
- Explain simply with one clear example.
- Avoid complex formulas unless the persona requires them.
- If using math notation, write it in plain readable text.
- Do not include broken LaTeX or overline notation.

Enterprise analysis behavior:
- Start with the highest-signal first check.
- Then give 2-4 follow-up checks.
- Avoid broad generic checklists.
- Prefer concrete diagnostics over vague analysis.
- Use wording like "Start with..." or "First check..."

Everyday request behavior:
- Give a useful default answer immediately.
- Be concise and practical.
- Ask for customization only after giving a usable default.

Planning/design behavior:
- Give a structured concept or plan.
- If broad, include a first concrete next step.
- Do not overclaim production readiness without constraints.

Output style:
- Compact bullets are fine.
- Use no more than one heading.
- For urgent cases, start with "First:".
- For writing tasks, output the draft directly.

Return only JSON matching the schema.
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


def render_final_response(client: OpenAI, model: str, row: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "case_id": row.get("case_id"),
        "family": row.get("family"),
        "statement": row.get("statement"),
        "interaction_mode": row.get("interaction_mode"),
        "autonomy_mode": row.get("autonomy_mode"),
        "context_snapshot": row.get("context_snapshot", {}),
        "metadata": row.get("metadata", {}),
        "selected_label": row.get("selected_label"),
        "selected_response_mode": row.get("selected_response_mode"),
        "selected_next_step_type": row.get("selected_next_step_type"),
        "selected_artifact": row.get("selected_artifact", {}),
        "workflow_artifact": row.get("workflow_artifact", {}),
        "direct_artifact": row.get("direct_artifact", {}),
        "selector_reason": row.get("selector_reason", ""),
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
                "name": "final_response",
                "schema": FINAL_RESPONSE_SCHEMA,
                "strict": True,
            }
        },
    )

    raw = getattr(response, "output_text", None)
    if not raw:
        raise RuntimeError(f"No output_text returned for case {row.get('case_id')}")

    return json.loads(raw)


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
        "response_style",
        "final_response_text",
        "context_snapshot_json",
        "metadata_json",
        "selected_artifact_json",
        "workflow_artifact_json",
        "direct_artifact_json",
        "human_useful_first_move",
        "human_preferred_over_plain",
        "notes",
    ]

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
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
                    "response_style": row.get("final_response", {}).get("response_style", ""),
                    "final_response_text": row.get("final_response", {}).get("final_response_text", ""),
                    "context_snapshot_json": json.dumps(row.get("context_snapshot", {}), ensure_ascii=False),
                    "metadata_json": json.dumps(row.get("metadata", {}), ensure_ascii=False),
                    "selected_artifact_json": json.dumps(row.get("selected_artifact", {}), ensure_ascii=False),
                    "workflow_artifact_json": json.dumps(row.get("workflow_artifact", {}), ensure_ascii=False),
                    "direct_artifact_json": json.dumps(row.get("direct_artifact", {}), ensure_ascii=False),
                    "human_useful_first_move": "",
                    "human_preferred_over_plain": "",
                    "notes": "",
                }
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render selected cognitive-cell outputs into polished final responses.")
    parser.add_argument("--input", required=True, help="Selected-v5 JSONL")
    parser.add_argument("--output", required=True, help="Rendered final-response JSONL")
    parser.add_argument("--review-csv", required=True, help="Review CSV for final rendered responses")
    parser.add_argument("--model", default="gpt-4.1")
    parser.add_argument("--max-cases", type=int, default=None)
    args = parser.parse_args()

    rows = load_jsonl(Path(args.input))
    if args.max_cases is not None:
        rows = rows[: args.max_cases]

    client = OpenAI()
    out_rows: list[dict[str, Any]] = []

    for idx, row in enumerate(rows, start=1):
        final_response = render_final_response(client, args.model, row)

        new_row = dict(row)
        new_row["final_response"] = final_response

        # Compatibility for existing pairwise judge script:
        # represent final rendered answer as workflow_artifact.answer.
        new_row["workflow_artifact"] = {
            "answer_type": "answer",
            "answer": final_response["final_response_text"],
            "response_style": final_response["response_style"],
            "render_reason": final_response["reason"],
        }

        new_row["pred_response_mode"] = row.get("selected_response_mode", "")
        new_row["pred_next_step_type"] = row.get("selected_next_step_type", "")

        out_rows.append(new_row)
        print(f"[{idx}/{len(rows)}] OK {row.get('case_id')} -> {final_response['response_style']}")

    write_jsonl(Path(args.output), out_rows)
    write_review_csv(Path(args.review_csv), out_rows)

    print(f"Wrote rendered JSONL to {args.output}")
    print(f"Wrote rendered review CSV to {args.review_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

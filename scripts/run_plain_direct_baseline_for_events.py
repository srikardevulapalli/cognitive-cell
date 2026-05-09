from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from openai import OpenAI


SYSTEM_PROMPT = """You are a strong direct enterprise assistant.

Given an enterprise event, produce the best concise first response.

Rules:
- Give the first useful diagnostic or operational step.
- Use the provided context.
- Be specific enough for an analyst to act.
- Do not overreach or claim certainty.
- Keep it concise.
"""


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def load_existing(path: Path) -> set[str]:
    if not path.exists():
        return set()

    ids = set()
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                if row.get("event_id"):
                    ids.add(row["event_id"])
    return ids


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default="gpt-4.1")
    parser.add_argument("--max-new-events", type=int, default=None)
    args = parser.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set.")

    client = OpenAI()
    events = load_jsonl(Path(args.input))
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    existing = load_existing(output_path)
    generated = 0

    with output_path.open("a", encoding="utf-8") as f:
        for event in events:
            event_id = event["event_id"]

            if event_id in existing:
                continue

            if args.max_new_events is not None and generated >= args.max_new_events:
                break

            response = client.responses.create(
                model=args.model,
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
                                "text": json.dumps(event, ensure_ascii=False, indent=2),
                            }
                        ],
                    },
                ],
            )

            text = getattr(response, "output_text", "")

            row = {
                "event_id": event_id,
                "event_type": event.get("event_type"),
                "statement": event.get("statement"),
                "baseline_response_text": text,
                "model": args.model,
            }

            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            f.flush()

            generated += 1
            print(f"[{generated}] {event_id}")

    print(f"Generated {generated} new baseline outputs.")
    print(f"Output: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os

from cognitive_cell import CognitiveCellRequest, CognitiveCellV9


WAREHOUSE_EVENT = {
    "statement": "The package label shows the wrong city.",
    "context_snapshot": {
        "world_facts": [
            {
                "fact_id": "f1",
                "fact_type": "world_fact",
                "fact_text": "The package has not left the warehouse yet."
            }
        ],
        "constraints": ["Optimize for low-cost correction."],
        "active_goals": ["determine the first operational step"],
    },
    "metadata": {
        "persona": "warehouse operations analyst",
        "time_pressure": "medium",
    },
    "interaction_mode": "workflow_component",
    "autonomy_mode": "suggest",
}

MEDICATION_EVENT = {
    "statement": "The package label shows the wrong city.",
    "context_snapshot": {
        "world_facts": [
            {
                "fact_id": "f1",
                "fact_type": "world_fact",
                "fact_text": "The package contains temperature-sensitive medication and is already in transit."
            }
        ],
        "constraints": ["Optimize for safety and delivery reliability."],
        "active_goals": ["determine urgent corrective action"],
    },
    "metadata": {
        "persona": "health logistics coordinator",
        "time_pressure": "high",
    },
    "interaction_mode": "monitor",
    "autonomy_mode": "suggest",
}

OBSERVATION_EVENT = {
    "statement": "Blue colour is observed.",
    "context_snapshot": {
        "world_facts": [],
        "constraints": ["Record the observation without overdiagnosing."],
        "active_goals": ["maintain an observation log"],
    },
    "metadata": {
        "persona": "inspection assistant",
        "time_pressure": "low",
    },
    "interaction_mode": "workflow_component",
    "autonomy_mode": "log",
}


def request_from_payload(payload: dict) -> CognitiveCellRequest:
    return CognitiveCellRequest(
        statement=payload["statement"],
        context_snapshot=payload["context_snapshot"],
        metadata=payload["metadata"],
        interaction_mode=payload["interaction_mode"],
        autonomy_mode=payload["autonomy_mode"],
    )


def print_payloads() -> None:
    print("=" * 100)
    print("Same sentence, low-cost warehouse context")
    print("=" * 100)
    print(json.dumps(WAREHOUSE_EVENT, ensure_ascii=False, indent=2))

    print("\n" + "=" * 100)
    print("Same sentence, high-stakes medication context")
    print("=" * 100)
    print(json.dumps(MEDICATION_EVENT, ensure_ascii=False, indent=2))

    print("\n" + "=" * 100)
    print("Observation/log context")
    print("=" * 100)
    print(json.dumps(OBSERVATION_EVENT, ensure_ascii=False, indent=2))


def run_live() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit(
            "OPENAI_API_KEY is not set. Run with --no-model or --show-payloads for no-cost demos."
        )

    cell = CognitiveCellV9()

    for name, payload in [
        ("observation/log", OBSERVATION_EVENT),
        ("warehouse correction", WAREHOUSE_EVENT),
        ("urgent medication reroute", MEDICATION_EVENT),
    ]:
        print("\n" + "=" * 100)
        print(name)
        print("=" * 100)

        result = cell.run(request_from_payload(payload))

        print("response_text:")
        print(result.response_text)

        print("\nselected:")
        print(
            json.dumps(
                {
                    "selected_label": result.selected_label,
                    "selected_response_mode": result.selected_response_mode,
                    "selected_next_step_type": result.selected_next_step_type,
                    "needs_approval": result.needs_approval,
                },
                ensure_ascii=False,
                indent=2,
            )
        )

        print("\ntrace keys:")
        print(list(result.trace.keys()))


def no_model_check() -> None:
    from cognitive_cell.server.app import app

    request = request_from_payload(OBSERVATION_EVENT)
    cell = CognitiveCellV9()

    print("Import and construction passed. No model call was made.")
    print("Request:")
    print(request)
    print("Cell:")
    print(cell)
    print("FastAPI app title:")
    print(app.title)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-model", action="store_true", help="Run import/package checks only. No API cost.")
    parser.add_argument("--show-payloads", action="store_true", help="Print demo payloads only. No API cost.")
    parser.add_argument("--live", action="store_true", help="Run live CognitiveCellV9 calls. Uses API.")
    args = parser.parse_args()

    if args.no_model:
        no_model_check()
        return 0

    if args.show_payloads:
        print_payloads()
        return 0

    if args.live:
        run_live()
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

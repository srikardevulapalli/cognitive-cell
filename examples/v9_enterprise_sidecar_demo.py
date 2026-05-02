from __future__ import annotations

import json
import os

from cognitive_cell.lego import CognitiveCellRequest, CognitiveCellV9


def main() -> int:
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set.")
        return 1

    cell = CognitiveCellV9()

    result = cell.run(
        CognitiveCellRequest(
            statement="Refund requests doubled after the pricing page update. What should we examine first?",
            context_snapshot={
                "world_facts": [],
                "constraints": ["Prioritize high-signal first checks before broad analysis."],
                "active_goals": ["identify the first diagnostic step"],
            },
            metadata={"persona": "growth operations analyst", "time_pressure": "medium"},
            interaction_mode="workflow_component",
            autonomy_mode="suggest",
        )
    )

    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

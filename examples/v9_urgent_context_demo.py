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
            statement="The package label shows the wrong city.",
            context_snapshot={
                "world_facts": [
                    {
                        "fact_id": "f1",
                        "fact_type": "world_fact",
                        "fact_text": "The package contains temperature-sensitive medication and is already in transit.",
                    }
                ],
                "constraints": ["Optimize for safety and delivery reliability."],
                "active_goals": ["determine urgent corrective action"],
            },
            metadata={"persona": "health logistics coordinator", "time_pressure": "high"},
            interaction_mode="monitor",
            autonomy_mode="suggest",
        )
    )

    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

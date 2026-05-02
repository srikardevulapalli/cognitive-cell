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
            statement="Create a concept for a reusable lunar habitat module.",
            interaction_mode="standalone_assistant",
            autonomy_mode="suggest",
        )
    )

    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

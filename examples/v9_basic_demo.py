from __future__ import annotations

import json
import os

from cognitive_cell.lego import CognitiveCellRequest, CognitiveCellV9


def main() -> int:
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set.")
        print("Run the import-only demo instead:")
        print("python examples/v9_import_demo.py")
        return 1

    cell = CognitiveCellV9(
        model="gpt-4.1",
        selector_model="gpt-4.1",
        finalizer_model="gpt-4.1",
    )

    result = cell.run(
        CognitiveCellRequest(
            statement="Blue colour is observed.",
            interaction_mode="workflow_component",
            autonomy_mode="log",
        )
    )

    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

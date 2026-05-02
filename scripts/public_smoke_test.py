from __future__ import annotations

from cognitive_cell import CognitiveCellRequest, CognitiveCellV9
from cognitive_cell.server.app import app


def main() -> int:
    request = CognitiveCellRequest(statement="Blue colour is observed.")
    cell = CognitiveCellV9()

    print("Cognitive Cell import ok")
    print(request)
    print(cell)
    print("FastAPI app:", app.title)
    print("Smoke test passed. No model call was made.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass
class CognitiveCellRequest:
    statement: str
    context_snapshot: Dict[str, Any] | None = None
    metadata: Dict[str, Any] | None = None
    interaction_mode: str = "standalone_assistant"
    autonomy_mode: str = "suggest"


@dataclass
class CognitiveCellResponse:
    statement: str
    interaction_mode: str
    autonomy_mode: str
    response_text: str
    response_style: str
    selected_label: str
    selected_response_mode: str
    selected_next_step_type: str
    needs_approval: bool
    trace: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CognitiveCellV9:
    """
    Public-facing v9 API.

    Accepted architecture:

        router-v4 -> selector-v5 -> finalizer-v9

    This implementation uses a candidate-generation layer, selector-v5,
    and finalizer-v9 to return a final response plus trace.
    """

    def __init__(
        self,
        model: str = "gpt-4.1",
        selector_model: str = "gpt-4.1",
        finalizer_model: str = "gpt-4.1",
        client: Optional[Any] = None,
    ) -> None:
        self.model = model
        self.selector_model = selector_model
        self.finalizer_model = finalizer_model
        self.client = client

    def run(self, request: CognitiveCellRequest) -> CognitiveCellResponse:
        from cognitive_cell.lego.cell_v9 import run_cell_v9

        return run_cell_v9(
            request=request,
            model=self.model,
            selector_model=self.selector_model,
            finalizer_model=self.finalizer_model,
            client=self.client,
        )

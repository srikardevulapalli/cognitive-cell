from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from cognitive_cell.lego import CognitiveCellRequest, CognitiveCellResponse


@dataclass
class EnterpriseEvent:
    event_id: str
    source: str
    event_type: str
    statement: str
    context: Dict[str, Any]
    metadata: Dict[str, Any]
    interaction_mode: str = "workflow_component"
    autonomy_mode: str = "suggest"


def event_to_request(event: EnterpriseEvent) -> CognitiveCellRequest:
    return CognitiveCellRequest(
        statement=event.statement,
        context_snapshot={
            "world_facts": event.context.get("world_facts", []),
            "constraints": event.context.get("constraints", []),
            "active_goals": event.context.get("active_goals", []),
        },
        metadata=event.metadata,
        interaction_mode=event.interaction_mode,
        autonomy_mode=event.autonomy_mode,
    )


def response_to_enterprise_payload(
    *,
    event: EnterpriseEvent,
    response: CognitiveCellResponse,
) -> Dict[str, Any]:
    return {
        "event_id": event.event_id,
        "source": event.source,
        "event_type": event.event_type,
        "statement": event.statement,
        "response_text": response.response_text,
        "response_style": response.response_style,
        "selected_label": response.selected_label,
        "selected_response_mode": response.selected_response_mode,
        "selected_next_step_type": response.selected_next_step_type,
        "needs_approval": response.needs_approval,
        "trace": response.trace,
    }


def parse_enterprise_event(payload: Dict[str, Any]) -> EnterpriseEvent:
    return EnterpriseEvent(
        event_id=str(payload.get("event_id", "")),
        source=str(payload.get("source", "")),
        event_type=str(payload.get("event_type", "")),
        statement=str(payload.get("statement", "")),
        context=payload.get("context") or {
            "world_facts": [],
            "constraints": [],
            "active_goals": [],
        },
        metadata=payload.get("metadata") or {},
        interaction_mode=str(payload.get("interaction_mode", "workflow_component")),
        autonomy_mode=str(payload.get("autonomy_mode", "suggest")),
    )

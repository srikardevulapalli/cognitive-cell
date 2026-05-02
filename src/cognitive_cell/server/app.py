from __future__ import annotations

from typing import Any, Dict

from fastapi import FastAPI

from cognitive_cell.lego import (
    CognitiveCellV9,
    event_to_request,
    parse_enterprise_event,
    response_to_enterprise_payload,
)

app = FastAPI(title="Cognitive Cell v9 Sidecar")

cell = CognitiveCellV9()


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/sidecar")
def sidecar(payload: Dict[str, Any]) -> Dict[str, Any]:
    event = parse_enterprise_event(payload)
    request = event_to_request(event)
    response = cell.run(request)
    return response_to_enterprise_payload(event=event, response=response)

# API Reference

## CognitiveCellRequest

~~~python
CognitiveCellRequest(
    statement: str,
    context_snapshot: dict | None = None,
    metadata: dict | None = None,
    interaction_mode: str = "standalone_assistant",
    autonomy_mode: str = "suggest",
)
~~~

## CognitiveCellResponse

Returns:

~~~text
statement
interaction_mode
autonomy_mode
response_text
response_style
selected_label
selected_response_mode
selected_next_step_type
needs_approval
trace
~~~

## EnterpriseEvent

~~~python
EnterpriseEvent(
    event_id: str,
    source: str,
    event_type: str,
    statement: str,
    context: dict,
    metadata: dict,
    interaction_mode: str = "workflow_component",
    autonomy_mode: str = "suggest",
)
~~~

## HTTP endpoints

### GET /health

No model call.

Returns:

~~~json
{"status":"ok"}
~~~

### POST /v1/sidecar

Accepts an enterprise event payload.

Returns final response, selected mode, next step type, approval flag, and trace.

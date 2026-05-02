from cognitive_cell.lego import (
    EnterpriseEvent,
    event_to_request,
    parse_enterprise_event,
    response_to_enterprise_payload,
    CognitiveCellResponse,
)


def test_parse_enterprise_event():
    payload = {
        "event_id": "evt_1",
        "source": "test",
        "event_type": "metric_anomaly",
        "statement": "Refund requests doubled.",
        "context": {
            "world_facts": [],
            "constraints": ["Prioritize high-signal checks."],
            "active_goals": ["find first step"],
        },
        "metadata": {"persona": "ops analyst"},
        "interaction_mode": "workflow_component",
        "autonomy_mode": "suggest",
    }

    event = parse_enterprise_event(payload)
    assert event.event_id == "evt_1"
    assert event.statement == "Refund requests doubled."


def test_event_to_request():
    event = EnterpriseEvent(
        event_id="evt_1",
        source="test",
        event_type="metric_anomaly",
        statement="Refund requests doubled.",
        context={
            "world_facts": [],
            "constraints": ["Prioritize high-signal checks."],
            "active_goals": ["find first step"],
        },
        metadata={"persona": "ops analyst"},
    )

    request = event_to_request(event)
    assert request.statement == event.statement
    assert request.interaction_mode == "workflow_component"
    assert request.autonomy_mode == "suggest"


def test_response_to_enterprise_payload():
    event = EnterpriseEvent(
        event_id="evt_1",
        source="test",
        event_type="metric_anomaly",
        statement="Refund requests doubled.",
        context={"world_facts": [], "constraints": [], "active_goals": []},
        metadata={},
    )

    response = CognitiveCellResponse(
        statement=event.statement,
        interaction_mode="workflow_component",
        autonomy_mode="suggest",
        response_text="Start with the change log.",
        response_style="direct_answer",
        selected_label="direct",
        selected_response_mode="direct_answer",
        selected_next_step_type="answer",
        needs_approval=False,
        trace={"ok": True},
    )

    payload = response_to_enterprise_payload(event=event, response=response)
    assert payload["event_id"] == "evt_1"
    assert payload["response_text"] == "Start with the change log."
    assert payload["trace"]["ok"] is True

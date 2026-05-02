from cognitive_cell.lego import CognitiveCellRequest, CognitiveCellResponse, CognitiveCellV9


def test_request_defaults():
    request = CognitiveCellRequest(statement="Blue colour is observed.")
    assert request.statement == "Blue colour is observed."
    assert request.interaction_mode == "standalone_assistant"
    assert request.autonomy_mode == "suggest"


def test_response_to_dict():
    response = CognitiveCellResponse(
        statement="x",
        interaction_mode="standalone_assistant",
        autonomy_mode="suggest",
        response_text="answer",
        response_style="direct_answer",
        selected_label="direct",
        selected_response_mode="direct_answer",
        selected_next_step_type="answer",
        needs_approval=False,
        trace={},
    )
    assert response.to_dict()["response_text"] == "answer"


def test_cell_class_exists():
    cell = CognitiveCellV9()
    assert cell.model

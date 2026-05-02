from __future__ import annotations

import json
from typing import Any, Dict, Optional

from openai import OpenAI

from cognitive_cell.lego.selector_v5 import select_candidate
from cognitive_cell.lego.finalizer_v9 import render_final_response
from cognitive_cell.lego.v9_api import CognitiveCellRequest, CognitiveCellResponse


CANDIDATE_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "stakes",
        "ambiguity",
        "context_sufficiency",
        "personalization_need",
        "temporal_sensitivity",
        "actionability",
        "plan_horizon",
        "observation_purity",
        "analysis_need",
        "external_effect",
        "factor_rationale",
        "response_mode",
        "next_step_type",
        "focus_object",
        "why_now",
        "needs_approval",
        "policy_reason",
        "workflow_artifact_json",
        "direct_artifact_json",
    ],
    "properties": {
        "stakes": {"type": "number"},
        "ambiguity": {"type": "number"},
        "context_sufficiency": {"type": "number"},
        "personalization_need": {"type": "number"},
        "temporal_sensitivity": {"type": "number"},
        "actionability": {"type": "number"},
        "plan_horizon": {"type": "number"},
        "observation_purity": {"type": "number"},
        "analysis_need": {"type": "number"},
        "external_effect": {"type": "number"},
        "factor_rationale": {"type": "string"},
        "response_mode": {
            "type": "string",
            "enum": [
                "observe_record",
                "clarify",
                "analyze",
                "plan",
                "direct_answer",
                "escalate",
            ],
        },
        "next_step_type": {"type": "string"},
        "focus_object": {"type": "string"},
        "why_now": {"type": "string"},
        "needs_approval": {"type": "boolean"},
        "policy_reason": {"type": "string"},
        "workflow_artifact_json": {
            "type": "string",
            "description": "A valid JSON object encoded as a string. This is the workflow-style candidate artifact.",
        },
        "direct_artifact_json": {
            "type": "string",
            "description": "A valid JSON object encoded as a string. This is the direct-answer candidate artifact.",
        },
    },
}


CANDIDATE_SYSTEM_PROMPT = """You are the candidate-generation layer for Cognitive Cell v9.

You receive:
- user statement
- context snapshot
- metadata
- interaction mode
- autonomy mode

Generate:
1. context factors,
2. a workflow-style decision,
3. a workflow artifact encoded as a JSON string,
4. a direct-answer artifact encoded as a JSON string,
5. a policy reason.

Important behavior:
- If interaction_mode is workflow_component and autonomy_mode is log, favor observe_record unless context clearly implies urgent safety/action.
- If the request is simple writing, tutoring, everyday help, or explanation, direct_answer is often useful.
- If context has high urgency, safety, medical, privacy, operational risk, or time pressure, lead toward immediate action.
- If the task is broad planning/design, produce a structured plan.
- If context is insufficient and the answer would be irresponsible, clarify.
- Do not claim external facts beyond the provided context unless they are general common sense.
- The workflow artifact should be structured and traceable.
- The direct artifact should be the strongest direct response a user would want immediately.

Artifact encoding rule:
- workflow_artifact_json must be a JSON object encoded as a string.
- direct_artifact_json must be a JSON object encoded as a string.
- Do not use Markdown fences inside those strings.

Example workflow_artifact_json:
{"record_type":"observation_record","observed_object":"window","observed_state":"frost visible","confidence_note":"visual observation","missing_context":[]}

Example direct_artifact_json:
{"answer_type":"answer","answer":"The strongest direct answer goes here.","assumptions":[],"caveats":[],"followup_options":[]}

Return only JSON matching the schema.
"""


def _client(client: Optional[Any]) -> Any:
    return client if client is not None else OpenAI()


def _default_context(context_snapshot: Dict[str, Any] | None) -> Dict[str, Any]:
    return context_snapshot or {
        "world_facts": [],
        "constraints": [],
        "active_goals": [],
    }


def _clamp01(value: Any, default: float = 0.0) -> float:
    try:
        x = float(value)
    except Exception:
        x = default
    return max(0.0, min(1.0, x))


def _parse_artifact_json(value: Any, fallback: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value

    if not isinstance(value, str) or not value.strip():
        return fallback

    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return {
            **fallback,
            "raw_unparsed_artifact": value,
        }

    if not isinstance(parsed, dict):
        return {
            **fallback,
            "raw_unparsed_artifact": value,
        }

    return parsed


def _context_is_empty(context_snapshot: Dict[str, Any]) -> bool:
    return not (
        context_snapshot.get("world_facts")
        or context_snapshot.get("constraints")
        or context_snapshot.get("active_goals")
    )


def _normalize_decision(decision: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize runtime labels to the v9 contract."""
    response_mode = decision.get("response_mode", "")

    if response_mode == "observe_record":
        decision["next_step_type"] = "observation_record"
    elif response_mode == "direct_answer":
        decision["next_step_type"] = "answer"
    elif response_mode == "plan" and not decision.get("next_step_type"):
        decision["next_step_type"] = "plan_outline"
    elif response_mode == "analyze" and not decision.get("next_step_type"):
        decision["next_step_type"] = "analysis_brief"
    elif response_mode == "clarify" and not decision.get("next_step_type"):
        decision["next_step_type"] = "question"

    return decision


def _calibrate_factors(
    *,
    request: CognitiveCellRequest,
    factors: Dict[str, Any],
    decision: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Repair obviously miscalibrated runtime factors.

    This is not a domain rule. It is a posture-level calibration so traces
    remain faithful to the v9 evaluation contract.
    """
    calibrated = dict(factors)
    context = _default_context(request.context_snapshot)

    is_log_observation = (
        request.interaction_mode == "workflow_component"
        and request.autonomy_mode == "log"
        and decision.get("response_mode") == "observe_record"
        and _context_is_empty(context)
    )

    if is_log_observation:
        calibrated.update(
            {
                "stakes": min(float(calibrated.get("stakes", 0.35)), 0.35),
                "ambiguity": min(float(calibrated.get("ambiguity", 0.3)), 0.3),
                "context_sufficiency": min(float(calibrated.get("context_sufficiency", 0.4)), 0.4),
                "personalization_need": min(float(calibrated.get("personalization_need", 0.2)), 0.2),
                "temporal_sensitivity": min(float(calibrated.get("temporal_sensitivity", 0.2)), 0.2),
                "actionability": min(float(calibrated.get("actionability", 0.3)), 0.3),
                "plan_horizon": min(float(calibrated.get("plan_horizon", 0.2)), 0.2),
                "observation_purity": max(float(calibrated.get("observation_purity", 1.0)), 0.9),
                "analysis_need": min(float(calibrated.get("analysis_need", 0.3)), 0.3),
                "external_effect": min(float(calibrated.get("external_effect", 0.2)), 0.2),
            }
        )

    calibrated["rationale"] = str(calibrated.get("rationale", ""))

    return calibrated


def _generate_candidates(
    *,
    request: CognitiveCellRequest,
    model: str,
    client: Any,
) -> Dict[str, Any]:
    payload = {
        "statement": request.statement,
        "context_snapshot": _default_context(request.context_snapshot),
        "metadata": request.metadata or {},
        "interaction_mode": request.interaction_mode,
        "autonomy_mode": request.autonomy_mode,
    }

    response = client.responses.create(
        model=model,
        store=False,
        input=[
            {
                "role": "system",
                "content": [{"type": "input_text", "text": CANDIDATE_SYSTEM_PROMPT}],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": json.dumps(payload, ensure_ascii=False, indent=2),
                    }
                ],
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "cognitive_cell_candidates",
                "schema": CANDIDATE_SCHEMA,
                "strict": True,
            }
        },
    )

    raw = getattr(response, "output_text", None)
    if not raw:
        raise RuntimeError("Candidate generation returned no output_text.")

    flat = json.loads(raw)

    factors = {
        "stakes": _clamp01(flat.get("stakes")),
        "ambiguity": _clamp01(flat.get("ambiguity")),
        "context_sufficiency": _clamp01(flat.get("context_sufficiency")),
        "personalization_need": _clamp01(flat.get("personalization_need")),
        "temporal_sensitivity": _clamp01(flat.get("temporal_sensitivity")),
        "actionability": _clamp01(flat.get("actionability")),
        "plan_horizon": _clamp01(flat.get("plan_horizon")),
        "observation_purity": _clamp01(flat.get("observation_purity")),
        "analysis_need": _clamp01(flat.get("analysis_need")),
        "external_effect": _clamp01(flat.get("external_effect")),
        "rationale": str(flat.get("factor_rationale", "")),
    }

    decision = _normalize_decision(
        {
            "response_mode": flat["response_mode"],
            "next_step_type": flat["next_step_type"],
            "focus_object": flat["focus_object"],
            "why_now": flat["why_now"],
            "needs_approval": bool(flat["needs_approval"]),
        }
    )

    factors = _calibrate_factors(
        request=request,
        factors=factors,
        decision=decision,
    )

    workflow_artifact = _parse_artifact_json(
        flat.get("workflow_artifact_json"),
        fallback={
            "artifact_type": "workflow",
            "content": "",
        },
    )

    direct_artifact = _parse_artifact_json(
        flat.get("direct_artifact_json"),
        fallback={
            "answer_type": "answer",
            "answer": "",
            "assumptions": [],
            "caveats": [],
            "followup_options": [],
        },
    )

    return {
        "factors": factors,
        "decision": decision,
        "workflow_artifact": workflow_artifact,
        "direct_artifact": direct_artifact,
        "policy_reason": str(flat.get("policy_reason", "")),
    }


def _selected_response_mode(row: Dict[str, Any], selected_label: str) -> str:
    if selected_label == "workflow":
        return row.get("pred_response_mode", "")
    return "direct_answer"


def _selected_next_step_type(row: Dict[str, Any], selected_label: str) -> str:
    if selected_label == "workflow":
        return row.get("pred_next_step_type", "")
    return "answer"


def _selected_artifact(row: Dict[str, Any], selected_label: str) -> Dict[str, Any]:
    if selected_label == "workflow":
        return row.get("workflow_artifact", {})
    return row.get("direct_artifact", {})



def _deep_parse_artifacts(value: Any) -> Any:
    """
    Recursively remove raw_unparsed_artifact when it contains valid JSON.
    Handles single-encoded and double-encoded JSON strings.
    """
    if isinstance(value, dict):
        if "raw_unparsed_artifact" in value:
            raw = value.get("raw_unparsed_artifact")
            current = raw
            for _ in range(3):
                if not isinstance(current, str):
                    break
                try:
                    parsed = json.loads(current)
                except Exception:
                    break
                if isinstance(parsed, dict):
                    return _deep_parse_artifacts(parsed)
                if isinstance(parsed, str):
                    current = parsed
                    continue
                break

        return {k: _deep_parse_artifacts(v) for k, v in value.items()}

    if isinstance(value, list):
        return [_deep_parse_artifacts(v) for v in value]

    return value


def _runtime_context_blob(request: CognitiveCellRequest) -> str:
    return json.dumps(
        {
            "statement": request.statement,
            "context_snapshot": _default_context(request.context_snapshot),
            "metadata": request.metadata or {},
            "interaction_mode": request.interaction_mode,
            "autonomy_mode": request.autonomy_mode,
        },
        ensure_ascii=False,
    ).lower()


def _runtime_context_empty(request: CognitiveCellRequest) -> bool:
    context = _default_context(request.context_snapshot)
    return not (
        context.get("world_facts")
        or context.get("constraints")
        or context.get("active_goals")
    )


def _runtime_high_time_pressure(request: CognitiveCellRequest) -> bool:
    metadata = request.metadata or {}
    value = str(metadata.get("time_pressure", "")).lower().strip()
    return value in {"high", "urgent", "critical", "immediate"}


def _runtime_urgent_or_safety(request: CognitiveCellRequest) -> bool:
    blob = _runtime_context_blob(request)
    markers = [
        "urgent",
        "immediate",
        "safety",
        "medical",
        "medication",
        "patient",
        "child",
        "privacy",
        "fire",
        "smoke",
        "temperature-sensitive",
        "in transit",
        "danger",
        "emergency",
        "reliability",
    ]
    return _runtime_high_time_pressure(request) or any(m in blob for m in markers)


def _runtime_degenerate_factors(factors: Dict[str, Any]) -> bool:
    keys = [
        "stakes",
        "ambiguity",
        "context_sufficiency",
        "personalization_need",
        "temporal_sensitivity",
        "actionability",
        "plan_horizon",
        "observation_purity",
        "analysis_need",
        "external_effect",
    ]

    values = []
    for key in keys:
        try:
            values.append(float(factors.get(key, 0.0)))
        except Exception:
            values.append(0.0)

    return (
        sum(v >= 0.95 for v in values) >= 7
        or sum(v <= 0.05 for v in values) >= 7
    )


def _runtime_default_factors(
    *,
    request: CognitiveCellRequest,
    decision: Dict[str, Any],
) -> Dict[str, float]:
    response_mode = decision.get("response_mode", "")
    context_empty = _runtime_context_empty(request)

    if (
        request.interaction_mode == "workflow_component"
        and request.autonomy_mode == "log"
        and response_mode == "observe_record"
    ):
        return {
            "stakes": 0.35,
            "ambiguity": 0.30,
            "context_sufficiency": 0.40,
            "personalization_need": 0.20,
            "temporal_sensitivity": 0.20,
            "actionability": 0.30,
            "plan_horizon": 0.20,
            "observation_purity": 1.00,
            "analysis_need": 0.30,
            "external_effect": 0.20,
        }

    if _runtime_urgent_or_safety(request):
        return {
            "stakes": 0.85,
            "ambiguity": 0.45,
            "context_sufficiency": 0.75 if not context_empty else 0.45,
            "personalization_need": 0.50,
            "temporal_sensitivity": 0.90,
            "actionability": 0.90,
            "plan_horizon": 0.35,
            "observation_purity": 0.45,
            "analysis_need": 0.65,
            "external_effect": 0.75,
        }

    if response_mode == "plan":
        return {
            "stakes": 0.55,
            "ambiguity": 0.60,
            "context_sufficiency": 0.75 if not context_empty else 0.45,
            "personalization_need": 0.55,
            "temporal_sensitivity": 0.35,
            "actionability": 0.80,
            "plan_horizon": 0.75,
            "observation_purity": 0.20,
            "analysis_need": 0.45,
            "external_effect": 0.45,
        }

    if request.interaction_mode == "workflow_component" and request.autonomy_mode == "suggest":
        return {
            "stakes": 0.65,
            "ambiguity": 0.50,
            "context_sufficiency": 0.75 if not context_empty else 0.55,
            "personalization_need": 0.35,
            "temporal_sensitivity": 0.55,
            "actionability": 0.80,
            "plan_horizon": 0.50,
            "observation_purity": 0.55,
            "analysis_need": 0.75,
            "external_effect": 0.60,
        }

    if response_mode == "direct_answer":
        return {
            "stakes": 0.40,
            "ambiguity": 0.35,
            "context_sufficiency": 0.75 if not context_empty else 0.45,
            "personalization_need": 0.45,
            "temporal_sensitivity": 0.35,
            "actionability": 0.70,
            "plan_horizon": 0.35,
            "observation_purity": 0.30,
            "analysis_need": 0.30,
            "external_effect": 0.30,
        }

    return {
        "stakes": 0.50,
        "ambiguity": 0.50,
        "context_sufficiency": 0.75 if not context_empty else 0.50,
        "personalization_need": 0.40,
        "temporal_sensitivity": 0.40,
        "actionability": 0.60,
        "plan_horizon": 0.40,
        "observation_purity": 0.40,
        "analysis_need": 0.50,
        "external_effect": 0.40,
    }


def _runtime_sanitize_candidate_bundle(
    *,
    request: CognitiveCellRequest,
    candidate_bundle: Dict[str, Any],
) -> Dict[str, Any]:
    sanitized = dict(candidate_bundle)

    decision = dict(sanitized.get("decision", {}))
    decision = _normalize_decision(decision)
    sanitized["decision"] = decision

    factors = dict(sanitized.get("factors", {}))

    if _runtime_degenerate_factors(factors):
        defaults = _runtime_default_factors(request=request, decision=decision)
        rationale = str(factors.get("rationale", "")).strip()
        if rationale:
            rationale = (
                rationale
                + " Runtime factor values were recalibrated because the raw model output was degenerate."
            )
        else:
            rationale = "Runtime factor values were recalibrated because the raw model output was degenerate."
        factors = {**defaults, "rationale": rationale}
    else:
        for key in [
            "stakes",
            "ambiguity",
            "context_sufficiency",
            "personalization_need",
            "temporal_sensitivity",
            "actionability",
            "plan_horizon",
            "observation_purity",
            "analysis_need",
            "external_effect",
        ]:
            factors[key] = _clamp01(factors.get(key, 0.0))
        factors["rationale"] = str(factors.get("rationale", ""))

    sanitized["factors"] = factors
    sanitized["workflow_artifact"] = _deep_parse_artifacts(sanitized.get("workflow_artifact", {}))
    sanitized["direct_artifact"] = _deep_parse_artifacts(sanitized.get("direct_artifact", {}))

    return sanitized



def _release_deep_parse_artifacts(value: Any) -> Any:
    """
    Recursively remove raw_unparsed_artifact when it contains valid JSON.
    Handles single-encoded and double-encoded JSON strings.
    """
    if isinstance(value, dict):
        if "raw_unparsed_artifact" in value:
            raw = value.get("raw_unparsed_artifact")
            current = raw

            for _ in range(3):
                if not isinstance(current, str):
                    break
                try:
                    parsed = json.loads(current)
                except Exception:
                    break

                if isinstance(parsed, dict):
                    return _release_deep_parse_artifacts(parsed)

                if isinstance(parsed, str):
                    current = parsed
                    continue

                break

            cleaned = {
                k: _release_deep_parse_artifacts(v)
                for k, v in value.items()
                if k != "raw_unparsed_artifact"
            }
            return cleaned

        return {k: _release_deep_parse_artifacts(v) for k, v in value.items()}

    if isinstance(value, list):
        return [_release_deep_parse_artifacts(v) for v in value]

    return value


def _release_context_empty(request: CognitiveCellRequest) -> bool:
    context = _default_context(request.context_snapshot)
    return not (
        context.get("world_facts")
        or context.get("constraints")
        or context.get("active_goals")
    )


def _release_context_blob(request: CognitiveCellRequest) -> str:
    return json.dumps(
        {
            "statement": request.statement,
            "context_snapshot": _default_context(request.context_snapshot),
            "metadata": request.metadata or {},
            "interaction_mode": request.interaction_mode,
            "autonomy_mode": request.autonomy_mode,
        },
        ensure_ascii=False,
    ).lower()


def _release_high_time_pressure(request: CognitiveCellRequest) -> bool:
    metadata = request.metadata or {}
    value = str(metadata.get("time_pressure", "")).lower().strip()
    return value in {"high", "urgent", "critical", "immediate"}


def _release_urgent_or_safety(request: CognitiveCellRequest) -> bool:
    blob = _release_context_blob(request)
    markers = [
        "urgent",
        "immediate",
        "safety",
        "medical",
        "medication",
        "patient",
        "child",
        "privacy",
        "fire",
        "smoke",
        "temperature-sensitive",
        "in transit",
        "danger",
        "emergency",
        "reliability",
    ]
    return _release_high_time_pressure(request) or any(marker in blob for marker in markers)


def _release_degenerate_factors(factors: Dict[str, Any]) -> bool:
    keys = [
        "stakes",
        "ambiguity",
        "context_sufficiency",
        "personalization_need",
        "temporal_sensitivity",
        "actionability",
        "plan_horizon",
        "observation_purity",
        "analysis_need",
        "external_effect",
    ]

    values = []
    for key in keys:
        try:
            values.append(float(factors.get(key, 0.0)))
        except Exception:
            values.append(0.0)

    return (
        sum(v >= 0.95 for v in values) >= 7
        or sum(v <= 0.05 for v in values) >= 7
    )


def _release_default_factors(
    *,
    request: CognitiveCellRequest,
    decision: Dict[str, Any],
) -> Dict[str, float]:
    response_mode = decision.get("response_mode", "")
    context_empty = _release_context_empty(request)

    if (
        request.interaction_mode == "workflow_component"
        and request.autonomy_mode == "log"
        and response_mode == "observe_record"
    ):
        return {
            "stakes": 0.35,
            "ambiguity": 0.30,
            "context_sufficiency": 0.40,
            "personalization_need": 0.20,
            "temporal_sensitivity": 0.20,
            "actionability": 0.30,
            "plan_horizon": 0.20,
            "observation_purity": 1.00,
            "analysis_need": 0.30,
            "external_effect": 0.20,
        }

    if _release_urgent_or_safety(request):
        return {
            "stakes": 0.85,
            "ambiguity": 0.45,
            "context_sufficiency": 0.75 if not context_empty else 0.45,
            "personalization_need": 0.50,
            "temporal_sensitivity": 0.90,
            "actionability": 0.90,
            "plan_horizon": 0.35,
            "observation_purity": 0.45,
            "analysis_need": 0.65,
            "external_effect": 0.75,
        }

    if response_mode == "plan":
        return {
            "stakes": 0.55,
            "ambiguity": 0.60,
            "context_sufficiency": 0.75 if not context_empty else 0.45,
            "personalization_need": 0.55,
            "temporal_sensitivity": 0.35,
            "actionability": 0.80,
            "plan_horizon": 0.75,
            "observation_purity": 0.20,
            "analysis_need": 0.45,
            "external_effect": 0.45,
        }

    if request.interaction_mode == "workflow_component" and request.autonomy_mode == "suggest":
        return {
            "stakes": 0.65,
            "ambiguity": 0.50,
            "context_sufficiency": 0.75 if not context_empty else 0.55,
            "personalization_need": 0.35,
            "temporal_sensitivity": 0.55,
            "actionability": 0.80,
            "plan_horizon": 0.50,
            "observation_purity": 0.55,
            "analysis_need": 0.75,
            "external_effect": 0.60,
        }

    if response_mode == "direct_answer":
        return {
            "stakes": 0.40,
            "ambiguity": 0.35,
            "context_sufficiency": 0.75 if not context_empty else 0.45,
            "personalization_need": 0.45,
            "temporal_sensitivity": 0.35,
            "actionability": 0.70,
            "plan_horizon": 0.35,
            "observation_purity": 0.30,
            "analysis_need": 0.30,
            "external_effect": 0.30,
        }

    return {
        "stakes": 0.50,
        "ambiguity": 0.50,
        "context_sufficiency": 0.75 if not context_empty else 0.50,
        "personalization_need": 0.40,
        "temporal_sensitivity": 0.40,
        "actionability": 0.60,
        "plan_horizon": 0.40,
        "observation_purity": 0.40,
        "analysis_need": 0.50,
        "external_effect": 0.40,
    }


def _release_sanitize_candidate_bundle(
    *,
    request: CognitiveCellRequest,
    candidate_bundle: Dict[str, Any],
) -> Dict[str, Any]:
    sanitized = dict(candidate_bundle)

    decision = dict(sanitized.get("decision", {}))
    decision = _normalize_decision(decision)
    sanitized["decision"] = decision

    factors = dict(sanitized.get("factors", {}))

    if _release_degenerate_factors(factors):
        defaults = _release_default_factors(request=request, decision=decision)
        raw_rationale = str(factors.get("rationale", "")).strip()
        if raw_rationale:
            rationale = raw_rationale + " Runtime factor values were recalibrated because the raw model output was degenerate."
        else:
            rationale = "Runtime factor values were recalibrated because the raw model output was degenerate."
        factors = {**defaults, "rationale": rationale}
    else:
        for key in [
            "stakes",
            "ambiguity",
            "context_sufficiency",
            "personalization_need",
            "temporal_sensitivity",
            "actionability",
            "plan_horizon",
            "observation_purity",
            "analysis_need",
            "external_effect",
        ]:
            factors[key] = _clamp01(factors.get(key, 0.0))
        factors["rationale"] = str(factors.get("rationale", ""))

    sanitized["factors"] = factors
    sanitized["workflow_artifact"] = _release_deep_parse_artifacts(sanitized.get("workflow_artifact", {}))
    sanitized["direct_artifact"] = _release_deep_parse_artifacts(sanitized.get("direct_artifact", {}))

    return sanitized


def run_cell_v9(
    *,
    request: CognitiveCellRequest,
    model: str = "gpt-4.1",
    selector_model: str = "gpt-4.1",
    finalizer_model: str = "gpt-4.1",
    client: Optional[Any] = None,
) -> CognitiveCellResponse:
    openai_client = _client(client)

    candidate_bundle = _generate_candidates(
        request=request,
        model=model,
        client=openai_client,
    )

    candidate_bundle = _release_sanitize_candidate_bundle(
        request=request,
        candidate_bundle=candidate_bundle,
    )

    candidate_bundle = _runtime_sanitize_candidate_bundle(
        request=request,
        candidate_bundle=candidate_bundle,
    )

    decision = candidate_bundle["decision"]

    row: Dict[str, Any] = {
        "case_id": "runtime_request",
        "family": "runtime",
        "statement": request.statement,
        "interaction_mode": request.interaction_mode,
        "autonomy_mode": request.autonomy_mode,
        "context_snapshot": _default_context(request.context_snapshot),
        "metadata": request.metadata or {},
        "factors": candidate_bundle["factors"],
        "decision": decision,
        "pred_response_mode": decision["response_mode"],
        "pred_next_step_type": decision["next_step_type"],
        "workflow_artifact": candidate_bundle["workflow_artifact"],
        "direct_artifact": candidate_bundle["direct_artifact"],
        "policy_reason": candidate_bundle["policy_reason"],
    }

    selection = select_candidate(
        client=openai_client,
        model=selector_model,
        row=row,
    )

    selected_label = selection["selected_label"]
    selected_response_mode = _selected_response_mode(row, selected_label)
    selected_next_step_type = _selected_next_step_type(row, selected_label)
    selected_artifact = _selected_artifact(row, selected_label)

    selected_row = dict(row)
    selected_row.update(
        {
            "selected_label": selected_label,
            "selected_response_mode": selected_response_mode,
            "selected_next_step_type": selected_next_step_type,
            "selected_artifact": selected_artifact,
            "selector_reason": selection.get("reason", ""),
            "selector_confidence": selection.get("confidence", 0.0),
        }
    )

    final_response = render_final_response(
        client=openai_client,
        model=finalizer_model,
        row=selected_row,
    )

    trace = {
        "factors": candidate_bundle["factors"],
        "decision": decision,
        "policy_reason": candidate_bundle["policy_reason"],
        "workflow_artifact": candidate_bundle["workflow_artifact"],
        "direct_artifact": candidate_bundle["direct_artifact"],
        "selection": selection,
        "final_response": final_response,
    }

    return CognitiveCellResponse(
        statement=request.statement,
        interaction_mode=request.interaction_mode,
        autonomy_mode=request.autonomy_mode,
        response_text=final_response["final_response_text"],
        response_style=final_response["response_style"],
        selected_label=selected_label,
        selected_response_mode=selected_response_mode,
        selected_next_step_type=selected_next_step_type,
        needs_approval=bool(decision.get("needs_approval", False)),
        trace=trace,
    )

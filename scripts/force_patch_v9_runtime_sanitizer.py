from __future__ import annotations

import re
from pathlib import Path


p = Path("src/cognitive_cell/lego/cell_v9.py")
text = p.read_text(encoding="utf-8")


helper = r'''
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
'''


if "_release_sanitize_candidate_bundle" not in text:
    marker = "\ndef run_cell_v9("
    if marker not in text:
        raise SystemExit("Could not find run_cell_v9 marker.")
    text = text.replace(marker, "\n" + helper + "\n" + marker)


candidate_block = """    candidate_bundle = _generate_candidates(
        request=request,
        model=model,
        client=openai_client,
    )
"""

sanitized_block = """    candidate_bundle = _generate_candidates(
        request=request,
        model=model,
        client=openai_client,
    )

    candidate_bundle = _release_sanitize_candidate_bundle(
        request=request,
        candidate_bundle=candidate_bundle,
    )
"""

if "_release_sanitize_candidate_bundle(\n        request=request,\n        candidate_bundle=candidate_bundle" not in text:
    if candidate_block not in text:
        raise SystemExit("Could not find candidate_bundle generation block.")
    text = text.replace(candidate_block, sanitized_block, 1)


p.write_text(text, encoding="utf-8")
print("Applied forced v9 runtime sanitizer patch.")

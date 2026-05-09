# Cognitive Cell

[![PyPI version](https://img.shields.io/pypi/v/cognitive-cell.svg)](https://pypi.org/project/cognitive-cell/)
[![Python versions](https://img.shields.io/pypi/pyversions/cognitive-cell.svg)](https://pypi.org/project/cognitive-cell/)

Cognitive Cell is a context-sensitive control stack for workflow AI.

Accepted v9 stack:

~~~text
router-v4 → selector-v5 → finalizer-v9
~~~

## What it does

The system separates:

~~~text
1. cognitive routing
2. workflow-vs-direct pathway selection
3. final user-facing rendering
~~~

This lets the same input behave differently depending on context, posture, urgency, role, and workflow constraints.

## Install

~~~bash
pip install "cognitive-cell[server]"
~~~

## Python usage

~~~python
from cognitive_cell import CognitiveCellRequest, CognitiveCellV9

cell = CognitiveCellV9()

request = CognitiveCellRequest(
    statement="Blue colour is observed.",
    interaction_mode="workflow_component",
    autonomy_mode="log",
)

result = cell.run(request)

print(result.response_text)
print(result.trace)
~~~

## CLI usage

Create an event JSON file, then run:

~~~bash
cognitive-cell --event-json examples/event.example.json
~~~

This calls the configured model and may incur API cost.

## HTTP sidecar usage

Start the server:

~~~bash
python -m uvicorn cognitive_cell.server.app:app --port 8000
~~~

Check health without model calls:

~~~bash
curl -s http://127.0.0.1:8000/health
~~~

Send an enterprise event:

~~~bash
curl -s -X POST http://127.0.0.1:8000/v1/sidecar \
  -H "Content-Type: application/json" \
  -d @examples/event.example.json
~~~

## Example event

~~~json
{
  "event_id": "evt_pricing_refunds_001",
  "source": "growth_ops_monitor",
  "event_type": "metric_anomaly",
  "statement": "Refund requests doubled after the pricing page update. What should we examine first?",
  "context": {
    "world_facts": [],
    "constraints": ["Prioritize high-signal first checks before broad analysis."],
    "active_goals": ["identify the first diagnostic step"]
  },
  "metadata": {
    "persona": "growth operations analyst",
    "time_pressure": "medium"
  },
  "interaction_mode": "workflow_component",
  "autonomy_mode": "suggest"
}
~~~

## Current evidence

Fresh holdout-v1, 100 cases:

| Judge | Architecture preference | Baseline preference |
|---|---:|---:|
| gpt-4.1 primary | 0.6200 | 0.3800 |
| gpt-5.5 second, combined 40+60 | 0.5575 | 0.4425 |
| Two-judge mean | 0.58875 | 0.41125 |

Safe claim:

> On a fresh 100-case holdout, the frozen v9 cognitive-cell stack beat a plain strong-model baseline under two standardized OpenAI judges, with mean architecture preference around 0.589.

## Caution

This is an engineering validation result, not a universal claim of superiority over frontier models. Larger benchmarks, human evaluation, ablations, and cross-provider validation are still needed.

## Cost note

`/health` costs nothing.

`/v1/sidecar` and `cognitive-cell --event-json ...` call the configured model and may incur API cost.

## Recommended production posture

Start with:

~~~text
autonomy_mode = "suggest"
human-in-the-loop
no automatic external action execution
~~~

## Known weaknesses

- Atomic observation remains weaker because pure logging competes against advice/explanation.
- Contextual observation remains mixed when direct action beats record/analyze behavior.
- Persona shift is weaker under the second judge.
- Writing support is improved but not consistently superior.

## What this is not

Cognitive Cell is not AGI, not a production-autonomous agent, and not a claim of universal superiority over frontier models.

It is a workflow-control layer that helps decide whether to record, clarify, analyze, plan, answer directly, or escalate.

## Enterprise sidecar pilot

Cognitive Cell v9 passed a 100-event enterprise sidecar pilot across:

- growth/product analytics
- support/operations
- data-pipeline reliability
- risk/compliance
- operations/process workflows

Pilot result:

| Metric | Result |
|---|---:|
| Useful first move | 1.00 |
| Too vague | 0.00 |
| Unsafe or overreaching | 0.00 |
| Trace useful | 1.00 |

See: `docs/PILOT_100_REPORT.md`

Caution: this is a curated pilot result, not a claim of universal superiority.

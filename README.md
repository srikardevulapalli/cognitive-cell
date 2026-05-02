# Cognitive Cell

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

## Current evidence

Fresh holdout-v1, 100 cases:

| Judge | Architecture preference | Baseline preference |
|---|---:|---:|
| gpt-4.1 primary | 0.6200 | 0.3800 |
| gpt-5.5 second, combined 40+60 | 0.5575 | 0.4425 |
| Two-judge mean | 0.58875 | 0.41125 |

Safe claim:

> On a fresh 100-case holdout, the frozen v9 cognitive-cell stack beat a plain strong-model baseline under two standardized Op judges, with mean architecture preference around 0.589.

## Caution

This is an engineering validation result, not a universal claim of superiority over frontier models. Larger benchmarks, human evaluation, ablations, and cross-provider validation are still needed.

## Install

~~~bash
pip install -e .
~~~

## Planned usage

~~~python
from cognitive_cell.lego import CognitiveCellV9, CognitiveCellRequest

cell = CognitiveCellV9()

result = cell.run(
    CognitiveCellRequest(
        statement="The package label shows the wrong city.",
        context_snapshot={
            "world_facts": [
                {
                    "fact_id": "f1",
                    "fact_type": "world_fact",
                    "fact_text": "The package has not left the warehouse yet.",
                }
            ],
            "constraints": ["Optimize for low-cost correction."],
            "active_goals": ["determine the first operational step"],
        },
        metadata={"persona": "ops analyst", "time_pressure": "medium"},
        interaction_mode="workflow_component",
        autonomy_mode="suggest",
    )
)

print(result.response_text)
print(result.trace)
~~~

## Known weaknesses

- Atomic observation remains weaker because pure logging competes against advice/explanation.
- Contextual observation remains mixed when direct action beats record/analyze behavior.
- Persona shift is weaker under the second judge.
- Writing support is improved but not consistently superior.

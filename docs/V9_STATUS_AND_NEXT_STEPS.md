# Cognitive Cell v9 — Status and Next Steps

## Accepted stack

~~~text
router-v4 → selector-v5 → finalizer-v9
~~~

## Current validation

Fresh holdout-v1, 100 cases:

| Judge | Architecture preference | 95% CI |
|---|---:|---:|
| gpt-4.1 primary | 0.6200 | 0.5475–0.6925 |
| gpt-5.5 second | 0.5575 | 0.4700–0.6450 |

## Interpretation

The primary judge result is clearly above 0.50. The second judge result is supportive but lesse because its 95% confidence interval includes 0.50.

## Current decision

Freeze v9 as the engineering candidate.

Do not create v10 before packaging.

## Immediate next engineering target

Another developer should be able to run:

~~~bash
pip install -e .
python examples/v9_basic_demo.py
~~~

and receive a final response plus trace.

## Research next target

Create holdout-v2 with 500 cases and run ablations.

## Known weaknesses

- Observation/log cases are evaluation-ambiguous because workflow-correct logging can lose to advice-rich assistant answers.
- Writing and persona-shift need stronger future validation.
- Cross-provider validation is not included in the final holdout because Gemini quota failed.

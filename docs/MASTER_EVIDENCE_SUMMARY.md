# Cognitive Cell v9 — Master Evidence Summary

## Accepted stack

~~~text
router-v4 → selector-v5 → finalizer-v9
~~~

## Public package status

Cognitive Cell is publicly installable through PyPI and usable through:

- Python API
- CLI
- HTTP sidecar

## Fresh holdout-v1

| Judge | Architecture preference |
|---|---:|
| gpt-4.1 primary | 0.6200 |
| gpt-5.5 second | 0.5575 |
| Two-judge mean | 0.58875 |

## 100-event enterprise sidecar pilot

| Metric | Result |
|---|---:|
| Useful first move | 1.00 |
| Too vague | 0.00 |
| Unsafe or overreaching | 0.00 |
| Trace useful | 1.00 |

## 100-event direct-baseline ablation

| Preferred output | Count | Rate |
|---|---:|---:|
| Full v9 | 44 | 0.44 |
| Baseline | 21 | 0.21 |
| Tie | 35 | 0.35 |

Full v9 was preferred or tied in:

~~~text
79 / 100 = 0.79
~~~

## 100-event component ablation

| Output | Preferred count |
|---|---:|
| Full v9 | 77 |
| Plain direct | 9 |
| Direct artifact | 13 |
| Workflow artifac|
| Selector without finalizer | 0 |
| Tie | 1 |

Full v9 was preferred or tied in:

~~~text
78 / 100 = 0.78
~~~

## Holdout-v2 500-case dataset

Status:

~~~text
500 / 500 cases reviewed
~~~

Composition:

- 10 families
- 50 cases per family

Review result:

- case quality: 1.00
- context sufficient: 1.00
- family correct: 1.00
- revisions needed: 3 / 500 = 0.006

## Holdout-v2 50-case evaluation smoke

| Preferred output | Count | Rate |
|---|---:|---:|
| Full v9 | 23 | 0.46 |
| Baseline | 24 | 0.48 |
| Tie | 3 | 0.06 |

Full v9 was preferred or tied in:

~~~text
26 / 50 = 0.52
~~~

Interpretation:

The broader holdout-v2 smoke was borderline. Full v9 remained useful and safe, but the plain direct baseline was highly competitive on broader assistant-style tasks.

## Weak-family diagnostic

Weak areas:

- planning_design
- persona_shift
- timing_shift
- tutoring_explaining
- writing_support

Main diagnostic result:

~~~text
v10_patch_needed_count = 16 / 25
v10_patch_needed_rate = 0.64
~~~

Interpretation:

The weakness is mostly broad assistant-style behavior, not workflow-sidecar failure.

## v10-dev 20-case smoke

| Preferred output | Count | Rate |
|---|---:|---:|
| Full v9 | 11 | 0.55 |
| Baseline | 5 | 0.25 |
| Tie | 4 | 0.20 |

Full v9 was preferred or tied in:

~~~text
15 / 20 = 0.75
~~~

Decision:

Do not patch v10 yet.

## Main conclusion

Cognitive Cell v9 is strongest as a context-sensitive workflow sidecar and route-select-render control layer.

It should not be framed as a universal assistant replacement.

## Claims to avoid

- AGI
- consciousness
- universal superiority over frontier models
- production-autonomous agent

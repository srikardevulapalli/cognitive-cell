# Evaluation Summary

## Accepted stack

~~~text
router-v4 → selector-v5 → finalizer-v9
~~~

## Fresh holdout-v1

| Judge | Architecture preference |
|---|---:|
| gpt-4.1 primary | 0.6200 |
| gpt-5.5 second | 0.5575 |
| Mean | 0.58875 |

## 100-event enterprise pilot

| Metric | Result |
|---|---:|
| Useful first move | 1.00 |
| Too vague | 0.00 |
| Unsafe or overreaching | 0.00 |
| Trace useful | 1.00 |

## 100-event direct-baseline ablation

| Preferred output | Count |
|---|---:|
| Full v9 | 44 |
| Plain direct baseline | 21 |
| Tie | 35 |

Full v9 preferred or tied:

~~~text
79 / 100 = 0.79
~~~

## 100-event component ablation

| Output | Preferred count |
|---|---:|
| Full v9 | 77 |
| Plain direct | 9 |
| Direct artifact | 13 |
| Workflow artifact | 0 |
| Selector without finalizer | 0 |
| Tie | 1 |

Full v9 preferred or tied:

~~~text
78 / 100 = 0.78
~~~

## Main interpretation

The full route-select-render stack is more useful than exposing intermediartifacts directly.

## Important caution

These are curated enterprise sidecar evaluations. They are not a universal benchmark and not a claim of AGI or broad frontier-model superiority.

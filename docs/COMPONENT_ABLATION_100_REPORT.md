# Cognitive Cell v9 — 100-Event Component Ablation

## Status

component_ablation_100_strong_pass

## Preferred output

| Output | Count | Rate |
|---|---:|---:|
| Full v9 | 77 | 0.77 |
| Plain direct | 9 | 0.09 |
| Direct artifact | 13 | 0.13 |
| Workflow artifact | 0 | 0.00 |
| Selector without finalizer | 0 | 0.00 |
| Tie | 1 | 0.01 |

## Main metric

Full v9 was preferred or tied in:

~~~text
78 / 100 = 0.78
~~~

## Usefulness by component

| Component | Useful rate |
|---|---:|
| Full v9 | 1.00 |
| Plain direct | 1.00 |
| Direct artifact | 1.00 |
| Workflow artifact | 0.42 |
| Selector without finalizer | 0.59 |

## By group

| Group | Full v9 preferred or tied |
|---|---:|
| growth_product | 0.85 |
| support_ops | 0.60 |
| data_pipeline | 0.90 |
| risk_compliance | 0.65 |
| ops_process | 0.90 |

## Interpretation

This component ablation supports the route-select-render architecture.

Plain direct and direct artifacts were usefulbut full v9 was preferred most often. Raw workflow artifacts and selector-without-finalizer outputs were much less useful as user-facing responses.

## Architectural lesson

Internal artifacts are not the product. The finalizer-v9 layer is important for turning cognitive traces and selected artifacts into useful user-facing answers.

## Caveat

This is a 100-event component ablation on a curated enterprise sidecar pilot. It is not a universal benchmark and not a claim of AGI or broad frontier-model superiority.

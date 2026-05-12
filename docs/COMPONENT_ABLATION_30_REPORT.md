# Cognitive Cell v9 — 30-Event Component Ablation

## Status

Component ablation passed.

## Preferred output

| Output | Count | Rate |
|---|---:|---:|
| Full v9 | 22 | 0.73 |
| Plain direct | 1 | 0.03 |
| Direct artifact | 6 | 0.20 |
| Workflow artifact | 0 | 0.00 |
| Selector without finalizer | 0 | 0.00 |
| Tie | 1 | 0.03 |

## Main metric

Full v9 was preferred or tied in:

~~~text
23 / 30 = 0.77
~~~

## Usefulness by component

| Component | Useful rate |
|---|---:|
| Full v9 | 1.00 |
| Plain direct | 1.00 |
| Direct artifact | 1.00 |
| Workflow artifact | 0.37 |
| Selector without finalizer | 0.47 |

## Interpretation

This component ablation supports the route-select-render architecture.

Plain direct and direct artifacts were often useful, but full v9 was preferred most often. Raw workflow artifacts and selector-without-finalizer outputs were much less useful as user-facing responses.

## Architectural lesson

Internal artifacts are not the oduct. The finalizer-v9 layer is important for turning cognitive traces and selected artifacts into useful user-facing answers.

## Caveat

This is a 30-event component ablation on a curated enterprise sidecar pilot. It is not a universal benchmark and not a claim of AGI or broad frontier-model superiority.

## Next milestone

Expand to a 100-event component ablation using cached outputs only.

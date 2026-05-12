# Cognitive Cell v9 — 10-Event Component Ablation Smoke

## Status

Component ablation smoke passed.

## Preferred output

| Output | Count | Rate |
|---|---:|---:|
| Full v9 | 7 | 0.70 |
| Plain direct | 1 | 0.10 |
| Direct artifact | 1 | 0.10 |
| Tie | 1 | 0.10 |

## Usefulness by component

| Component | Useful rate |
|---|---:|
| Full v9 | 1.00 |
| Plain direct | 1.00 |
| Direct artifact | 1.00 |
| Workflow artifact | 0.20 |
| Selector without finalizer | 0.30 |

## Interpretation

Full v9 was preferred or tied in 8 / 10 cases.

The smoke test suggests that the finalizer-v9 layer is important: raw workflow artifacts and selector-without-finalizer outputs were much less useful as user-facing responses.

## Caveat

This is a 10-event smoke test. Expand to 30 events before making a stronger component-ablation claim.

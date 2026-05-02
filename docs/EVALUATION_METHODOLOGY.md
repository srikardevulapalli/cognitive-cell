# Evaluation Methodology

## Two tracks

### 1. Assistant preference

Question:

> Which re a human user rather continue from?

Use for standalone assistant tasks, writing, tutoring, everyday requests, and general planning.

### 2. Workflow-contract correctness

Question:

> Did the system behave correctly for the workflow posture?

Use for workflow_component/log, monitor/suggest, enterprise sidecars, audit trails, and observation logs.

## Why this split matters

A pure observation record may lose to an advice-rich baseline in assistant preference while still being correct for workflow logging.

## Metrics

- pairwise preference
- workflow-contract correctness
- useful first move
- pathway selection accuracy
- latency
- cost
- trace usefulness

## Future paper requirement

Add:

- 500-case holdout-v2
- ablations
- human evaluation
- cost/latency table
- confidence intervals

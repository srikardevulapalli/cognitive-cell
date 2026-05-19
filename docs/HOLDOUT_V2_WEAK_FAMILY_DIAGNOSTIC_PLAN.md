# Holdout-v2 Weak-Family Diagnostic Plan

## Why this exists

The holdout-v2 50-case smoke was borderline:

- Full v9 preferred: 23
- Baseline preferred: 24
- Tie: 3
- Full v9 preferred or tied: 26 / 50 = 0.52

Full v9 remains useful and safe, but the plain direct baseline is highly competitive on the broader holdout-v2 distribution.

## Stronger families

- analysis_enterprise
- atomic_observation
- contextual_observation
- everyday_request
- sensitive_guidance

## Weaker families

- planning_design
- persona_shift
- timing_shift
- tutoring_explaining
- writing_support

## Diagnostic question

For each weak-family case, determine whether the issue is:

1. Router issue
2. Selector issue
3. Finalizer issue
4. Evaluation-contract issue
5. Plain direct baseline is simply the right response
6. v9 is over-structuring a simple assistant task

## Do not do yet

- Do not patch v10.
- Do not run full 500.
- Do not use API judging.
- Do not tune on holdout-v2.

## Decision rule

If weak cases are mostly simple assistant tasks where direct baseline is naturally better, then v9 should remain framed as a workflow sidecar, not a universal assistant replacement.

If weak cases show systematic selector/finalizer errors that also affect workflow-sidecar use cases, then consider a targeted v10 patch after a separate dev set.

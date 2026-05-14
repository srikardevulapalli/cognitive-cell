# Holdout-v2 Design

## Purpose

Holdout-v2 is a 500-case benchmark for evaluating whether Cognitive Cell generalizes beyond the current curated enterprise sidecar pilot and holdout-v1.

## Size

~~~text
500 cases
10 families
50 cases per family
~~~

## Families

- atomic_observation
- contextual_observation
- everyday_request
- planning_design
- analysis_enterprise
- sensitive_guidance
- persona_shift
- timing_shift
- tutoring_explaining
- writing_support

## Rules

- Do not tune v9 on holdout-v2.
- Do not patch v10 using holdout-v2 failures.
- Do not inspect individual failures until after scoring.
- Use holdout-v2 for final validation, not development.
- Use manual ratings for human columns.
- Use API calls only to generate candidate outputs.

## Required case fields

~~~text
case_id
family
statement
context_snapshot
metadata
interaction_mode
autonomy_mode
expected_contract
notes
~~~

## Evaluation tracks

### Assistant preference

Which response would a user rather continue from?

### Workflow-contract correctness

Did the system behave correctly for the workflow posture?

### Trace usefulness

Does the trace help explain the selected pathway?

## Success metrics

- useful first move
- pairwise preference
- workflow-contract correctness
- trace usefulness
- safety / overreach
- latency and cost

## Important caveat

Observation/log cases need separate workflow-contract scoring because pure recordkeeping can lose to advice-rich assistant responses even when logging is the correct workflow behavior.

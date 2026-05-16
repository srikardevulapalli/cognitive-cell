# v10 Development Plan

## Why v10-dev exists

Holdout-v2 smoke showed that v9 is useful and safe but not consistently better than direct baseline on broad assistant-style tasks.

Weak families:

- planning_design
- persona_shift
- timing_shift
- tutoring_explaining
- writing_support

## Rule

Do not patch on holdout-v2.

Use a separate v10-dev set for development. Holdout-v2 remains validation-only.

## Goal

Improve broad assistant-style rendering while preserving v9's workflow-sidecar strengths.

## Likely patch area

Start with finalizer only.

Do not patch router or selector unless the dev diagnostics clearly show selector failure.

## v10-dev dataset

100 cases:

- 20 planning_design
- 20 persona_shift
- 20 timing_shift
- 20 tutoring_explaining
- 20 writing_support

## Evaluation ladder

1. Generate v10-dev 100 cases.
2. Review dataset quality manually.
3. Run v9 and baseline on 20-case smoke.
4. Diagnose failures.
5. Create finalizer-v10 candidate.
6. Run v10 on same dev set.
7. If v10 improves dev set, validate on untouched holdout-v2 smoke.
8. Do not claim improvement until holdout-v2 improves.

## Success criteria

v10 should improve:

- planning concreteness
- persona adaptation
- timing adaptation
- tutoring clarity
- writing naturalness

without weakening:

- workflow sidecar behavior
- safety
- trace usefulness

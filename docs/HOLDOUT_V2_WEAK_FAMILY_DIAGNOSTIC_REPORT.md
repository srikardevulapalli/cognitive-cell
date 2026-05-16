# Holdout-v2 Weak-Family Diagnostic

## Status

Diagnostic completed.

## Context

The holdout-v2 50-case evaluation smoke was borderline:

| Preferred output | Count |
|---|---:|
| Full v9 | 23 |
| Baseline | 24 |
| Tie | 3 |

Full v9 was preferred or tied in:

~~~text
26 / 50 = 0.52
~~~

## Weak-family diagnostic result

25 weak-family rows were reviewed across:

- planning_design
- persona_shift
- timing_shift
- tutoring_explaining
- writing_support

## Diagnostic category counts

| Category | Count |
|---|---:|
| persona_adaptation_weak | 4 |
| planning_output_less_concrete | 5 |
| tutoring_less_clear | 3 |
| writing_output_less_natural | 3 |
| v9_over_structured | 1 |
| timing_adaptation_weak | 1 |
| direct_baseline_naturally_better | 1 |
| no_v9_issue | 7 |

## Patch signal

~~~text
v10_patch_needed_count = 16 / 25
v10_patch_needed_rate = 0.64
~~~

## Interpretation

The weak cases are mostly broad assistant-style tasks where direct baselines are naturally strong or where v9 needs better rendering, adaptation, and concreteness.

This does not invalidate the workflow-sidecar claim. It means the product claim should remain narrow:

> Cognitive Cell v9 is strongest as a workflow sidecar and context-sensitive control layer, not as a universal replacement for direct assistant answers.

## Recommendation

Do not patch v9 directly from holdout-v2 failures.

If v10 is pursued, create a separate development set focused on:

- persona adaptation
- planning first-step concreteness
- tutoring clarity
- writing naturalness
- timing adaptation

Then validate v10 on a fresh holdout, not on the same diagnostic cases.

# Ablation Plan

## Goal

Determine whether the full Cognitive Cell v9 stack is better than simpler alternatives.

Accepted full stack:

~~~text
router-v4 → selector-v5 → finalizer-v9
~~~

## Systems to compare

### A. Full Cognitive Cell v9

Current package behavior.

### B. Plain direct baseline

A single strong model response to the same enterprise event.

### C. Workflow-only

Use workflow-style candidate only, without direct-path selection.

### D. Direct-only

Use direct candidate only, without workflow-path selection.

### E. Selector without finalizer

Select workflow/direct artifact, but do not render through finalizer-v9.

### F. Finalizer-only baseline

Give the plain direct baseline to the finalizer, without router/selector structure.

## First ablation scope

Start with a 10-event smoke only.

Do not run all 100 until the ablation smoke produces useful differences.

## Metrics

For each output, manu score:

- useful_first_move_0_1
- too_vague_0_1
- unsafe_or_overreaching_0_1
- trace_useful_0_1
- preferred_output: full_v9 / baseline / tie

## Success criterion

Full v9 should beat or tie simpler baselines on most cases while preserving trace usefulness.

## Cost rule

Use API only to generate outputs.

Do not use API to judge, rank, or fill human-review columns.

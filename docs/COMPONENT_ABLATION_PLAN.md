# Component Ablation Plan

## Goal

Determine which part of Cognitive Cell v9 contributes most to the observed improvement.

Accepted full stack:

~~~text
router-v4 → selector-v5 → finalizer-v9
~~~

## Systems to compare

### A. Full v9

The current public package output.

### B. Plain direct baseline

A direct model answer with no cognitive-cell structure.

### C. Direct artifact only

The direct candidate generated inside the cell, before selector/finalizer.

### D. Workflow artifact only

The workflow candidate generated inside the cell, before selector/finalizer.

### E. Selector without finalizer

The selected internal artifact, shown without finalizer-v9 rendering.

## What each ablation tests

- Plain direct baseline tests whether the whole architecture adds value over direct prompting.
- Direct artifact only tests whether internal candidate generation alone is enough.
- Workflow artifact only tests whether structured workflow artifacts are usefuthout final rendering.
- Selector without finalizer tests whether finalizer-v9 is necessary.
- Full v9 tests the complete route-select-render stack.

## Cost rule

Use cached full-v9 traces and cached plain baselines wherever possible.

Do not call API for judging or manual ratings.

## First scope

Run a 10-event component-ablation smoke.

Expand only if the result is informative.

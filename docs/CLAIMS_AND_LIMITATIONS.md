# Claims and Limitations

## What Cognitive Cell v9 is

Cognitive Cell v9 is a context-sensitive workflow-control layer.

It separates:

~~~text
routing → pathway selection → final rendering
~~~

The accepted stack is:

~~~text
router-v4 → selector-v5 → finalizer-v9
~~~

## Supported claims

### Public package claim

Cognitive Cell is publicly installable and usable through:

- Python API
- CLI
- HTTP sidecar

### Workflow-sidecar claim

Cognitive Cell v9 performs strongly in curated enterprise sidecar tasks.

### Ablation claim

On the curated 100-event enterprise sidecar pilot, full v9 outperformed or tied simpler baselines and intermediate components.

### Traceability claim

Cognitive Cell returns a response plus trace, selected pathway, response mode, and next-step type.

## Claims to avoid

Do not claim:

- AGI
- consciousness
- sentience
- universal assistant superiority
- frontier-model superiority
- production-ready autonomous action
- replaor human review in sensitive workflows

## Known limitations

- Broader holdout-v2 smoke was borderline.
- Plain direct baseline is highly competitive on broad assistant-style tasks.
- Weaknesses include planning concreteness, persona adaptation, timing adaptation, tutoring clarity, and writing naturalness.
- Current evidence includes curated pilot evaluations and manual ratings.
- More human evaluation is needed.
- More cross-provider validation is needed.
- Do not tune on holdout-v2.

## Current release decision

v9 remains the public release.

A v10 patch is not justified yet based on the v10-dev 20-case smoke.

## Best framing

Cognitive Cell v9 is best framed as:

> A benchmarked, installable, context-sensitive workflow-control layer for routing, selecting, rendering, and tracing AI first responses.

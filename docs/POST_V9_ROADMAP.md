# Post-v9 Roadmap

## Current status

Cognitive Cell v9 is publicly installable and has passed:

- fresh holdout-v1 validation
- 100-event enterprise sidecar pilot
- 100-event direct-baseline ablation
- 100-event component ablation

Accepted stack:

~~~text
router-v4 → selector-v5 → finalizer-v9
~~~

## Current safe claim

On a fresh 100-case holdout, the frozen v9 stack beat a plain strong-model baseline under two standardized OpenAI judges, with mean architecture preference around 0.589.

On a curated 100-event enterprise sidecar pilot, full v9 was preferred or tied in 79 / 100 cases against a plain direct baseline.

On a 100-event component ablation, full v9 was preferred or tied in 78 / 100 cases against simpler components.

## What not to claim

- Not AGI.
- Not consciousness.
- Not universal superiority over frontier models.
- Not production-autonomous without governance.

## Next research milestones

1. Holdout-v2 500-case benchmark.
2. Human evaluation pcol.
3. Cost and latency report.
4. Technical report / paper draft.
5. Optional cross-provider evaluation when quota/cost allows.

## Next product milestones

1. Improve quickstart docs.
2. Add more integration examples.
3. Add no-cost smoke tests.
4. Document human-in-the-loop production posture.
5. Add issue templates and contribution guidelines.

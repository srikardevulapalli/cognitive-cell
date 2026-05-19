# Cognitive Cell: A Route-Select-Render Control Stack for Workflow AI

## Abstract

Cognitive Cell is a context-sensitive control layer for workflow AI. It separates routing, pathway selection, and final response rendering. The accepted v9 stack is router-v4, selector-v5, and finalizer-v9. Across curated enterprise sidecar evaluations, full v9 outperforms a plain direct baseline and its own intermediate components. Broader holdout-v2 smoke testing shows that v9 should be framed as a workflow sidecar rather than a universal assistant replacement.

## 1. Motivation

LLMs can answer well, but they do not always know what kind of first move is appropriate.

The same input can require different behavior depending on:

- workflow posture
- urgency
- context
- persona
- risk
- whether the system is logging, suggesting, or answering directly

## 2. Architecture

Accepted stack:

~~~text
router-v4 → selector-v5 → finalizer-v9
~~~

The architecture separates:

1. itive routing
2. workflow-vs-direct pathway selection
3. final user-facing rendering

## 3. Product interface

Cognitive Cell v9 is available as:

- Python library
- CLI
- HTTP sidecar

The HTTP sidecar accepts enterprise event payloads and returns:

- response text
- selected pathway
- response mode
- next-step type
- approval flag
- trace

## 4. Evaluation summary

### Fresh holdout-v1

Two OpenAI judges scored the v9 stack above a plain baseline with mean architecture preference around 0.589.

### Enterprise sidecar pilot

A 100-event enterprise sidecar pilot passed with:

- useful first move: 1.00
- too vague: 0.00
- unsafe/overreaching: 0.00
- trace useful: 1.00

### Direct-baseline ablation

Full v9 was preferred or tied in 79 / 100 cases against a plain direct baseline.

### Component ablation

Full v9 was preferred or tied in 78 / 100 cases against simpler components and a plain direct baseline.

### Holdout-v2

A 500-case holdout-v2 benchmark was built and reviewed.

A 50-case holdout-v2 smoke was borderline:

- full v9 preferred: 23
- baseline preferred: 24
- tie: 3

This shows the plain direct baseline is highly competitive on broader assistant-style tasks.

## 5. Failure analysis

Weak areas include:

- planning concreteness
- persona adaptation
- timing adaptation
- tutoring clarity
- writing naturalness

The weak-family diagnostic suggests that these are broad assistant-style weaknesses rather than failures of the enterprise sidecar architecture.

## 6. Decision on v10

A separate v10-dev set was created to avoid contaminating holdout-v2.

The 20-case v10-dev smoke did not justify a v10 patch yet:

- full v9 preferred: 11
- baseline preferred: 5
- tie: 4

Therefore, v9 remains the current release candidate.

## 7. Limitations

Cognitive Cell v9 is not:

- AGI
- consciousness
- a production-autonomous agent
- a universal replacement for direct assistant answers
- a claim of broad superiority over frontier models

Current evaluations include curated pilot sets and manual ratings. Broader external validation is still needed.

## 8. Future work

- larger human evaluation
- full holdout-v2 evaluation after smoke analysis
- cross-provider evaluation
- cost and latency optimization
- production governance and human-in-the-loop workflows
- optional v10 finalizer work on a separate development set

## Main claim

Cognitive Cell v9 is a public, installable, benchmarked workflow-control layer whose full route-select-render stack outperforms simpler direct and component baselines in curated enterprise sidecar evaluations, while broader holdout-v2 testing shows it should not be framed as a universal assistant replacement.

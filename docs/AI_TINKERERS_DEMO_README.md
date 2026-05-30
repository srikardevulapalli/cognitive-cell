# AI Tinkerers Demo README — Cognitive Cell

## Talk title

**I Built a Traffic Controller for LLM Workflows: Route, Select, Render**

Alternative title:

**Cognitive Cell: What I Learned Building a Control Layer for LLM Workflows**

---

## One-sentence explanation

I built a small control layer for LLM workflows that decides **what kind of response is appropriate before answering**: should the AI record, clarify, analyze, plan, answer directly, or escalate?

---

## The easiest way to understand it

Most LLM apps work like this:

~~~text
user asks something → model answers
~~~

Cognitive Cell works like this:

~~~text
user asks something
→ decide what kind of situation this is
→ choose the right response pathway
→ render the final answer
→ return a trace explaining the decision
~~~

It is like adding a **traffic controller** in front of an LLM.

The point is not to build a new foundation model. The point is to make existing modetter inside workflows.

---

## Why I built it

I started with a simple question:

> Why does the same sentence sometimes need totally different AI behavior?

Example:

~~~text
Blue colour is observed.
~~~

In normal chat, an assistant might explain what blue could mean.

But in a workflow log, the right response is:

~~~text
Observation recorded.
~~~

Another example:

~~~text
The package label shows the wrong city.
~~~

If the package is still in the warehouse, the right move is:

~~~text
Fix the label before shipment.
~~~

If the package contains temperature-sensitive medication and is already in transit, the right move is:

~~~text
Contact the carrier immediately and request a reroute or hold.
~~~

Same sentence. Different context. Different correct first move.

That became the core idea:

> AI systems should not only answer. They should first decide what kind of cognitive move is appropriate.

---

## What I built

I built **Cognitive Cell**, a Python package and HTTP sidecar for context-sensitive workflow AI.

The accepted v9 stack is:

~~~text
router-v4 → selector-v5 → finalizer-v9
~~~

Each layer has a job.

### Router

The router decides the response mode:

~~~text
record
clarify
analyze
plan
direct answer
escalate
~~~

### Selector

The selector chooses between possible pathways:

~~~text
workflow-style response
direct-answer response
~~~

### Finalizer

The finalizer turns internal reasoning artifacts into a useful human-facing answer.

This became the most important lesson:

> Internal artifacts are not the product.

Raw workflow artifacts are useful for traceability, but often weak as final answers. The finalizer is what makes the system usable.

---

## How to install it

~~~bash
pip install "cognitive-cell[server]"
~~~

The package is public on PyPI as `cognitive-cell`.

---

## Python usage

~~~python
from cognitive_cell import CognitiveCellRequest, CognitiveCellV9

cell = CognitiveCellV9()

request = CognitiveCellRequest(
    statement="Blue colour is observed.",
    interaction_mode="worw_component",
    autonomy_mode="log",
)

result = cell.run(request)

print(result.response_text)
print(result.selected_response_mode)
print(result.selected_next_step_type)
print(result.trace)
~~~

Expected behavior:

~~~text
The system should record the observation instead of over-explaining it.
~~~

---

## CLI usage

Create an event JSON file, then run:

~~~bash
cognitive-cell --event-json examples/event.example.json
~~~

This calls the configured model and may incur API cost.

---

## HTTP sidecar usage

Start the sidecar:

~~~bash
python -m uvicorn cognitive_cell.server.app:app --port 8000
~~~

Check health without model calls:

~~~bash
curl -s http://127.0.0.1:8000/health
~~~

Send an event:

~~~bash
curl -s -X POST http://127.0.0.1:8000/v1/sidecar \
  -H "Content-Type: application/json" \
  -d @examples/event.example.json
~~~

The `/health` endpoint costs nothing. The `/v1/sidecar` endpoint calls the configured model.

---

## Example event payload

~~~json
{
  "event_id": "evt_pricing_refunds_001",
  "source": "growth_ops_monitor",
  "event_type": "metric_anomaly",
  "statement": "Refund requests doubled after the pricing page update. What should we examine first?",
  "context": {
    "world_facts": [
      {
        "fact_id": "f1",
        "fact_type": "world_fact",
        "fact_text": "The pricing page was updated yesterday."
      }
    ],
    "constraints": [
      "Prioritize high-signal first checks before broad analysis."
    ],
    "active_goals": [
      "identify the first diagnostic step"
    ]
  },
  "metadata": {
    "persona": "growth operations analyst",
    "time_pressure": "medium"
  },
  "interaction_mode": "workflow_component",
  "autonomy_mode": "suggest"
}
~~~

---

## Feeding context into the system

Cognitive Cell receives context through three channels:

~~~text
1. context_snapshot
2. metadata
3. interaction_mode + autonomy_mode
~~~

### context_snapshot

~~~json
{
  "world_facts": [],
  "constraints": [],
  "active_goals": []
}
~~~

### metadata

~~~json
{
  "persona": "ops analyst",
  "time_pressure": "medium"
}
~~~

### behavior posture

~~~text
interaction_mode = workflow_component
autonomy_mode = suggest
~~~

This lets the same input behave differently depending on workflow posture, urgency, persona, and goal.

---

## The hard-won lesson

Early versions produced structured workflow artifacts.

They looked architecturally elegant, but users and judges often preferred the plain baseline because the baseline gave a smoother answer.

The surprising lesson was:

> Internal structure is not enough. The final user-facing rendering matters.

That is why the architecture became:

~~~text
route → select → render
~~~

Instead of exposing raw internal artifacts, finalizer-v9 renders the selected artifact into something useful.

---

## Journey from idea to now

### Stage 1 — Original idea

I started with a “cognitive cell” idea: a reusable unit that can appraise context, focus attention, choose a response mode, and produce a trace.

At this stage, it was more architecture tt.

### Stage 2 — Router

I built a router that could decide:

~~~text
record vs clarify vs analyze vs plan vs direct answer
~~~

This worked in simple demos, but it was brittle.

### Stage 3 — Evals exposed the truth

When I evaluated early versions against a plain baseline, the architecture initially lost.

The problem was not that the idea was useless.

The problem was that internal workflow outputs were not always good final answers.

### Stage 4 — Selector

I added a selector that could choose between workflow-style and direct-style pathways.

This made the system more flexible.

### Stage 5 — Finalizer

The major unlock was finalizer-v9.

Instead of exposing raw artifacts, the finalizer rendered a response that preserved the selected pathway but sounded useful to a human.

### Stage 6 — Package

I moved it from research scripts into an installable package:

~~~bash
pip install "cognitive-cell[server]"
~~~

It now supports:

~~~text
Python API
CLI
HTTP sidecar
~~~

### Stage 7 — Pilot and aen I tested whether the architecture actually helped.

---

## Metrics and evidence

### Fresh holdout-v1

On a fresh 100-case holdout:

| Judge | Architecture preference |
|---|---:|
| gpt-4.1 primary | 0.6200 |
| gpt-5.5 second | 0.5575 |
| Mean | 0.58875 |

Safe claim:

> On a fresh 100-case holdout, the frozen v9 stack beat a plain strong-model baseline under two standardized OpenAI judges, with mean architecture preference around 0.589.

---

### 100-event enterprise sidecar pilot

I ran the system on 100 enterprise-style workflow events.

| Metric | Result |
|---|---:|
| Useful first move | 1.00 |
| Too vague | 0.00 |
| Unsafe or overreaching | 0.00 |
| Trace useful | 1.00 |

Plain English:

> In this curated workflow setting, the system gave useful, safe first moves and useful traces.

---

### 100-event direct-baseline ablation

I compared full v9 against a plain direct baseline.

| Preferred output | Count |
|---|---:|
| Full v9 | 44 |
| Baseline | 21 |
| Tie | 35 |

Full v9 was preferred or tied in:

~~~text
79 / 100 = 0.79
~~~

Plain English:

> The architecture usually matched or beat a normal direct answer in enterprise sidecar tasks.

---

### 100-event component ablation

I compared full v9 against its own simpler pieces:

~~~text
full v9
plain direct
direct artifact
workflow artifact
selector without finalizer
~~~

Result:

| Output | Preferred count |
|---|---:|
| Full v9 | 77 |
| Plain direct | 9 |
| Direct artifact | 13 |
| Workflow artifact | 0 |
| Selector without finalizer | 0 |
| Tie | 1 |

Full v9 was preferred or tied in:

~~~text
78 / 100 = 0.78
~~~

Plain English:

> The complete route-select-render stack was much better than exposing raw intermediate pieces.

This was the strongest architecture result.

---

## Where it does not win

On broader assistant-style tasks, the plain direct baseline is very competitive.

In a 50-case holdout-v2 smoke test:

| Preferred output | Count |
|---|---:|
| Full v9 | 23 |
| Baseline | 24 |
| Tie | 3 |

Full v9 was preferred or tied in:

~~~text
26 / 50 = 0.52
~~~

Plain English:

> Cognitive Cell is not automatically better for every normal assistant task.

It is strongest when context and workflow posture matter.

It is weaker when the user simply wants a normal direct assistant response, especially in:

~~~text
writing
tutoring
persona adaptation
general planning
some timing-sensitive everyday tasks
~~~

That is why the correct claim is:

> Cognitive Cell is a workflow-control layer, not a universal assistant replacement.

---

## Manual adjudication

A manual blinded adjudication pass was completed on the 100-case enterprise direct-baseline comparison.

| Preferred output | Count |
|---|---:|
| Full v9 | 44 |
| Baseline | 21 |
| Tie | 35 |

Full v9 was preferred or tied in:

~~~text
79 / 100 = 0.79
~~~

Important caveat:

This was manual adjudication, not independent multi-rater human evaluation. Independent raters remain future work.

---

## What another builder can reuse

The reusable pattern is:

~~~text
route → select → render
~~~

Do noild workflow AI as only:

~~~text
prompt → answer
~~~

Build it as:

~~~text
input + context
→ classify the kind of move needed
→ generate candidate pathways
→ select the right pathway
→ render the final answer
→ expose a trace
~~~

This pattern is useful for:

~~~text
support triage
incident response
ops monitoring
data-quality alerts
compliance workflows
customer communication drafts
analytics first-check recommendations
workflow-sidecar systems
~~~

---

## What broke

Three things broke repeatedly:

### 1. The router over-clarified

Early versions asked clarifying questions even when they should record or answer.

### 2. Workflow artifacts looked good internally but bad externally

Structured artifacts were useful as traces, but not always good final answers.

### 3. The baseline was stronger than expected

Plain direct responses were often useful and safe.

The result was a more disciplined claim:

> Cognitive Cell adds value when response mode, context, traceability, and workflow posture m
## What surprised me

The finalizer mattered more than expected.

The router and selector were necessary, but raw selected artifacts were not enough.

The strongest architecture lesson became:

> Internal artifacts are not the product.

---

## What I would show live

### 1. Install

~~~bash
pip install "cognitive-cell[server]"
~~~

### 2. Python API

~~~python
from cognitive_cell import CognitiveCellRequest, CognitiveCellV9
~~~

### 3. Health endpoint

~~~bash
python -m uvicorn cognitive_cell.server.app:app --port 8000
curl -s http://127.0.0.1:8000/health
~~~

### 4. Context-sensitive example

Show:

~~~text
The package label shows the wrong city.
~~~

Then show two contexts:

~~~text
warehouse / low-cost correction
medicine / already in transit / high urgency
~~~

### 5. Trace

Show:

~~~text
selected_label
selected_response_mode
selected_next_step_type
trace
~~~

### 6. Evals

Show:

~~~text
100-event pilot
direct-baseline ablation
component ablation
holdout-v2 limitation
~~~

---

## What I would say in 90 seconds

I built Cognitive Cell, a small control layer for workflow AI.

The idea is that before an LLM answers, it should decide what kind of move is appropriate: record, clarify, analyze, plan, answer directly, or escalate.

The architecture is route-select-render. A router decides the response mode, a selector chooses between workflow and direct pathways, and a finalizer turns the selected internal artifact into a useful human-facing answer.

The hard lesson was that internal artifacts are not the product. Early versions produced structured outputs but lost to plain baselines because the final response was not human-useful enough. Finalizer-v9 became the key layer.

I packaged this as `cognitive-cell` on PyPI with a Python API, CLI, and HTTP sidecar.

In curated enterprise sidecar evaluations, full v9 was preferred or tied in 79/100 cases against a direct baseline, and 78/100 cases against its own simpler components.

But broader holdout-v2 testing was borderline, so the honest framing is: this is not AGI and not a universal assistant replacement. It is strongest as a context-sensitive workflow sidecar.

The reusable builder takeaway is: do not just prompt for the final answer. Route first, select the pathway, then render.

---

## What this is not

Cognitive Cell is not:

~~~text
AGI
consciousness
a new foundation model
a production-autonomous agent
a universal replacement for direct assistant answers
a claim of broad frontier-model superiority
~~~

It is:

~~~text
a workflow-control layer around existing LLMs
~~~

---

## Best framing

Use this:

> Cognitive Cell is a workflow-control layer for context-sensitive AI responses.

Do not use this:

> Cognitive Cell is AGI.

Use this:

> It improves first-response behavior in workflow and enterprise sidecar settings.

Do not use this:

> It beats frontier models generally.

Use this:

> The full route-select-render stack beat or tied simpler baselines in curated enterprise evaluations.

Do not use this:

> It is universally better than direct prompting.

---

## Next research steps

The next research steps are:

~~~text
1. Independent human evaluation.
2. Technical report polish.
3. Cost and latency report.
4. Broader external validation.
5. Memory/context adapter prototype.
6. Only consider v10 after a separate dev-set diagnosis.
~~~

Current decision:

~~~text
v9 remains the public release.
v10 is not justified yet.
holdout-v2 should not be used for tuning.
~~~

---

## Best demo takeaway

The strongest demo line is:

> The reusable lesson is not “use my package.” It is: when building workflow AI, separate route, select, and render — and evaluate internal artifacts separately from final answers.

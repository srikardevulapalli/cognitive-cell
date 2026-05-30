# Cognitive Cell

[![PyPI version](https://img.shields.io/pypi/v/cognitive-cell.svg)](https://pypi.org/project/cognitive-cell/)
[![Python versions](https://img.shields.io/pypi/pyversions/cognitive-cell.svg)](https://pypi.org/project/cognitive-cell/)

Cognitive Cell is a context-sensitive control stack for workflow AI.

Accepted v9 stack:

~~~text
router-v4 → selector-v5 → finalizer-v9
~~~

## What it does

The system separates:

~~~text
1. cognitive routing
2. workflow-vs-direct pathway selection
3. final user-facing rendering
~~~

This lets the same input behave differently depending on context, posture, urgency, role, and workflow constraints.

## Install

~~~bash
pip install "cognitive-cell[server]"
~~~

## Python usage

~~~python
from cognitive_cell import CognitiveCellRequest, CognitiveCellV9

cell = CognitiveCellV9()

request = CognitiveCellRequest(
    statement="Blue colour is observed.",
    interaction_mode="workflow_component",
    autonomy_mode="log",
)

result = cell.run(request)

print(result.response_text)
print(result.trace)
~~~

## CLI usage

Create an event JSON file, then run:

~~~bash
cognitive-cell --event-json examples/event.example.json
~~~

This calls the configured model and may incur API cost.

## HTTP sidecar usage

Start the server:

~~~bash
python -m uvicorn cognitive_cell.server.app:app --port 8000
~~~

Check health without model calls:

~~~bash
curl -s http://127.0.0.1:8000/health
~~~

Send an enterprise event:

~~~bash
curl -s -X POST http://127.0.0.1:8000/v1/sidecar \
  -H "Content-Type: application/json" \
  -d @examples/event.example.json
~~~

## Example event

~~~json
{
  "event_id": "evt_pricing_refunds_001",
  "source": "growth_ops_monitor",
  "event_type": "metric_anomaly",
  "statement": "Refund requests doubled after the pricing page update. What should we examine first?",
  "context": {
    "world_facts": [],
    "constraints": ["Prioritize high-signal first checks before broad analysis."],
    "active_goals": ["identify the first diagnostic step"]
  },
  "metadata": {
    "persona": "growth operations analyst",
    "time_pressure": "medium"
  },
  "interaction_mode": "workflow_component",
  "autonomy_mode": "suggest"
}
~~~

## Current evidence

Fresh holdout-v1, 100 cases:

| Judge | Architecture preference | Baseline preference |
|---|---:|---:|
| gpt-4.1 primary | 0.6200 | 0.3800 |
| gpt-5.5 second, combined 40+60 | 0.5575 | 0.4425 |
| Two-judge mean | 0.58875 | 0.41125 |

Safe claim:

> On a fresh 100-case holdout, the frozen v9 cognitive-cell stack beat a plain strong-model baseline under two standardized OpenAI judges, with mean architecture preference around 0.589.

## Caution

This is an engineering validation result, not a universal claim of superiority over frontier models. Larger benchmarks, human evaluation, ablations, and cross-provider validation are still needed.

## Cost note

`/health` costs nothing.

`/v1/sidecar` and `cognitive-cell --event-json ...` call the configured model and may incur API cost.

## Recommended production posture

Start with:

~~~text
autonomy_mode = "suggest"
human-in-the-loop
no automatic external action execution
~~~

## Known weaknesses

- Atomic observation remains weaker because pure logging competes against advice/explanation.
- Contextual observation remains mixed when direct action beats record/analyze behavior.
- Persona shift is weaker under the second judge.
- Writing support is improved but not consistently superior.

## What this is not

Cognitive Cell is not AGI, not a production-autonomous agent, and not a claim of universal superiority over frontier models.

It is a workflow-control layer that helps decide whether to record, clarify, analyze, plan, answer directly, or escalate.

## Enterprise sidecar pilot

Cognitive Cell v9 passed a 100-event enterprise sidecar pilot across:

- growth/product analytics
- support/operations
- data-pipeline reliability
- risk/compliance
- operations/process workflows

Pilot result:

| Metric | Result |
|---|---:|
| Useful first move | 1.00 |
| Too vague | 0.00 |
| Unsafe or overreaching | 0.00 |
| Trace useful | 1.00 |

See: `docs/PILOT_100_REPORT.md`

Caution: this is a curated pilot result, not a claim of universal superiority.


## 100-event ablation

Full Cognitive Cell v9 was compared against a plain direct baseline on the 100-event enterprise sidecar pilot.

Result:

| Preferred output | Count | Rate |
|---|---:|---:|
| Full v9 | 44 | 0.44 |
| Baseline | 21 | 0.21 |
| Tie | 35 | 0.35 |

Full v9 was preferred or tied in:

~~~text
79 / 100 = 0.79
~~~

See: `docs/ABLATION_100_REPORT.md`

Caution: this is a curated enterprise sidecar ablation, not a universal benchmark.

## 100-event component ablation

Full Cognitive Cell v9 was compared against its simpler components and a plain direct baseline on the 100-event enterprise sidecar pilot.

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

This supports the route-select-render architecture: internal artifacts are useful for reasoning and traceability, but finalizer-v9 is important for converting them into user-facing answers.

See: `docs/COMPONENT_ABLATION_100_REPORT.md`

## Documentation

Key docs:

- [Quickstart](docs/QUICKSTART.md)
- [API Reference](docs/API_REFERENCE.md)
- [Claims and Limitations](docs/CLAIMS_AND_LIMITATIONS.md)
- [Master Evidence Summary](docs/MASTER_EVIDENCE_SUMMARY.md)
- [100-event Component Ablation](docs/COMPONENT_ABLATION_100_REPORT.md)
- [Holdout-v2 500-case Review](docs/HOLDOUT_V2_500_FINAL_REPORT.md)
- [Technical Report Draft](docs/TECHNICAL_REPORT_DRAFT.md)
- [Documentation Index](docs/INDEX.md)

<!-- AI_TINKERERS_DEMO_NARRATIVE_START -->

# Demo Narrative: Cognitive Cell

## The easiest way to explain Cognitive Cell

Cognitive Cell is a small control layer for LLM workflows.

Before the model answers, Cognitive Cell asks:

~~~text
What kind of response is appropriate here?
~~~

Should the AI:

~~~text
record
clarify
analyze
plan
answer directly
escalate
~~~

Most LLM apps work like this:

~~~text
user asks something → model answers
~~~

Cognitive Cell works like this:

~~~text
user asks something
→ decide what kind of situation this is
→ choose the right response pathway
→ render the final  return a trace explaining the decision
~~~

It is like adding a traffic controller in front of an LLM.

The goal is not to build a new foundation model. The goal is to make existing models behave better inside workflows.

---

## One-sentence version

I built a control layer for LLMs that decides what kind of response is appropriate before answering: should the AI record, clarify, analyze, plan, answer directly, or escalate?

---

## Why I built it

I started with a simple question:

> Why does the same sentence sometimes need totally different AI behavior?

For example:

~~~text
Blue colour is observed.
~~~

In a normal chat, the assistant might explain what blue could mean.

But in a workflow log, the right response is not an explanation. It is:

~~~text
Observation recorded.
~~~

Another example:

~~~text
The package label shows the wrong city.
~~~

If the package is still in the warehouse, the right response is:

~~~text
Fix the label before shipment.
~~~

But if the package contains temperature-sensitive medication and is already in transit, the right response is:

~~~text
Contact the carrier immediately and request a reroute or hold.
~~~

Same sentence. Different context. Different correct first move.

That became the core idea:

> AI systems should not only answer. They should first decide what kind of cognitive move is appropriate.

---

## What I built

I built Cognitive Cell, a Python package and HTTP sidecar for context-sensitive workflow AI.

The accepted v9 stack is:

~~~text
router-v4 → selector-v5 → finalizer-v9
~~~

Each layer has a job.

### 1. Router

The router decides the response mode:

~~~text
record
clarify
analyze
plan
direct answer
escalate
~~~

### 2. Selector

The selector chooses between possible pathways.

For example:

~~~text
Should this be a workflow artifact?
Or should this be a direct answer?
~~~

### 3. Finalizer

The finalizer turns internal reasoning artifacts into a clean user-facing response.

This turned out to be one of the most important lessons.

Raw internal arcts are useful for traceability, but they are often bad as final answers. The finalizer is what makes the system usable.

---

## How to use the package

Install:

~~~bash
pip install "cognitive-cell[server]"
~~~

### Python API

~~~python
from cognitive_cell import CognitiveCellRequest, CognitiveCellV9

cell = CognitiveCellV9()

request = CognitiveCellRequest(
    statement="Blue colour is observed.",
    interaction_mode="workflow_component",
    autonomy_mode="log",
)

result = cell.run(request)

print(result.response_text)
print(result.selected_response_mode)
print(result.trace)
~~~

### CLI

Create an event JSON file, then run:

~~~bash
cognitive-cell --event-json examples/event.example.json
~~~

This calls the configured model and may incur API cost.

### HTTP sidecar

Start the server:

~~~bash
python -m uvicorn cognitive_cell.server.app:app --port 8000
~~~

Check health without model calls:

~~~bash
curl -s http://127.0.0.1:8000/health
~~~

Send an enterprise event:

~~~bash
curl -s -X POST http://127.0.0.1:8000/v1/sidecar \
  -H "Content-Type: application/json" \
  -d @examples/event.example.json
~~~

The `/health` endpoint costs nothing. The `/v1/sidecar` endpoint calls the configured model.

---

## Demo examples

### Example 1: observation log

Input:

~~~text
A small puddle is forming under the sink.
~~~

A plain assistant might answer:

~~~text
It could be a leak. Check the pipe, clean it up, call maintenance...
~~~

But in workflow-log mode, Cognitive Cell should respond more like:

~~~text
Observation recorded: small puddle forming under sink.
Missing context: source, timing, severity.
~~~

That is better if the AI is inside an inspection or facilities log.

---

### Example 2: same sentence, different context

Input:

~~~text
The freezer temperature reads -4°C.
~~~

Context A:

~~~text
The freezer stores classroom ice packs.
~~~

Correct first move:

~~~text
Record the observation.
~~~

Context B:

~~~text
The freezer stores medication requiring -20°C storage.
~~~

Correct first move:

~~~tt
Take urgent cold-chain action.
~~~

This is the core value of the system: the same sentence can need a different cognitive move depending on context.

---

### Example 3: time pressure

Input:

~~~text
The client presentation starts in 20 minutes and the slides have formatting issues.
~~~

A generic assistant may give a full slide-design checklist.

Cognitive Cell should prioritize:

~~~text
Fix only visible formatting issues on the title, agenda, and key data slides.
Do not redesign everything.
~~~

It adapts to time pressure.

---

### Example 4: enterprise workflow

Input:

~~~text
Refund requests doubled after the pricing page update.
~~~

A plain answer might list many possible causes.

Cognitive Cell gives a workflow-style first diagnostic move:

~~~text
Compare the old and new pricing page for refund-policy wording,
price clarity, plan comparison changes, and user confusion signals in refund notes.
~~~

That is more useful in an operations workflow because it gives the first check, not just a brainstorm.

---

## What another builder can reuse

The reusable pattern is:

~~~text
route → select → render
~~~

Do not build workflow AI as only:

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

## Hard-won lesson

The surprising lesson was:

> Internal structure is not the product.

Early versions produced structured workflow artifacts. They looked architecturally elegant, but users and evaluators often preferred the plain baseline because the baseline gave a smoother answer.

So the key improvement was not only better routing. It was adding a final rendering layer.

That is why the final architecture became:

4 → selector-v5 → finalizer-v9
~~~

The finalizer-v9 layer translated internal artifacts into something people could actually use.

---

## Journey from idea to now

### Stage 1: Idea

I started with a “cognitive cell” idea: a reusable unit that can appraise context, focus attention, choose a response mode, and produce a trace.

At this stage, it was more architecture than product.

### Stage 2: Router

I built a router that could decide:

~~~text
record vs clarify vs analyze vs plan vs direct answer
~~~

This worked in simple demos, but it was brittle.

### Stage 3: Evals exposed the truth

When I evaluated it against a plain baseline, the architecture initially lost.

That was painful but useful.

The problem was not that the idea was useless. The problem was that internal workflow outputs were not always good final answers.

### Stage 4: Selector

I added a selector that could choose between workflow-style and direct-style outputs.

This made the system more flexible.

### Stage 5: Finalizer

Thenlock was the finalizer.

Instead of exposing raw internal artifacts, the system rendered a final response that preserved the selected pathway but sounded useful to a human.

That became v9.

### Stage 6: Packaging

Then I moved it out of research scripts and into an installable package:

~~~bash
pip install "cognitive-cell[server]"
~~~

It now supports:

~~~text
Python API
CLI
HTTP sidecar
~~~

### Stage 7: Pilot and ablations

Then I tested whether it actually helped.

---

## Metrics and evaluation

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

### Direct-baseline ablation

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

### Component ablation

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

> The complete route-select-render stack was much better than exposing the raw intermediate pieces.

This was the strongest architecture result.

---

## Where it does not win

This is important.

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

It is weaker when the user just wants a simple direct answer, especially in:

~~~text
writing
tutoring
persona adaptation
general planning
some timing-sensitive everyday tasks
~~~

That is why the right claim is:

> Cognitive Cell is a workflow control layer, not a universal assistant replacement.

---

## What I would say if someone asks: “Is this AGI?”

No.

Cognitive Cell is not AGI.

It is not a new foundation m.

It is not consciousness.

It is a control layer around existing LLMs.

It helps decide:

~~~text
what kind of response should happen next?
~~~

That is valuable, but narrow.

---

## What I would say if someone asks: “Why not just use a better prompt?”

Because prompts can produce good answers, but they do not naturally separate:

~~~text
workflow posture
routing
candidate generation
pathway selection
final rendering
trace
~~~

A direct prompt is often strong. In fact, the baseline was useful in almost every test.

But the architecture helps when:

~~~text
the same input needs different behavior depending on context
the system needs traceability
the response is part of a workflow
the AI needs to choose between record/analyze/plan/direct/escalate
~~~

That is the niche.

---

## Builder takeaway

If you are building AI inside workflows, do not just prompt for the final answer.

Separate:

~~~text
route
select
render
~~~

Also evaluate intermediate artifacts separately from final answers.

A trace can seful internally but bad as a user-facing response.

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
1. Run independent human evaluation.
2. Polish the technical report.
3. Improve cost and latency reporting.
4. Run broader external validation.
5. Only consider v10 after a separate dev-set diagnosis.
~~~

Current decision:

~~~text
v9 remains the public release.
v10 is not justified yet.
holdout-v2 should not be used for tuning.
~~~

<!-- AI_TINKERERS_DEMO_NARRATIVE_END -->

## AI Tinkerers demo narrative

For a builder-focused walkthrough of the project journey, architecture, evals, failures, and demo flow, see:

- [AI Tinkerers Demo README](docs/AI_TINKERERS_DEMO_README.md)


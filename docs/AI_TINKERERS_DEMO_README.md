# AI Tinkerers Demo README — Cognitive Cell

## Talk title

**I Built a Traffic Controller for LLM Workflows: Route, Select, Render**

## One-sentence explanation

Cognitive Cell is a small control layer for LLM workflows. Before the model answers, it decides what kind of response is appropriate: record, clarify, analyze, plan, answer directly, or escalate.

## The simple idea

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

It is like adding a traffic controller in front of an LLM.

The point is not to build a new foundation model. The point is to make existing models behave better inside workflows.

---

## Why I built it

I started with a simple problem:

> The same sentence can require different AI behavior depending on context.

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

---

## What I built

Cognitive Cell is a Python package and HTTP sidecar for context-sensitive workflow AI.

Accepted v9 stack:

~~~text
router-v4 → selector-v5 → finalizer-v9
~~~

### Router

Decides the response mode:

~~~text
record
clarify
analyze
plan
direct answer
escalate
~~~

### Selector

Chooses the best pathway:

~~~text
workflow-style response
direct-answer response
~~~

### Finalizer

Turns internal reasoning artifacts into a useful human-facing response.

This was the biggest lesson:

> Internal artifacts are not the product.

Traces and workflow records are useful internally, but they still need to be rendered clearly for humans.

---

## How to install

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
print(result.selected_response_mode)
print(result.selected_next_step_type)
print(result.trace)
~~~

## CLI usage

~~~bash
cognitive-cell --event-json examples/event.example.json
~~~

## HTTP sidecar usage

Start the server:

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

Cost note:

~~~text
/health costs nothing.
/v1/sidecar and CLI calls use the configured model.
~~~

---

## What I will show live

### 1. No-cost import check

~~~bash
python examples/ai_tinkerers_live_demo.py --no-model
~~~

### 2. Context-sensitive request examples

~~~bash
python examples/ai_tinkerers_live_demo.py --show-payloads
~~~

### 3. Optional live model run

~~~bash
export OPENAI_API_KEY="your_key_here"
python examples/ai_tinkerers_live_demo.py --live
~~~

### 4. HTTP health check

~~~bash
python -m uvicorn cognitive_cell.server.app:app --port 8000
curl -s http://127.0.0.1:8000/health
~~~

---

## Metrics and evidence

### Fresh holdout-v1

| Judge | Architecture preference |
|---|---:|
| gpt-4.1 primary | 0.6200 |
| gpt-5.5 second | 0.5575 |
| Mean | 0.58875 |

Safe claim:

> On a fresh 100-case holdout, the frozen v9 stack beat a plain strong-model baseline under two standardized OpenAI judges, with mean architecture preference around 0.589.

### 100-event enterprise sidecar pilot

| Metric | Result |
|---|---:|
| Useful first move | 1.00 |
| Too vague | 0.00 |
| Unsafe or overreaching | 0.00 |
| Trace useful | 1.00 |

### Direct-baseline ablation

| Preferred output | Count |
|---|---:|
| Full v9 | 44 |
| Baseline | 21 |
| Tie | 35 |

Full v9 preferred or tied:

~~~text
79 / 100 = 0.79
~~~

### Component ablation

| Output | Preferred count |
|---|---:|
| Full v9 | 77 |
| Plain direct | 9 |
| Direct artifact | 13 |
| Workflow artifact | 0 |
| Selector without finalizer | 0 |
| Tie | 1 |

Full v9 preferred or tied:

~~~text
78 / 100 = 0.78
~~~

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

Full v9 preferred or tied:

~~~text
26 / 50 = 0.52
~~~

Interpretation:

> Cognitive Cell is strongest as a workflow sidecar and context-sensitive control layer. It is not a universal assistant replacement.

---

## What broke

### 1. The router over-clarified

Early versions asked clarifying questions when they should have recorded or answered.

### 2. Workflow artifacts were too raw

Structured artifacts were useful internally, but weak as user-facing answers.

### 3. The baseline was stronger than expected

Plain direct answers were often useful and safe.

This forced the architecture to become more honest and more useful.

---

## Builder takeaway

The reusable pattern is:

~~~text
route → select → render
~~~

If you are building workflow AI, do not only do:

~~~text
prompt → answer
~~~

Instead:

~~~text
input + context
→ classify the kind of move needed
→ generate candidate pathways
→ select the right pathway
→ render the final answer
→ expose a trace
~~~

Also evaluate internal artifacts separately from final answers.

A trace can be useful internally but bad as a user-facing response.

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

## Tying it back to the original cognitive-cell idea

The original idea was a reusable cognitive unit that could:

~~~text
observe
appraise context
focus attention
choose a cognitive move
act through a pathway
return a response
expose a trace
eventually update context over time
~~~

Current v9 implements the stateless core:

| Original idea | Current v9 |
|---|---|
| input/perception | statement |
| world model | context_snapshot |
| appraisal | trace factors |
| focus | focus object / selected pathway |
| cognitive move | response mode |
| pathway choice | selector-v5 |
| expression | finalizer-v9 |
| trace | response trace |
| memory | future external adapter |

The next frontier is an explicit memory/context layer around the stateless cell.

---

## Best 90-second explanation

I built Cognitive Cell, a small control layer for workflow AI.

The idea is that before an LLM answers, it should decide what kind of move is appropriate: record, clarify, analyze, plan, answer directly, or escalate.

The architecture is route-select-render. A router decides the response mode, a selector chooses between workflow and direct pathways, and a finalizer turns the selected internal artifact into a useful human-facing answer.

The hard lesson was that internal artifacts are not the product. Early versions produced structured outputs but lost to plain baselines because the final response was not human-useful enough. Finalizer-v9 became the key layer.

I packaged this as `cognitive-cell` on PyPI with a Python API, CLI, and HTTP sidecar.

In curated enterprise sidecar evaluations, full v9 was preferred or tied in 79/100 cases against a direct baseline, and 78/100 cases against its own simpler components.

But broader holdout-v2 testing was borderline, so the honest framing is: this is not AGI and not a universal assistant replacement. It is strongest as a context-sensitive workflow sidecar.

The reusable builder takeaway is: do not just prompt for the final answer. Route first, select the pathway, then render.

---

## Best demo takeaway

The reusable lesson is not “use my package.”

It is:

> When building workflow AI, separate route, select, and render — and evaluate internal artifacts separately from final answers.

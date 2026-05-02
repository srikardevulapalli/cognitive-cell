# Pilot Plan: Analytics First-Check Sidecar

## Goal

Use Cognitive Cell v9 as a sidecar for analytics and operations anomaly events.

## Example input

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

## Output

The cell returns:

- response text
- selected pathway
- selected response mode
- next step type
- needs approval flag
- trace

## Success criteria

- The sidecar gives a useful first diagnostic step.
- The trace explains why direct/workflow was selected.
- Human analyst can accept, edit, or reject the recommendation.
- No automatic external action is taken.

## Pilot dataset

Start with 30 events:

- 10 growth/product anomalies
- 10 support/ops anomalies
- 10 data-pipeline anomalies

## Evaluation

For each event, score:

- useful first move: 0/1
- too vague: 0/1
- unsafe or overreaching: 0/1
- trace useful: 0/1
- human preferred over plain baseline: architecture / baseline / tie

## Deployment mode

~~~text
suggest-only
human-in-the-loop
no external action execution
~~~

## Do not include yet

- automatic ticket updates
- automatic customer messages
- production write actions
- sensitive PII workflows

from __future__ import annotations

import json
from pathlib import Path

GROUPS = [
    ("growth", "growth_ops_monitor", "metric_anomaly", "growth operations analyst"),
    ("support", "support_queue_monitor", "support_anomaly", "support operations analyst"),
    ("data", "data_quality_monitor", "data_pipeline_anomaly", "data operations analyst"),
    ("risk", "risk_monitor", "risk_anomaly", "risk operations analyst"),
    ("ops", "operations_monitor", "ops_anomaly", "operations analyst"),
]

templates = [
    "A key metric changed after a recent workflow update. What should we examine first?",
    "A process improved speed but quality complaints increased. Where should analysis start?",
    "The job completed successfully, but downstream outputs look wrong. What should we check first?",
    "A policy change affected one segment more than others. Where should investigation begin?",
    "User behavior changed after a product or process update. What is the first diagnostic step?"
]

rows = []
for group, source, event_type, persona in GROUPS:
    for i in range(1, 21):
        rows.append(
            {
                "event_id": f"pilot100_{group}_{i:03d}",
                "source": source,
                "event_type": event_type,
                "statement": templates[(i - 1) % len(templates)],
                "context": {
                    "world_facts": [],
                    "constraints": ["Prioritize high-signal first checks before broad analysis."],
                    "active_goals": ["identify the first diagnostic step"]
                },
                "metadata": {
                    "persona": persona,
                    "time_pressure": "medium"
                },
                "interaction_mode": "workflow_component",
                "autonomy_mode": "suggest"
            }
        )

out = Path("data/pilot_analytics_sidecar_events_100_scaffold.jsonl")
out.parent.mkdir(parents=True, exist_ok=True)

with out.open("w", encoding="utf-8") as f:
    for row in rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print(f"Wrote {len(rows)} events to {out}")

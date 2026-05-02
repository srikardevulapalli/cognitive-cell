from __future__ import annotations

import json
from pathlib import Path


events = [
    {
        "event_id": "pilot_growth_001",
        "source": "growth_ops_monitor",
        "event_type": "metric_anomaly",
        "statement": "Refund requests doubled after the pricing page update. What should we examine first?",
        "context": {
            "world_facts": [],
            "constraints": ["Prioritize high-signal first checks before broad analysis."],
            "active_goals": ["identify the first diagnostic step"],
        },
        "metadata": {"persona": "growth operations analyst", "time_pressure": "medium"},
        "interaction_mode": "workflow_component",
        "autonomy_mode": "suggest",
    },
    {
        "event_id": "pilot_support_001",
        "source": "support_queue_monitor",
        "event_type": "support_anomaly",
        "statement": "Support tickets about login issues are rising, but uptime is normal.",
        "context": {
            "world_facts": [],
            "constraints": ["Prioritize first diagnostic checks that separate user-facing friction from infrastructure outage."],
            "active_goals": ["identify where support analysis should start"],
        },
        "metadata": {"persona": "support operations analyst", "time_pressure": "medium"},
        "interaction_mode": "workflow_component",
        "autonomy_mode": "suggest",
    },
    {
        "event_id": "pilot_data_001",
        "source": "data_quality_monitor",
        "event_type": "data_freshness_anomaly",
        "statement": "The weekly ETL run completed, but downstream dashboards look stale.",
        "context": {
            "world_facts": [],
            "constraints": ["Prioritize checks that distinguish ETL completion from dashboard freshness."],
            "active_goals": ["identify the first diagnostic step"],
        },
        "metadata": {"persona": "data operations analyst", "time_pressure": "medium"},
        "interaction_mode": "workflow_component",
        "autonomy_mode": "suggest",
    },
]

out = Path("data/pilot_analytics_sidecar_events.jsonl")
with out.open("w", encoding="utf-8") as f:
    for event in events:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

print(f"Wrote {len(events)} events to {out}")

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def evt(
    event_id: str,
    source: str,
    event_type: str,
    statement: str,
    constraints: list[str],
    goals: list[str],
    persona: str,
    time_pressure: str = "medium",
    facts: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "event_id": event_id,
        "source": source,
        "event_type": event_type,
        "statement": statement,
        "context": {
            "world_facts": [
                {
                    "fact_id": f"f{i + 1}",
                    "fact_type": "world_fact",
                    "fact_text": fact,
                }
                for i, fact in enumerate(facts or [])
            ],
            "constraints": constraints,
            "active_goals": goals,
        },
        "metadata": {
            "persona": persona,
            "time_pressure": time_pressure,
        },
        "interaction_mode": "workflow_component",
        "autonomy_mode": "suggest",
    }


events = [
    # ------------------------------------------------------------------
    # Growth / product analytics anomalies
    # ------------------------------------------------------------------
    evt(
        "pilot_growth_001",
        "growth_ops_monitor",
        "metric_anomaly",
        "Refund requests doubled after the pricing page update. What should we examine first?",
        ["Prioritize high-signal first checks before broad analysis."],
        ["identify the first diagnostic step"],
        "growth operations analyst",
    ),
    evt(
        "pilot_growth_002",
        "growth_ops_monitor",
        "funnel_anomaly",
        "Trial signups rose but paid conversions dropped after a checkout change. Where should we look first?",
        ["Focus on the first likely conversion blocker."],
        ["identify checkout or activation friction"],
        "growth analyst",
    ),
    evt(
        "pilot_growth_003",
        "recommendation_monitor",
        "model_behavior_shift",
        "A new recommendation model improved clicks but lowered orders. What should we check first?",
        ["Avoid broad model speculation; prioritize funnel evidence."],
        ["find the first diagnostic check"],
        "product analytics lead",
    ),
    evt(
        "pilot_growth_004",
        "lifecycle_marketing_monitor",
        "campaign_anomaly",
        "An email campaign lifted opens but lowered purchases. What should we examine first?",
        ["Prioritize message-to-purchase mismatch checks."],
        ["identify where engagement stopped converting"],
        "lifecycle marketing analyst",
    ),
    evt(
        "pilot_growth_005",
        "organic_growth_monitor",
        "conversion_anomaly",
        "Search traffic is flat, but conversions from organic dropped sharply. Where should we start?",
        ["Separate traffic-quality issues from landing-page or funnel issues."],
        ["identify the first high-signal diagnostic step"],
        "growth analytics manager",
    ),
    evt(
        "pilot_growth_006",
        "checkout_monitor",
        "cart_anomaly",
        "Cart abandonment increased after we added a free-shipping banner.",
        ["Do not assume the banner is the only cause; start with highest-signal evidence."],
        ["find the first check for abandonment increase"],
        "checkout product analyst",
    ),
    evt(
        "pilot_growth_007",
        "payments_monitor",
        "support_metric_anomaly",
        "Payment failure logs look normal, but support complaints about checkout are rising.",
        ["Distinguish technical failure from user confusion."],
        ["identify the first investigation path"],
        "payments operations analyst",
    ),
    evt(
        "pilot_growth_008",
        "promotion_monitor",
        "usage_anomaly",
        "Promo code usage dropped after the coupon box was redesigned.",
        ["Prioritize UX discoverability checks."],
        ["find whether design change affected promo usage"],
        "commerce UX analyst",
    ),
    evt(
        "pilot_growth_009",
        "mobile_product_monitor",
        "mobile_funnel_anomaly",
        "Mobile add-to-cart rate dropped after product images were changed.",
        ["Start with mobile-specific visual and interaction checks."],
        ["identify first diagnostic check"],
        "mobile product analyst",
    ),
    evt(
        "pilot_growth_010",
        "subscription_monitor",
        "upgrade_anomaly",
        "Subscription upgrades slowed after pricing copy was rewritten.",
        ["Prioritize copy clarity and plan-comparison checks."],
        ["determine where upgrade intent is being lost"],
        "subscription growth analyst",
    ),

    # ------------------------------------------------------------------
    # Support / operations anomalies
    # ------------------------------------------------------------------
    evt(
        "pilot_support_001",
        "support_queue_monitor",
        "support_anomaly",
        "Support tickets about login issues are rising, but uptime is normal.",
        ["Prioritize first checks that separate user-facing friction from infrastructure outage."],
        ["identify where support analysis should start"],
        "support operations analyst",
    ),
    evt(
        "pilot_support_002",
        "support_quality_monitor",
        "quality_anomaly",
        "A new support macro reduced response time but increased reopen rates.",
        ["Prioritize quality-of-resolution checks over speed metrics."],
        ["find the first operational investigation step"],
        "support quality analyst",
    ),
    evt(
        "pilot_support_003",
        "warehouse_ops_monitor",
        "process_anomaly",
        "Warehouse pick speed improved but packing errors rose after a process change.",
        ["Avoid blaming staff first; inspect process and handoff changes."],
        ["identify the first process check"],
        "warehouse operations analyst",
    ),
    evt(
        "pilot_support_004",
        "inventory_monitor",
        "inventory_variance_anomaly",
        "Inventory variance widened after a warehouse process change. Where should analysis start?",
        ["Start with changes closest to transaction recording and handoff points."],
        ["identify likely variance source"],
        "inventory control analyst",
    ),
    evt(
        "pilot_support_005",
        "store_ops_monitor",
        "terminal_anomaly",
        "Payment terminals show intermittent network errors during peak checkout periods.",
        ["Prioritize customer-flow continuity and evidence collection."],
        ["identify first operational workaround or diagnostic"],
        "retail operations analyst",
        "high",
    ),
    evt(
        "pilot_support_006",
        "routing_policy_monitor",
        "service_quality_anomaly",
        "A new routing policy improved SLA but lowered customer satisfaction.",
        ["Prioritize whether speed came at the cost of issue fit or ownership."],
        ["identify first support quality check"],
        "customer operations analyst",
    ),
    evt(
        "pilot_support_007",
        "customer_success_monitor",
        "onboarding_anomaly",
        "Customer churn rose after we shortened the onboarding flow. Where do we look first?",
        ["Focus on removed onboarding steps and early confusion signals."],
        ["identify whether the shortened flow removed critical guidance"],
        "customer success analyst",
    ),
    evt(
        "pilot_support_008",
        "call_center_monitor",
        "escalation_anomaly",
        "Call hold times went down, but escalations increased.",
        ["Separate faster queue handling from lower first-contact resolution."],
        ["identify why faster calls are escalating more"],
        "call center operations analyst",
    ),
    evt(
        "pilot_support_009",
        "logistics_monitor",
        "delivery_complaint_anomaly",
        "Delivery delay complaints increased after switching carriers.",
        ["Prioritize carrier handoff and tracking visibility checks."],
        ["identify first logistics diagnostic"],
        "logistics operations analyst",
    ),
    evt(
        "pilot_support_010",
        "field_ops_monitor",
        "form_quality_anomaly",
        "Field technician notes became shorter and less useful after the mobile form update.",
        ["Prioritize form design and required-field behavior."],
        ["identify why note quality dropped"],
        "field operations analyst",
    ),

    # ------------------------------------------------------------------
    # Data pipeline / analytics reliability anomalies
    # ------------------------------------------------------------------
    evt(
        "pilot_data_001",
        "data_quality_monitor",
        "data_freshness_anomaly",
        "The weekly ETL run completed, but downstream dashboards look stale.",
        ["Prioritize checks that distinguish ETL completion from dashboard freshness."],
        ["identify the first diagnostic step"],
        "data operations analyst",
    ),
    evt(
        "pilot_data_002",
        "finance_data_monitor",
        "schema_anomaly",
        "The revenue dashboard changed after a schema rename, but the ETL job shows success.",
        ["Distinguish successful job execution from semantic field mapping issues."],
        ["identify the first data validation check"],
        "analytics engineer",
    ),
    evt(
        "pilot_data_003",
        "product_analytics_monitor",
        "reporting_anomaly",
        "Daily active users look flat, but the weekly report is missing rows.",
        ["Separate metric stability from report completeness."],
        ["identify the first data completeness check"],
        "product data analyst",
    ),
    evt(
        "pilot_data_004",
        "crm_sync_monitor",
        "data_freshness_anomaly",
        "The CRM export finished on time, but sales dashboards show yesterday's pipeline numbers.",
        ["Prioritize sync freshness and dashboard cache checks."],
        ["identify whether stale data is in source, warehouse, or dashboard"],
        "revenue operations analyst",
    ),
    evt(
        "pilot_data_005",
        "fraud_model_monitor",
        "model_input_shift",
        "Fraud model score distribution shifted after a feature pipeline update.",
        ["Prioritize input-feature validation before model retraining assumptions."],
        ["identify first model-monitoring check"],
        "risk analytics engineer",
    ),
    evt(
        "pilot_data_006",
        "cloud_cost_monitor",
        "cost_reporting_anomaly",
        "The warehouse cost report doubled after a partition configuration change.",
        ["Prioritize whether cost changed or reporting granularity changed."],
        ["identify the first cost anomaly check"],
        "data platform analyst",
    ),
    evt(
        "pilot_data_007",
        "forecasting_monitor",
        "forecast_anomaly",
        "The sales forecast job completed, but this week's numbers are identical to last week's.",
        ["Prioritize stale input and cached output checks."],
        ["identify first forecast pipeline diagnostic"],
        "forecasting analyst",
    ),
    evt(
        "pilot_data_008",
        "experimentation_monitor",
        "metric_validity_anomaly",
        "The experiment report shows a conversion rate above 100%.",
        ["Treat impossible metric values as data-quality issues first."],
        ["identify the first validation check"],
        "experimentation analyst",
        "high",
    ),
    evt(
        "pilot_data_009",
        "support_analytics_monitor",
        "taxonomy_anomaly",
        "Support trend dashboards became spiky after the ticket taxonomy changed.",
        ["Prioritize category mapping and historical comparability."],
        ["identify first taxonomy migration check"],
        "support data analyst",
    ),
    evt(
        "pilot_data_010",
        "billing_reconciliation_monitor",
        "reconciliation_anomaly",
        "Billing reconciliation mismatches increased after a timezone configuration change.",
        ["Prioritize date-boundary and timezone normalization checks."],
        ["identify first reconciliation diagnostic"],
        "billing data analyst",
        "high",
    ),
]

out = Path("data/pilot_analytics_sidecar_events_30.jsonl")
out.parent.mkdir(parents=True, exist_ok=True)

with out.open("w", encoding="utf-8") as f:
    for event in events:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

print(f"Wrote {len(events)} events to {out}")

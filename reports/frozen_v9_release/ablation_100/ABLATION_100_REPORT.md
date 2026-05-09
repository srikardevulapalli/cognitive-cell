# Cognitive Cell v9 — 100-Event Ablation Review

## Status

ablation_100_strong_pass

## Result

| Preferred output | Count | Rate |
|---|---:|---:|
| Full v9 | 44 | 0.44 |
| Baseline | 21 | 0.21 |
| Tie | 35 | 0.35 |

## Main metric

Full v9 was preferred or tied in:

~~~text
79 / 100 = 0.79
~~~

## Safety and usefulness

| Metric | Full v9 | Baseline |
|---|---:|---:|
| Useful first move | 1.00 | 1.00 |
| Too vague | 0.00 | 0.00 |
| Unsafe / overreaching | 0.00 | 0.00 |

## By group

~~~json
{
  "growth_product": {
    "count": 20,
    "preferred_output_counts": {
      "full_v9": 10,
      "tie": 6,
      "baseline": 4
    },
    "preferred_output_rates": {
      "full_v9": 0.5,
      "tie": 0.3,
      "baseline": 0.2
    },
    "full_v9_or_tie_rate": 0.8,
    "baseline_preferred_rate": 0.2,
    "full_v9_useful_rate": 1.0,
    "baseline_useful_rate": 1.0
  },
  "support_ops": {
    "count": 20,
    "preferred_output_counts": {
      "baseline": 6,
      "tie": 7,
      "full_v9": 7
    },
    "preferred_output_rates": {
      "baseline": 0.3,
      "tie": 0.35,
      "full_v9": 0.35
    },
    "full_v9_or_tie_rate": 0.7,
    "baseline_preferred_rate": 0.3,
    "full_v9_useful_rate": 1.0,
    "baseline_useful_rate": 1.0
  },
  "data_pipeline": {
    "count": 20,
    "preferred_output_counts": {
      "full_v9": 12,
      "tie": 7,
      "baseline": 1
    },
    "preferred_output_rates": {
      "full_v9": 0.6,
      "tie": 0.35,
      "baseline": 0.05
    },
    "full_v9_or_tie_rate": 0.95,
    "baseline_preferred_rate": 0.05,
    "full_v9_useful_rate": 1.0,
    "baseline_useful_rate": 1.0
  },
  "risk_compliance": {
    "count": 20,
    "preferred_output_counts": {
      "full_v9": 6,
      "tie": 7,
      "baseline": 7
    },
    "preferred_output_rates": {
      "full_v9": 0.3,
      "tie": 0.35,
      "baseline": 0.35
    },
    "full_v9_or_tie_rate": 0.65,
    "baseline_preferred_rate": 0.35,
    "full_v9_useful_rate": 1.0,
    "baseline_useful_rate": 1.0
  },
  "ops_process": {
    "count": 20,
    "preferred_output_counts": {
      "full_v9": 9,
      "tie": 8,
      "baseline": 3
    },
    "preferred_output_rates": {
      "full_v9": 0.45,
      "tie": 0.4,
      "baseline": 0.15
    },
    "full_v9_or_tie_rate": 0.85,
    "baseline_preferred_rate": 0.15,
    "full_v9_useful_rate": 1.0,
    "baseline_useful_rate": 1.0
  }
}
~~~

## Interpretation

Both systems were useful and safe, but full Cognitive Cell v9 was preferred or tied in most cases. This supports the claim that routing, pathway selection, and final rendering add value beyond a plain direct baseline in this curated enterprise sidecar pilot.

## Caveat

This is a curated pilot ablation with manual ratings. It is not a universal benchmark, not AGI evidence, and not a claim of universal superiority over frontier models.

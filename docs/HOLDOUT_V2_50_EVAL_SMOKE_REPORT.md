# Holdout-v2 50-Case Evaluation Smoke

## Status

Borderline.

## Result

| Preferred output | Count | Rate |
|---|---:|---:|
| Full v9 | 23 | 0.46 |
| Baseline | 24 | 0.48 |
| Tie | 3 | 0.06 |

Full v9 preferred or tied:

~~~text
26 / 50 = 0.52
~~~

## Metrics

| Metric | Full v9 | Baseline |
|---|---:|---:|
| Useful first move | 1.00 | 1.00 |
| Contract correct | 0.92 | 1.00 |
| Unsafe / overreaching | 0.00 | 0.00 |

Full v9 trace useful rate:

~~~text
0.98
~~~

## Interpretation

The smoke result is borderline. Full v9 remains useful and safe, but the plain direct baseline is highly competitive on the broader holdout-v2 distribution.

Full v9 is strongest on workflow/contextual/enterprise-style tasks and weaker on planning, persona adaptation, timing, tutoring, and writing.

## Decision

Do not run the full 500-case evaluation yet. Diagnose weak families first.

# v10-dev 20-Case Evaluation Smoke

## Status

v10 patch not justified yet.

## Result

| Preferred output | Count | Rate |
|---|---:|---:|
| Full v9 | 11 | 0.55 |
| Baseline | 5 | 0.25 |
| Tie | 4 | 0.20 |

Full v9 was preferred or tied in:

~~~text
15 / 20 = 0.75
~~~

## Metrics

| Metric | Full v9 | Baseline |
|---|---:|---:|
| Useful first move | 1.00 | 1.00 |
| Contract correct | 0.90 | 1.00 |
| Unsafe / overreaching | 0.00 | 0.00 |

Full v9 trace useful rate:

~~~text
1.00
~~~

## Interpretation

The v10-dev smoke did not strongly reproduce the holdout-v2 weak-family problem. Full v9 remained preferred or tied in most sampled cases.

The clearest remaining weakness is planning concreteness: in several planning cases, the plain direct baseline gave a sharper first step.

## Decision

Do not patch v10 yet.

If more confidence is needed, expand to a 50-case v10-dev evaluation before changing runtime behavior.

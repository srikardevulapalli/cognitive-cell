# Cost Control Plan

## Rule

Use API calls only for generating CognitiveCellV9 outputs.

Do not use API calls for:
- human review columns
- pilot scoring
- preference ratings
- notes
- summary interpretation
- manual adjudication

## Workflow

1. Generate a small batch of sidecar outputs.
2. Convert outputs to review CSV.
3. Upload the review CSV for manual rating.
4. Summarize locally.
5. Only expand if the previous batch passes.

## Current pilot ladder

~~~text
3-event pilot: passed
5-event smoke: next
30-event pilot: only after 5-event smoke passes
100-event pilot: only after 30-event pilot passes
~~~

## Cost-saving practices

- Use cached/resumable batch runner.
- Never rerun events already generated.
- Use small smoke tests before full batches.
- Upload CSVs for manual rating instead of using judge models.

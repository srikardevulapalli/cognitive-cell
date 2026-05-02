# Quickstart Validation

## Validated commands

~~~bash
python -m pip install -e .
python examples/v9_import_demo.py
python examples/v9_basic_demo.py
python examples/v9_urgent_context_demo.py
python examples/v9_enterprise_sidecar_demo.py
python examples/v9_planning_demo.py
python scripts/audit_v9_demo_outputs.py --dir reports/demo_outputs_v9_release --summary reports/demo_outputs_v9_release/audit_summary.json
python -m pytest -q
~~~

## Expected result

- Import demo works.
- Live demos return final response, selected pathway, and trace.
- Demo audit has `failure_count = 0`.
- Tests pass.

## Current status

Cognitive Cell v9 is a usable package skeleton with live examples.

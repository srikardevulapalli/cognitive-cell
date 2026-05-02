# Contributing

Thank you for considering contributing to Cognitive Cell.

## Project scope

Cognitive Cell is a context-sensitive workflow control layer.

It is not AGI, not a production-autonomous agent, and not a claim of universal superiority over frontier models.

## Development setup

~~~bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[server,dev]"
python -m pytest -q
~~~

## No-cost checks

~~~bash
python scripts/public_smoke_test.py
cognitive-cell --help
python -m uvicorn cognitive_cell.server.app:app --port 8000
curl -s http://127.0.0.1:8000/health
~~~

## Cost note

Do not add tests that require model calls by default.

Model-backed tests should be opt-in.

## Design principle

Preserve the separation:

~~~text
routing → selection → final rendering
~~~

Do not hard-code domain workflows into the core control layer.

# Quickstart

## 1. Install

~~~bash
python -m venv .venv
source .venv/bin/activate
pip install "cognitive-cell[server]"
~~~

## 2. Verify import without model calls

~~~bash
python - <<'PY'
from cognitive_cell import CognitiveCellRequest, CognitiveCellV9
from cognitive_cell.server.app import app

print(CognitiveCellRequest(statement="Blue colour is observed."))
print(CognitiveCellV9)
print(app.title)
PY
~~~

## 3. Start HTTP sidecar

~~~bash
python -m uvicorn cognitive_cell.server.app:app --port 8000
~~~

## 4. Check health

~~~bash
curl -s http://127.0.0.1:8000/health
~~~

Expected:

~~~json
{"status":"ok"}
~~~

## 5. Run a model-backed request

Set your API key first:

~~~bash
export OPENAI_API_KEY="your_key_here"
~~~

Then run:

~~~bash
cognitive-cell --event-json examples/event.example.json
~~~

or POST to:

~~~text
POST /v1/sidecar
~~~

## Cost note

`/health` costs nothing.

`/v1/sidecar` and CLI requests call the configured model.

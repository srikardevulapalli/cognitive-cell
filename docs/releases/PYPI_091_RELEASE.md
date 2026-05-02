# Cognitive Cell v0.9.1 PyPI Release

## Status

Real PyPI install passed.

## Package

~~~text
cognitive-cell==0.9.1
~~~

## Verified

~~~bash
pip install "cognitive-cell[server]==0.9.1"
~~~

Verified:

- `from cognitive_cell import CognitiveCellRequest, CognitiveCellV9`
- `from cognitive_cell.server.app import app`
- `cognitive-cell --help`
- server import: `Cognitive Cell v9 Sidecar`

## Scope

Cognitive Cell is a context-sensitive workflow control layer.

It is not AGI, not a production-autonomous agent, and not a claim of universal superiority over frontier models.

## Accepted stack

~~~text
router-v4 → selector-v5 → finalizer-v9
~~~

## Safe result claim

On a fresh 100-case holdout, the frozen v9 cognitive-cell stack beat a plain strong-model baseline under two standardized OpenAI judges, with mean architecture preference around 0.589.

# Next Actions After Import Works

## Current state

The clean release package imports:

~~~python
from cognitive_cell.lego import CognitiveCellRequest, CognitiveCellV9
~~~

## Next engineering milestone

Make this work:

~~~bash
python examples/v9_basic_demo.py
~~~

and return a real response, not only an import test.

## Implementation order

1. Convert selector-v5 script into importable library code.
2. Convert finalizer-v9 script into importable library code.
3. Create `cell_v9.py` orchestration.
4. Wire `CognitiveCellV9.run()` to `cell_v9.py`.
5. Create four runnable demos.
6. Only then return to evaluation.

## Do not do yet

- Do not create v10.
- Do not run more 100-case judge loops.
- Do not tune on holdout-v1 again.
- Do not add enterprise integrations before the local API works.

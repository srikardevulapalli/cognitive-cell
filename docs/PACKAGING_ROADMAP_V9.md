# Packaging Roadmap for Cognitive Cell v9

## Goal

Make CognitiveCellV9 usable by another developer in under 10 minutes.

## Accepted stack

~~~text
router-v4 → selector-v5 → finalizer-v9
~~~

##ules to finish

### 1. selector_v5.py

Move selector logic from script form into a stable library function.

Expected function:

~~~python
select_candidate(...) -> dict
~~~

### 2. finalizer_v9.py

Move finalizer logic from script form into a stable library function.

Expected function:

~~~python
render_final_response(...) -> dict
~~~

### 3. cell_v9.py

Create the orchestration layer:

~~~text
request
→ router-v4
→ workflow candidate
→ direct candidate
→ selector-v5
→ finalizer-v9
→ response + trace
~~~

### 4. examples

Create:

~~~text
examples/v9_basic_demo.py
examples/v9_observation_log_demo.py
examples/v9_enterprise_sidecar_demo.py
examples/v9_context_shift_demo.py
~~~

## Do not do

- Do not patch router-v4.
- Do not patch selector-v5.
- Do not create v10.
- Do not tune on holdout-v1 again.

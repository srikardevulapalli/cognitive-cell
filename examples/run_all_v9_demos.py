from __future__ import annotations

import subprocess
import sys

DEMOS = [
    "examples/v9_import_demo.py",
    "examples/v9_basic_demo.py",
    "examples/v9_urgent_context_demo.py",
    "examples/v9_enterprise_sidecar_demo.py",
    "examples/v9_planning_demo.py",
]

for demo in DEMOS:
    print("=" * 100)
    print(demo)
    print("=" * 100)
    completed = subprocess.run([sys.executable, demo], check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)

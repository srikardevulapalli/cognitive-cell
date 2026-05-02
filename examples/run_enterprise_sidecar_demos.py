from __future__ import annotations

import subprocess
import sys

DEMOS = [
    "examples/v9_sidecar_json_payload_demo.py",
    "examples/v9_enterprise_event_adapter_demo.py",
]

for demo in DEMOS:
    print("=" * 100)
    print(demo)
    print("=" * 100)
    result = subprocess.run([sys.executable, demo], check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

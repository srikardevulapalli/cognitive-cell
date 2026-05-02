from __future__ import annotations

import json
from pathlib import Path


def exists(path: str) -> bool:
    return Path(path).exists()


manifest = {
    "release": "cognitive-cell-v9",
    "status": "usable_package_skeleton_with_enterprise_sidecar",
    "accepted_stack": {
        "router": "router-v4",
        "selector": "selector-v5",
        "finalizer": "finalizer-v9",
    },
    "validated_commands": [
        "python examples/v9_import_demo.py",
        "python examples/v9_basic_demo.py",
        "python examples/v9_urgent_context_demo.py",
        "python examples/v9_enterprise_sidecar_demo.py",
        "python examples/v9_planning_demo.py",
        "python examples/v9_sidecar_json_payload_demo.py",
        "python examples/v9_enterprise_event_adapter_demo.py",
        "python scripts/audit_v9_demo_outputs.py --dir reports/demo_outputs_v9_release --summary reports/demo_outputs_v9_release/audit_summary.json",
        "python scripts/audit_enterprise_sidecar_outputs.py --dir reports/enterprise_sidecar_demo_outputs --summary reports/enterprise_sidecar_demo_outputs/audit_summary.json",
        "python -m pytest -q",
    ],
    "key_files": {
        "readme": exists("README.md"),
        "quickstart_validation": exists("docs/QUICKSTART_VALIDATION.md"),
        "enterprise_integration_guide": exists("docs/ENTERPRISE_INTEGRATION_GUIDE.md"),
        "v9_api": exists("src/cognitive_cell/lego/v9_api.py"),
        "cell_v9": exists("src/cognitive_cell/lego/cell_v9.py"),
        "selector_v5": exists("src/cognitive_cell/lego/selector_v5.py"),
        "finalizer_v9": exists("src/cognitive_cell/lego/finalizer_v9.py"),
        "enterprise_adapter": exists("src/cognitive_cell/lego/enterprise_adapter.py"),
    },
    "safe_claim": "On a fresh 100-case holdout, the frozen v9 cognitive-cell stack beat a plain strong-model baseline under two standardized OpenAI judges, with mean architecture preference around 0.589.",
    "cautions": [
        "This is an engineering validation result, not universal proof.",
        "The final holdout used same-provider OpenAI judges.",
        "Observation/log and contextual observation remain known weak spots.",
        "Do not claim AGI or broad superiority over frontier models.",
    ],
    "next_phase": [
        "Choose one narrow enterprise pilot.",
        "Create holdout-v2 with 500 cases.",
        "Run ablations.",
        "Add human evaluation.",
        "Prepare technical report.",
    ],
}

out = Path("reports/frozen_v9_release/release_manifest.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

print(json.dumps(manifest, ensure_ascii=False, indent=2))
print(f"Wrote {out}")

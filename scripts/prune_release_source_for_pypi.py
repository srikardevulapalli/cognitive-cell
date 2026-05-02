from __future__ import annotations

from pathlib import Path
import shutil

KEEP = {
    "src/cognitive_cell/__init__.py",
    "src/cognitive_cell/lego/__init__.py",
    "src/cognitive_cell/lego/v9_api.py",
    "src/cognitive_cell/lego/cell_v9.py",
    "src/cognitive_cell/lego/selector_v5.py",
    "src/cognitive_cell/lego/finalizer_v9.py",
    "src/cognitive_cell/lego/enterprise_adapter.py",
}

root = Path("src/cognitive_cell")

for path in list(root.rglob("*")):
    if path.is_file():
        rel = str(path)
        if rel not in KEEP:
            print(f"Removing file: {rel}")
            path.unlink()

for path in sorted(root.rglob("*"), reverse=True):
    if path.is_dir() and not any(path.iterdir()):
        print(f"Removing empty dir: {path}")
        path.rmdir()

print("Pruned release source for PyPI.")

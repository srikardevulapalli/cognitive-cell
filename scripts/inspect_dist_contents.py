from __future__ import annotations

import tarfile
import zipfile
from pathlib import Path


BAD_MARKERS = [
    ".venv",
    "OPENAI_API_KEY",
    "GEMINI_API_KEY",
    ".env",
    "reports/",
    "runs/",
    "pilot_analytics_sidecar_outputs",
    "pairwise_judge",
    "frozen_v9",
    "__pycache__",
]


def inspect_wheel(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as z:
        return sorted(z.namelist())


def inspect_sdist(path: Path) -> list[str]:
    with tarfile.open(path) as t:
        return sorted(t.getnames())


def main() -> int:
    dist = Path("dist")
    files = sorted(dist.glob("*"))

    if not files:
        raise SystemExit("No files in dist/. Run python -m build first.")

    failed = False

    for artifact in files:
        print("=" * 100)
        print(artifact)

        if artifact.suffix == ".whl":
            names = inspect_wheel(artifact)
        elif artifact.suffixes[-2:] == [".tar", ".gz"] or artifact.name.endswith(".tar.gz"):
            names = inspect_sdist(artifact)
        else:
            print("Skipping unknown artifact type")
            continue

        for name in names:
            print(name)

        bad = [
            name
            for name in names
            for marker in BAD_MARKERS
            if marker in name
        ]

        if bad:
            failed = True
            print("\nBAD FILES FOUND:")
            for item in bad:
                print("  ", item)

    if failed:
        raise SystemExit("Distribution contains files that should not be published.")

    print("\nDistribution contents look clean.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--n", type=int, required=True)
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        line
        for line in input_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    selected = lines[: args.n]
    output_path.write_text("\n".join(selected) + "\n", encoding="utf-8")

    print(f"Wrote {len(selected)} rows to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

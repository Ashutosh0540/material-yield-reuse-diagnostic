"""Command line entry point for synthetic material reuse screening."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from .decision import evaluate


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python -m src.evaluate <input.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        result = evaluate(payload)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

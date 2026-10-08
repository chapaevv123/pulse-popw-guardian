from __future__ import annotations

import argparse
import json
from pathlib import Path

from .verifier import verify_bundle


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify a Konnex-style PoPW evidence bundle")
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    result = verify_bundle(json.loads(args.bundle.read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=True))


if __name__ == "__main__":
    main()

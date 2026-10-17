"""Fail unless `semgrep --test --json` ran and passed every rule file under a folder.

`semgrep --test` exits 0 when a rule file fails to load, so a broken rule would pass CI.
This reads its JSON and also checks that each rule file reported results.

Usage: semgrep --test --json DIR > results.json; python3 check_tests.py results.json DIR
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def problems(results: dict, rule_files: list[Path]) -> list[str]:
    found: list[str] = []
    for error in results.get("config_with_errors", []):
        last_line = error["error"].strip().splitlines()[-1]
        found.append(f"{error['filename']}: failed to load: {last_line}")
    for path in results.get("config_missing_tests", []):
        found.append(f"{path}: no test file next to it")
    reported = {Path(path).resolve(): checks for path, checks in results.get("results", {}).items()}
    for rule_file in rule_files:
        checks = reported.get(rule_file.resolve())
        if checks is None:
            found.append(f"{rule_file}: no test results")
            continue
        for rule_id, check in checks["checks"].items():
            if not check["passed"] or check.get("errors"):
                found.append(f"{rule_file}: {rule_id} failed")
    return found


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    results = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    rule_files = sorted(p for p in Path(argv[2]).rglob("*.yml") if p.is_file())
    found = problems(results, rule_files)
    for message in found:
        print(f"::error title=Semgrep rule tests::{message}")
    if found:
        return 1
    print(f"All {len(rule_files)} rule files passed their tests.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

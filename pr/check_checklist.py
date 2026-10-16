"""Check a PR description against the checklist in the standard PR template.

Every checklist item in the template must appear in the PR body. Each must be ticked, or left
unticked with an explanation after the item text. Anything else fails.

Usage: PR_BODY="..." python3 check_checklist.py path/to/pull_request_template.md
Stdlib only, so it runs on a bare runner.
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass

CHECKBOX = re.compile(r"^\s*[-*]\s+\[(?P<mark>[ xX])\]\s+(?P<text>.+?)\s*$")


@dataclass(frozen=True)
class Result:
    errors: list[str]
    warnings: list[str]


def normalize(text: str) -> str:
    return " ".join(text.split()).casefold()


def required_items(template: str) -> list[str]:
    return [m["text"] for line in template.splitlines() if (m := CHECKBOX.match(line))]


def check(template: str, body: str) -> Result:
    items = required_items(template)
    if not items:
        return Result(errors=["The PR template has no checklist items."], warnings=[])

    boxes = [(m["mark"] != " ", m["text"]) for line in body.splitlines() if (m := CHECKBOX.match(line))]
    errors: list[str] = []
    warnings: list[str] = []
    for item in items:
        want = normalize(item)
        found = next(((ticked, text) for ticked, text in boxes if normalize(text).startswith(want)), None)
        if found is None:
            errors.append(f"Missing checklist item: {item}")
            continue
        ticked, text = found
        if ticked:
            continue
        reason = normalize(text)[len(want) :].strip(" .,;:-–—()")
        if reason:
            warnings.append(f"Unticked, with a reason: {text}")
        else:
            errors.append(f"Unticked with no reason: {item}. Tick it, or explain why after the item.")
    return Result(errors=errors, warnings=warnings)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as f:
        template = f.read()
    result = check(template, os.environ.get("PR_BODY", ""))
    for message in result.warnings:
        print(f"::warning title=PR checklist::{message}")
    for message in result.errors:
        print(f"::error title=PR checklist::{message}")
    if result.errors:
        print("Edit the PR description to fix the checklist; this check reruns on edit.")
        return 1
    print("PR checklist complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

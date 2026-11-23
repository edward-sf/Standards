"""Decide task acceptance, merge or release from a change record and protected policy."""
import argparse
import json
import re
import sys
from pathlib import Path

REVISION = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")


def check(policy, record, decision):
    rules = policy["decisions"].get(decision)
    if not isinstance(rules, dict):
        raise ValueError(f"{decision} is not a configured decision")
    revision = record["revision"]
    if not isinstance(revision, str) or not REVISION.fullmatch(revision):
        raise ValueError("record must name the full revision under decision")

    latest = {}
    for item in record["evidence"]:
        if item["revision"] == revision:
            latest[item["name"]] = item["result"]
    required = list(rules["evidence"])
    if rules.get("criteria"):
        criteria = record["criteria"]
        if not criteria:
            raise ValueError("no acceptance criteria recorded")
        required += [criterion["evidence"] for criterion in criteria]
    for name in required:
        if latest.get(name) != "pass":
            raise ValueError(f"{name}: no passing result on this revision")

    author = record["author"]
    for role, count in rules["approvals"].items():
        members = policy["roles"][role]
        if not isinstance(count, int) or count < 1:
            raise ValueError(f"{role}: approval count must be a positive integer")
        approvers = {item["reviewer"] for item in record["approvals"]
                     if item["revision"] == revision and item["reviewer"] in members
                     and (item["reviewer"] != author or rules.get("allow_author") is True)}
        if len(approvers) < count:
            raise ValueError(f"{role}: {len(approvers)} of {count} approval(s) on this revision")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policy", type=Path)
    parser.add_argument("record", type=Path)
    parser.add_argument("--decision", required=True)
    args = parser.parse_args()
    try:
        policy, record = [json.loads(path.read_text(encoding="utf-8"))
                          for path in (args.policy, args.record)]
        check(policy, record, args.decision)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        sys.exit(f"not done: {error}")


if __name__ == "__main__":
    main()

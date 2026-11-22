"""Allow deployment only of a gated, immutable artifact in the configured promotion order."""
import argparse
import json
import re
import sys
from pathlib import Path

DIGEST = re.compile(r"sha256:[0-9a-f]{64}")
REVISION = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
STATUSES = {"verified", "failed"}


def names(policy, key):
    values = policy.get(key)
    if (not isinstance(values, list) or not values or len(set(values)) != len(values)
            or not all(isinstance(value, str) and value for value in values)):
        raise ValueError(f"policy {key} must be a non-empty list of distinct names")
    return values


def check(policy, record, environment, artifact):
    checks = names(policy, "checks")
    environments = names(policy, "environments")
    if environment not in environments:
        raise ValueError(f"{environment} is not a configured environment")
    if not DIGEST.fullmatch(artifact) or record.get("artifact") != artifact:
        raise ValueError("deployment must name the recorded sha256 artifact digest")
    revision = record.get("revision")
    if not isinstance(revision, str) or not REVISION.fullmatch(revision):
        raise ValueError("record must name the full source revision")

    latest = {}
    for entry in record["checks"]:
        if entry.get("revision") != revision or entry.get("artifact") != artifact:
            raise ValueError(f"{entry.get('name')}: result recorded for another revision or artifact")
        latest[entry["name"]] = entry["conclusion"]
    for name in checks:
        if name not in latest:
            raise ValueError(f"{name}: no result")
        if latest[name] != "success":
            raise ValueError(f"{name}: latest result is {latest[name]}")

    deployed = {}
    for entry in record["deployments"]:
        if entry["environment"] not in environments or entry["status"] not in STATUSES:
            raise ValueError("unknown deployment environment or status")
        deployed[entry["environment"]] = entry["status"]
    if deployed.get(environment) == "failed":
        raise ValueError(f"artifact failed its last deployment to {environment}")
    position = environments.index(environment)
    if position:
        previous = environments[position - 1]
        if deployed.get(previous) != "verified":
            raise ValueError(f"artifact is not verified in {previous}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policy", type=Path)
    parser.add_argument("record", type=Path)
    parser.add_argument("--environment", required=True)
    parser.add_argument("--artifact", required=True)
    args = parser.parse_args()
    try:
        policy, record = [json.loads(path.read_text(encoding="utf-8"))
                          for path in (args.policy, args.record)]
        check(policy, record, args.environment, args.artifact)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        sys.exit(f"promotion rejected: {error}")


if __name__ == "__main__":
    main()

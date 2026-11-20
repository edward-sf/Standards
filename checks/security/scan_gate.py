"""Reject incomplete scanner evidence or any configured blocking result."""
import argparse
import json
import sys
from pathlib import Path


def check(report, tool):
    if not isinstance(report, dict) or report.get("version") != "2.1.0":
        raise ValueError("expected SARIF 2.1.0")
    runs = report.get("runs")
    if not isinstance(runs, list) or not runs:
        raise ValueError("no scan runs")
    for run in runs:
        if not isinstance(run, dict) or run.get("externalPropertyFileReferences"):
            raise ValueError("expected a self-contained scan run")
        driver = run["tool"]["driver"]["name"]
        if driver != tool:
            raise ValueError("unexpected scanner")
        invocations = run.get("invocations")
        if not isinstance(invocations, list) or not invocations:
            raise ValueError("missing execution evidence")
        if not all(isinstance(item, dict) and item.get("executionSuccessful") is True
                   for item in invocations):
            raise ValueError("scanner execution incomplete")
        results = run.get("results")
        if not isinstance(results, list):
            raise ValueError("missing results")
        if results:
            raise ValueError(f"{len(results)} blocking scanner result(s)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--tool", required=True)
    args = parser.parse_args()
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
        check(report, args.tool)
    except (OSError, ValueError, KeyError, TypeError) as error:
        sys.exit(f"scan rejected: {error}")


if __name__ == "__main__":
    main()

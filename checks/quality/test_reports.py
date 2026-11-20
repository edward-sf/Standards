"""Check fresh JUnit reports and an optional Cobertura line-coverage floor."""
import argparse
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction


def check_suites(paths, required):
    passed = set()
    for path in paths:
        root = ET.parse(path).getroot()
        if root.tag not in {"testsuites", "testsuite"}:
            raise ValueError(f"{path}: expected JUnit XML")
        cases = root.findall(".//testcase")
        if not cases:
            raise ValueError(f"{path}: no test cases")
        for suite in root.iter():
            if suite.tag in {"testsuite", "testsuites"}:
                if any(int(suite.get(key, "0")) != 0 for key in ("errors", "failures")):
                    raise ValueError(f"{path}: suite reports failures or errors")
        for case in cases:
            name = case.attrib["name"]
            identity = f"{case.get('classname', '')}::{name}"
            if case.find("error") is not None or case.find("failure") is not None:
                raise ValueError(f"{path}: {identity} failed")
            if case.find("skipped") is not None:
                if identity in required:
                    raise ValueError(f"{path}: {identity} skipped")
            else:
                passed.add(identity)
    missing = required - passed
    if missing:
        raise ValueError("missing required cases: " + ", ".join(sorted(missing)))


def check_coverage(path, threshold):
    root = ET.parse(path).getroot()
    if root.tag != "coverage":
        raise ValueError("expected Cobertura coverage XML")
    covered = int(root.attrib["lines-covered"])
    total = int(root.attrib["lines-valid"])
    floor = Fraction(threshold)
    if total <= 0 or not 0 <= covered <= total or not 0 <= floor <= 100:
        raise ValueError("invalid coverage counts or floor")
    if covered * 100 < floor * total:
        raise ValueError(f"{covered}/{total} lines covered, below {threshold}%")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reports", nargs="+")
    parser.add_argument("--case", action="append", required=True, dest="cases")
    parser.add_argument("--coverage")
    parser.add_argument("--minimum")
    args = parser.parse_args()
    if (args.coverage is None) != (args.minimum is None):
        parser.error("--coverage and --minimum must be supplied together")
    try:
        check_suites(args.reports, set(args.cases))
        if args.coverage is not None:
            check_coverage(args.coverage, args.minimum)
    except (OSError, ValueError, KeyError, ZeroDivisionError, ET.ParseError) as error:
        sys.exit(f"test evidence rejected: {error}")


if __name__ == "__main__":
    main()

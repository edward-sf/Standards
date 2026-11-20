"""Compare one protected read's observed responses and logs with its contract."""
import argparse
import json
import sys
from pathlib import Path


DENIAL = {401, 403, 404}
CASES = {"owner", "anonymous", "invalid", "other"}


def validate(contract, observed, log, private_marker, log_marker):
    if not private_marker or not log_marker or private_marker == log_marker:
        raise ValueError("supply distinct nonempty fixture markers")
    for document in (contract, observed):
        if not isinstance(document, dict) or set(document) != CASES:
            raise ValueError("missing or unexpected access cases")
    for case in sorted(CASES):
        for document in (contract, observed):
            response = document[case]
            if not isinstance(response, dict) or set(response) != {"status", "body"}:
                raise ValueError(f"{case}: expected status and body")
            if type(response["status"]) is not int:
                raise ValueError(f"{case}: expected integer status")
        expected = contract[case]
        permitted = {200} if case == "owner" else DENIAL
        if expected["status"] not in permitted:
            raise ValueError(f"{case}: invalid contract status")
        # JSON serialization distinguishes true from 1, including nested fields.
        actual = json.dumps(observed[case], sort_keys=True, ensure_ascii=False, allow_nan=False)
        wanted = json.dumps(expected, sort_keys=True, ensure_ascii=False, allow_nan=False)
        if actual != wanted or private_marker in actual:
            raise ValueError(f"{case}: response violates the public contract")
    if log_marker not in log or private_marker in log:
        raise ValueError("captured log failed the fixture marker checks")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path)
    parser.add_argument("observations", type=Path)
    parser.add_argument("log", type=Path)
    parser.add_argument("--private-marker", required=True)
    parser.add_argument("--log-marker", required=True)
    args = parser.parse_args()
    try:
        validate(json.loads(args.contract.read_text(encoding="utf-8")),
                 json.loads(args.observations.read_text(encoding="utf-8")),
                 args.log.read_text(encoding="utf-8"), args.private_marker, args.log_marker)
    except (OSError, ValueError) as error:
        sys.exit(f"access evidence rejected: {error}")


if __name__ == "__main__":
    main()

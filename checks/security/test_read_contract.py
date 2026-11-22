"""Run with python3 checks/security/test_read_contract.py."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class AccessCases(unittest.TestCase):
    def test_gate(self):
        expected = {
            "owner": {"status": 200, "body": {"id": "fixture-a", "display_name": "Ada"}},
            "anonymous": {"status": 401, "body": {"error": "unauthenticated"}},
            "invalid": {"status": 401, "body": {"error": "unauthenticated"}},
            "other": {"status": 404, "body": {"error": "not_found"}},
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            policy, observation, log = [root / name for name in ("policy", "observed", "log")]
            policy.write_text(json.dumps(expected))
            command = [sys.executable, str(Path(__file__).with_name("read_contract.py")),
                       str(policy), str(observation), str(log),
                       "--private-marker", "PRIVATE_FIXTURE", "--log-marker", "request-57"]
            for label, actual, message, code in [
                ("correct", expected, "handled request-57", 0),
                ("missing access check", dict(expected, other=expected["owner"]), "request-57", 1),
                ("denies owner", dict(expected, owner=expected["other"]), "request-57", 1),
                ("missing invalid token case", {k: v for k, v in expected.items() if k != "invalid"}, "request-57", 1),
                ("extra field", dict(expected, owner={"status": 200, "body": {"id": "fixture-a", "internal": 1}}), "request-57", 1),
                ("private log", expected, "request-57 PRIVATE_FIXTURE", 1),
                ("wrong log", expected, "", 1),
            ]:
                with self.subTest(label=label):
                    observation.write_text(json.dumps(actual))
                    log.write_text(message)
                    result = subprocess.run(command, capture_output=True)
                    self.assertEqual(result.returncode, code, result.stderr)


if __name__ == "__main__":
    unittest.main()

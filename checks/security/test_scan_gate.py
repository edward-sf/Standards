"""Run with python3 checks/security/test_scan_gate.py."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ScanCases(unittest.TestCase):
    def test_client_decisions(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "scan.sarif"
            for driver in ("credential-scanner", "dependency-auditor"):
                clean = {"tool": {"driver": {"name": driver}}, "results": [],
                         "invocations": [{"executionSuccessful": True}]}
                finding = {"ruleId": "fixture-rule", "message": {"text": "FIXTURE_PRIVATE_81"}}
                cases = [
                    ("clean", [clean], 0),
                    ("finding in second run", [clean, dict(clean, results=[finding])], 1),
                    ("no run", [], 1),
                    ("missing result list", [{k: v for k, v in clean.items() if k != "results"}], 1),
                    ("failed invocation", [dict(clean, invocations=[{"executionSuccessful": False}])], 1),
                    ("wrong scanner", [dict(clean, tool={"driver": {"name": "other"}})], 1),
                    ("external data", [dict(clean, externalPropertyFileReferences={"results": [{}]})], 1),
                ]
                for label, runs, expected in cases:
                    with self.subTest(driver=driver, label=label):
                        report.write_text(json.dumps({"version": "2.1.0", "runs": runs}))
                        result = subprocess.run([sys.executable, str(Path(__file__).with_name("scan_gate.py")),
                                                 str(report), "--tool", driver], capture_output=True)
                        self.assertEqual(result.returncode, expected, result.stderr)
                        self.assertNotIn(b"FIXTURE_PRIVATE_81", result.stderr)


if __name__ == "__main__":
    unittest.main()

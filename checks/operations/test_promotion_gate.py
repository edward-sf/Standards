"""Run with python3 checks/operations/test_promotion_gate.py."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REVISION = "a" * 40
CANDIDATE = "sha256:" + "1" * 64
PREVIOUS = "sha256:" + "0" * 64
CHECKS = ["build", "test", "lint", "validate", "credential-scan", "dependency-audit"]
POLICY = {"checks": CHECKS, "environments": ["staging", "production"]}


def record(artifact=CANDIDATE, deployments=()):
    return {"artifact": artifact, "revision": REVISION,
            "checks": [{"name": name, "revision": REVISION, "artifact": artifact,
                        "conclusion": "success"} for name in CHECKS],
            "deployments": [{"environment": env, "status": status} for env, status in deployments]}


def changed(base, edit):
    result = copy.deepcopy(base)
    edit(result)
    return result


class PromotionCases(unittest.TestCase):
    def test_client_decisions(self):
        staged = record(deployments=[("staging", "verified")])
        failed_audit = {"name": "dependency-audit", "revision": REVISION,
                        "artifact": CANDIDATE, "conclusion": "failure"}
        cases = [
            ("first environment", POLICY, record(), "staging", CANDIDATE, 0),
            ("verified in staging", POLICY, staged, "production", CANDIDATE, 0),
            ("rollback to verified release", POLICY,
             record(PREVIOUS, [("staging", "verified"), ("production", "verified")]),
             "production", PREVIOUS, 0),
            ("skipped staging", POLICY, record(), "production", CANDIDATE, 1),
            ("staging deployment failed", POLICY,
             record(deployments=[("staging", "verified"), ("staging", "failed")]),
             "production", CANDIDATE, 1),
            ("missing check", POLICY, changed(staged, lambda r: r["checks"].pop()),
             "production", CANDIDATE, 1),
            ("later check failure", POLICY,
             changed(staged, lambda r: r["checks"].append(failed_audit)), "production", CANDIDATE, 1),
            ("check on other revision", POLICY,
             changed(staged, lambda r: r["checks"][1].update(revision="b" * 40)),
             "production", CANDIDATE, 1),
            ("check on other artifact", POLICY,
             changed(staged, lambda r: r["checks"][1].update(artifact=PREVIOUS)),
             "production", CANDIDATE, 1),
            ("deploying different digest", POLICY, staged, "production", PREVIOUS, 1),
            ("failed in target environment", POLICY,
             record(deployments=[("staging", "verified"), ("production", "failed")]),
             "production", CANDIDATE, 1),
            ("unknown environment", POLICY, staged, "qa", CANDIDATE, 1),
            ("unknown deployment status", POLICY,
             record(deployments=[("staging", "ok")]), "production", CANDIDATE, 1),
            ("mutable artifact reference", POLICY, record("registry/app:latest"),
             "staging", "registry/app:latest", 1),
            ("duplicate policy check", dict(POLICY, checks=CHECKS + ["test"]),
             record(), "staging", CANDIDATE, 1),
            ("empty policy", {"checks": [], "environments": []}, record(), "staging", CANDIDATE, 1),
        ]
        with tempfile.TemporaryDirectory() as directory:
            policy_path = Path(directory) / "policy.json"
            record_path = Path(directory) / "record.json"
            for label, policy, evidence, environment, artifact, expected in cases:
                with self.subTest(label=label):
                    policy_path.write_text(json.dumps(policy))
                    record_path.write_text(json.dumps(evidence))
                    result = subprocess.run(
                        [sys.executable, str(Path(__file__).with_name("promotion_gate.py")),
                         str(policy_path), str(record_path),
                         "--environment", environment, "--artifact", artifact],
                        capture_output=True)
                    self.assertEqual(result.returncode, expected, result.stderr)
                    if expected:
                        self.assertIn(b"promotion rejected", result.stderr)


if __name__ == "__main__":
    unittest.main()

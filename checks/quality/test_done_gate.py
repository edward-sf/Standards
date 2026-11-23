"""Run with python3 checks/quality/test_done_gate.py."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HEAD = "b" * 40
OLD = "a" * 40
POLICY = {
    "roles": {"reviewer": ["lee", "sam"], "release-owner": ["kim"]},
    "decisions": {
        "task": {"criteria": True, "evidence": [], "approvals": {"reviewer": 1}},
        "merge": {"criteria": False, "evidence": ["tests", "docs"], "approvals": {"reviewer": 1}},
        "release": {"criteria": False, "evidence": ["promotion"], "approvals": {"release-owner": 1}},
    },
}


def evidence(name, result="pass", revision=HEAD):
    return {"name": name, "revision": revision, "result": result}


def approval(reviewer, revision=HEAD):
    return {"reviewer": reviewer, "revision": revision}


RECORD = {
    "author": "dana", "revision": HEAD,
    "criteria": [{"id": "AC1", "evidence": "tests"}, {"id": "AC2", "evidence": "docs"}],
    "evidence": [evidence("tests"), evidence("docs"), evidence("promotion")],
    "approvals": [approval("lee"), approval("kim")],
}


def changed(base, edit):
    result = copy.deepcopy(base)
    edit(result)
    return result


class DoneCases(unittest.TestCase):
    def test_client_decisions(self):
        solo = changed(POLICY, lambda p: p["decisions"]["merge"].update(allow_author=True))
        cases = [
            ("task accepted", POLICY, RECORD, "task", 0),
            ("merge", POLICY, RECORD, "merge", 0),
            ("release", POLICY, RECORD, "release", 0),
            ("permitted self-review", solo,
             changed(RECORD, lambda r: r.update(author="lee")), "merge", 0),
            ("approval on earlier revision", POLICY,
             changed(RECORD, lambda r: r["approvals"][0].update(revision=OLD)), "merge", 1),
            ("author approves own change", POLICY,
             changed(RECORD, lambda r: r.update(author="lee")), "merge", 1),
            ("approver lacks role", POLICY,
             changed(RECORD, lambda r: r["approvals"].__setitem__(0, approval("pat"))), "merge", 1),
            ("same reviewer twice", changed(POLICY, lambda p: p["decisions"]["merge"]["approvals"]
                                            .update(reviewer=2)),
             changed(RECORD, lambda r: r["approvals"].append(approval("lee"))), "merge", 1),
            ("release owner not reviewer", POLICY,
             changed(RECORD, lambda r: r["approvals"].pop()), "release", 1),
            ("missing evidence", POLICY,
             changed(RECORD, lambda r: r["evidence"].pop(1)), "merge", 1),
            ("later failure", POLICY,
             changed(RECORD, lambda r: r["evidence"].append(evidence("docs", "fail"))), "merge", 1),
            ("evidence from earlier revision", POLICY,
             changed(RECORD, lambda r: r["evidence"][0].update(revision=OLD)), "merge", 1),
            ("criterion without passing evidence", POLICY,
             changed(RECORD, lambda r: r["criteria"][1].update(evidence="changelog")), "task", 1),
            ("no criteria", POLICY, changed(RECORD, lambda r: r.update(criteria=[])), "task", 1),
            ("unknown decision", POLICY, RECORD, "deploy", 1),
            ("unknown role", changed(POLICY, lambda p: p["decisions"]["merge"]["approvals"]
                                     .update(owner=1)), RECORD, "merge", 1),
            ("short revision", POLICY, changed(RECORD, lambda r: r.update(revision="bbbbbbb")),
             "merge", 1),
        ]
        with tempfile.TemporaryDirectory() as directory:
            policy_path = Path(directory) / "policy.json"
            record_path = Path(directory) / "record.json"
            for label, policy, record, decision, expected in cases:
                with self.subTest(label=label):
                    policy_path.write_text(json.dumps(policy))
                    record_path.write_text(json.dumps(record))
                    result = subprocess.run(
                        [sys.executable, str(Path(__file__).with_name("done_gate.py")),
                         str(policy_path), str(record_path), "--decision", decision],
                        capture_output=True)
                    self.assertEqual(result.returncode, expected, result.stderr)
                    if expected:
                        self.assertIn(b"not done", result.stderr)


if __name__ == "__main__":
    unittest.main()

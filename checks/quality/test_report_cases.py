"""Run with python3 checks/quality/test_report_cases.py."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ReportCases(unittest.TestCase):
    def test_merge_decisions(self):
        with tempfile.TemporaryDirectory() as directory:
            suite = Path(directory) / "test.xml"
            coverage = Path(directory) / "coverage.xml"
            command = [sys.executable, str(Path(__file__).with_name("test_reports.py")),
                       str(suite), "--case", "API::duplicate",
                       "--coverage", str(coverage), "--minimum", "80"]
            for outcome, name, hits, total, expected in [
                ("", "duplicate", 4, 5, 0),
                ("", "duplicate", 3, 5, 1),
                ("", "unrelated", 5, 5, 1),
                ("<skipped/>", "duplicate", 5, 5, 1),
                ("<failure/>", "duplicate", 5, 5, 1),
                ("", "duplicate", 0, 0, 1),
            ]:
                with self.subTest(outcome=outcome, name=name, hits=hits, total=total):
                    suite.write_text(f'<testsuite><testcase classname="API" name="{name}">'
                                     f'{outcome}</testcase></testsuite>')
                    coverage.write_text(f'<coverage lines-covered="{hits}" lines-valid="{total}"/>')
                    result = subprocess.run(command, capture_output=True)
                    self.assertEqual(result.returncode, expected, result.stderr)


if __name__ == "__main__":
    unittest.main()

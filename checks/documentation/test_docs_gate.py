"""Exercise merge decisions against actual Git revisions."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class DocumentationCases(unittest.TestCase):
    def test_walkthrough(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args):
                return subprocess.check_output(["git", *args], cwd=root)

            def commit():
                git("add", ".")
                git("commit", "-qm", "fixture")

            def write(path, text):
                file = root / path
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(text)

            git("init", "-q")
            git("config", "user.name", "Fixture")
            git("config", "user.email", "fixture@example.invalid")
            for path in ["README.md", "docs/api.md", "CHANGELOG.md", "contracts/v1.json"]:
                write(path, "baseline\n")
            commit()
            base = git("rev-parse", "HEAD").decode().strip()
            gate = [sys.executable, str(Path(__file__).with_name("docs_gate.py").resolve()),
                    base, "HEAD", "--readme", "README.md", "--api-doc", "docs/api.md",
                    "--changelog", "CHANGELOG.md", "--api-pattern", "contracts/*.json",
                    "--adr-dir", "docs/decisions"]

            def decision(expected):
                result = subprocess.run(gate, cwd=root, capture_output=True)
                self.assertEqual(result.returncode, expected, result.stderr)

            decision(0)
            write("contracts/v1.json", '{"page_token":"optional"}\n')
            commit()
            decision(1)
            write("docs/api.md", "Pass the next page token.\n")
            write("CHANGELOG.md", "Added cursor pagination.\n")
            commit()
            decision(0)
            record = ("## Status\nAccepted\n## Context\nConcurrent writes\n## Alternatives\n"
                      "Offset and cursor\n## Decision\nCursor\n## Consequences\nStable ordering key\n")
            write("docs/decisions/001.md", record.replace("Accepted", "Superseded")
                  + "## Superseded by\n002.md\n")
            commit()
            decision(1)
            write("docs/decisions/002.md", record)
            commit()
            decision(0)
            write("docs/decisions/002.md", record.replace("Accepted", "Superseded")
                  + "## Superseded by\n001.md\n")
            commit()
            decision(1)
            write("docs/decisions/002.md", record.replace("## Alternatives", "## Notes"))
            commit()
            decision(1)
            write("docs/decisions/002.md", record)
            write("README.md", "\n")
            commit()
            decision(1)


if __name__ == "__main__":
    unittest.main()

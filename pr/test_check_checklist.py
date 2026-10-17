"""Tests for check_checklist.py. Run: python3 -m unittest discover -s pr"""

import unittest
from pathlib import Path

from check_checklist import check, required_items

TEMPLATE = (Path(__file__).parent.parent / ".github" / "pull_request_template.md").read_text(encoding="utf-8")
ITEMS = required_items(TEMPLATE)


def body(*lines: str) -> str:
    return "## What changed\n\nStuff.\n\n## Checklist\n\n" + "\n".join(lines) + "\n"


def all_ticked() -> list[str]:
    return [f"- [x] {item}" for item in ITEMS]


class CheckChecklistTest(unittest.TestCase):
    def test_template_has_items(self) -> None:
        self.assertEqual(len(ITEMS), 5)

    def test_all_ticked_passes(self) -> None:
        result = check(TEMPLATE, body(*all_ticked()))
        self.assertEqual(result.errors, [])
        self.assertEqual(result.warnings, [])

    def test_capital_x_and_asterisk_bullets_pass(self) -> None:
        lines = [f"* [X] {item}" for item in ITEMS]
        self.assertEqual(check(TEMPLATE, body(*lines)).errors, [])

    def test_ticked_with_trailing_note_passes(self) -> None:
        lines = all_ticked()
        lines[0] += " (`bash run.sh`, all green)"
        self.assertEqual(check(TEMPLATE, body(*lines)).errors, [])

    def test_whitespace_and_case_differences_pass(self) -> None:
        lines = all_ticked()
        lines[1] = "- [x]   new behavior HAS tests;  bug fixes start with a failing test"
        self.assertEqual(check(TEMPLATE, body(*lines)).errors, [])

    def test_unticked_with_reason_warns(self) -> None:
        lines = all_ticked()
        lines[1] = f"- [ ] {ITEMS[1]} (init skill is untested, see above)"
        result = check(TEMPLATE, body(*lines))
        self.assertEqual(result.errors, [])
        self.assertEqual(len(result.warnings), 1)

    def test_unticked_without_reason_fails(self) -> None:
        lines = all_ticked()
        lines[2] = f"- [ ] {ITEMS[2]}"
        result = check(TEMPLATE, body(*lines))
        self.assertEqual(len(result.errors), 1)
        self.assertIn("no reason", result.errors[0])

    def test_unticked_with_only_punctuation_fails(self) -> None:
        lines = all_ticked()
        lines[2] = f"- [ ] {ITEMS[2]} ()."
        self.assertEqual(len(check(TEMPLATE, body(*lines)).errors), 1)

    def test_missing_item_fails(self) -> None:
        result = check(TEMPLATE, body(*all_ticked()[:-1]))
        self.assertEqual(len(result.errors), 1)
        self.assertIn("Missing", result.errors[0])

    def test_empty_body_fails_every_item(self) -> None:
        self.assertEqual(len(check(TEMPLATE, "").errors), len(ITEMS))

    def test_item_mentioned_in_prose_does_not_count(self) -> None:
        prose = "I confirm: " + ITEMS[0]
        result = check(TEMPLATE, body(prose, *all_ticked()[1:]))
        self.assertEqual(len(result.errors), 1)

    def test_template_without_items_fails(self) -> None:
        self.assertEqual(len(check("## Checklist\n", body(*all_ticked())).errors), 1)

    def test_crlf_body_passes(self) -> None:
        self.assertEqual(check(TEMPLATE, body(*all_ticked()).replace("\n", "\r\n")).errors, [])


if __name__ == "__main__":
    unittest.main()

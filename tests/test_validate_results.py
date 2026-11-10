import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))

from validate_results import validate  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures"
SCRIPT = ROOT / "tests" / "validate_results.py"


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class ValidateRecordsTest(unittest.TestCase):
    def test_valid_fixture_has_no_errors(self):
        errors, warnings = validate(load("valid.json"))
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_invalid_fixture_reports_errors(self):
        errors, _ = validate(load("invalid.json"))
        joined = "\n".join(errors)
        self.assertIn("missing required field 'target_url'", joined)
        self.assertIn("invalid status", joined)
        self.assertIn("relevance_score", joined)
        self.assertIn("timestamp", joined)

    def test_root_must_be_array(self):
        errors, _ = validate({"not": "a list"})
        self.assertEqual(errors, ["root element must be a JSON array"])

    def test_empty_log_is_valid(self):
        self.assertEqual(validate([]), ([], []))

    def test_non_object_record_is_rejected(self):
        errors, _ = validate(["just a string"])
        self.assertIn("record[0]: must be a JSON object", errors)

    def test_success_requires_posted_url(self):
        record = load("valid.json")[0]
        record.pop("posted_url")
        errors, _ = validate([record])
        self.assertIn("record[0]: successful record must include posted_url", errors)

    def test_duplicate_domain_warns(self):
        record = load("valid.json")[0]
        errors, warnings = validate([record, dict(record, posted_url="https://example.com/x", status="pending")])
        self.assertEqual(errors, [])
        self.assertTrue(any("duplicate domain" in w for w in warnings))

    def test_success_without_screenshot_warns(self):
        record = load("valid.json")[0]
        record.pop("screenshot")
        errors, warnings = validate([record])
        self.assertEqual(errors, [])
        self.assertTrue(any("screenshot" in w for w in warnings))

    def test_skip_without_notes_warns(self):
        record = load("valid.json")[0]
        record.update(status="skipped", posted_url="", notes="")
        errors, warnings = validate([record])
        self.assertEqual(errors, [])
        self.assertTrue(any("should explain why" in w for w in warnings))


class CliTest(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_cli_valid_exit_zero(self):
        result = self.run_cli(FIXTURES / "valid.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK:", result.stdout)

    def test_cli_invalid_exit_two(self):
        result = self.run_cli(FIXTURES / "invalid.json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("FAIL:", result.stdout)

    def test_cli_missing_file_exit_two(self):
        result = self.run_cli(FIXTURES / "does-not-exist.json")
        self.assertEqual(result.returncode, 2)

    def test_cli_broken_json_exit_two(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            handle.write("{not json")
            path = handle.name
        result = self.run_cli(path)
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid JSON", result.stdout)

    def test_cli_strict_turns_warnings_into_failure(self):
        record = load("valid.json")[0]
        record.pop("screenshot")
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
            json.dump([record], handle)
            path = handle.name
        self.assertEqual(self.run_cli(path).returncode, 0)
        self.assertEqual(self.run_cli("--strict", path).returncode, 1)


if __name__ == "__main__":
    unittest.main()

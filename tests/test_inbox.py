import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import inbox  # noqa: E402


class InboxHelpersTest(unittest.TestCase):
    def test_matches_sender_and_subject(self):
        message = {
            "from": {"address": "noreply@directory.example"},
            "subject": "Verify your email address",
        }
        self.assertTrue(inbox.matches(message, "directory.example", None))
        self.assertTrue(inbox.matches(message, None, "verify"))
        self.assertTrue(inbox.matches(message, "directory", "email"))
        self.assertFalse(inbox.matches(message, "other.example", None))
        self.assertFalse(inbox.matches(message, None, "password"))

    def test_matches_is_case_insensitive(self):
        message = {"from": {"address": "NoReply@Example.COM"}, "subject": "VERIFY"}
        self.assertTrue(inbox.matches(message, "example.com", "verify"))

    def test_otp_pattern(self):
        self.assertEqual(inbox.OTP_PATTERN.findall("Your code is 748291."), ["748291"])
        self.assertEqual(inbox.OTP_PATTERN.findall("Order 12345678 shipped"), ["12345678"])
        self.assertEqual(inbox.OTP_PATTERN.findall("No code here"), [])

    def test_load_identity_accepts_bom(self):
        payload = {
            "provider": "mail.tm",
            "email": "inbox@example.com",
            "password": "secret",
            "api_base": "https://api.mail.tm",
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "identity.json"
            path.write_text("\ufeff" + json.dumps(payload), encoding="utf-8")
            loaded = inbox.load_identity(path)
            self.assertEqual(loaded["email"], "inbox@example.com")

    def test_load_identity_rejects_missing_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "identity.json"
            path.write_text(json.dumps({"email": "inbox@example.com"}), encoding="utf-8")
            with self.assertRaises(SystemExit):
                inbox.load_identity(path)


if __name__ == "__main__":
    unittest.main()

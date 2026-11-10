import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENGINES = ROOT / "data" / "search-engines.json"

LOCALES = {"en", "uk", "ru", "es", "fr", "de", "it", "pt", "zh", "ja", "pl", "vi"}
INDEXES = {"own", "api", "indexnow", "bing", "google", "yandex-google", "metasearch"}
METHODS = {"account", "form", "email", "api", "none"}


class SearchEnginesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(ENGINES.read_text(encoding="utf-8"))

    def test_is_non_empty_list(self):
        self.assertIsInstance(self.data, list)
        self.assertGreater(len(self.data), 0)

    def test_ids_are_unique(self):
        ids = [engine["id"] for engine in self.data]
        self.assertEqual(len(ids), len(set(ids)))

    def test_required_fields(self):
        for engine in self.data:
            with self.subTest(engine=engine.get("id")):
                for field in ("id", "name", "locales", "index", "submission_url", "method", "account_required", "captcha"):
                    self.assertIn(field, engine)
                self.assertIsInstance(engine["locales"], list)
                self.assertTrue(engine["locales"])
                self.assertTrue(set(engine["locales"]).issubset(LOCALES))
                self.assertIn(engine["index"], INDEXES)
                self.assertIn(engine["method"], METHODS)
                self.assertIsInstance(engine["account_required"], bool)
                self.assertIsInstance(engine["captcha"], bool)

    def test_submission_url_shape(self):
        for engine in self.data:
            url = engine["submission_url"]
            if url is None:
                self.assertEqual(engine["method"], "none", engine["id"])
            else:
                self.assertTrue(
                    url.startswith("https://") or url.startswith("mailto:"),
                    f"{engine['id']}: {url}",
                )

    def test_core_engines_present(self):
        ids = {engine["id"] for engine in self.data}
        for required in ("google", "bing", "indexnow", "yandex", "baidu", "coccoc"):
            self.assertIn(required, ids)

    def test_every_locale_is_covered(self):
        covered = set()
        for engine in self.data:
            if engine["method"] in {"account", "form", "api"}:
                covered.update(engine["locales"])
        self.assertEqual(covered, LOCALES)


if __name__ == "__main__":
    unittest.main()

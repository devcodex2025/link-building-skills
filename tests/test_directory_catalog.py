import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "data" / "directory-catalog.md"


class DirectoryCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = CATALOG.read_text(encoding="utf-8")
        cls.rows = []
        for line in cls.text.splitlines():
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != 5:
                continue
            if cells[0] == "#" or set(cells[0]) <= {"-", ":", " "}:
                continue
            cls.rows.append(cells)

    def test_catalog_exists(self):
        self.assertTrue(CATALOG.exists())
        self.assertGreater(CATALOG.stat().st_size, 50_000)

    def test_has_at_least_one_thousand_entries(self):
        self.assertGreaterEqual(len(self.rows), 1000, f"only {len(self.rows)} entries")

    def test_every_entry_has_a_submission_url(self):
        for cells in self.rows:
            with self.subTest(entry=cells[1]):
                self.assertTrue(cells[4].startswith("http"), cells[4])

    def test_urls_are_unique(self):
        urls = [cells[4].rstrip("/").lower() for cells in self.rows]
        self.assertEqual(len(urls), len(set(urls)))

    def test_sections_are_present(self):
        for heading in ("## Verified no-login entries", "## Free directories", "## Paid directories"):
            self.assertIn(heading, self.text)

    def test_no_cyrillic(self):
        self.assertIsNone(re.search(r"[\u0400-\u04FF]", self.text))


if __name__ == "__main__":
    unittest.main()

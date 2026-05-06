import datetime as dt
import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "compile-wiki"
    / "scripts"
    / "ingest_url.py"
)

spec = importlib.util.spec_from_file_location("ingest_url", SCRIPT)
ingest_url = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ingest_url)


class IngestUrlTests(unittest.TestCase):
    def test_html_to_markdown_extracts_readable_content(self):
        html = """
        <html>
          <head>
            <title>Test Page</title>
            <style>.hidden { display: none; }</style>
          </head>
          <body>
            <nav>Navigation should be skipped</nav>
            <h1>Heading</h1>
            <p>Hello <strong>world</strong>.</p>
            <ul>
              <li>First item</li>
              <li>Second item</li>
            </ul>
            <script>alert("skip me")</script>
          </body>
        </html>
        """

        title, markdown = ingest_url.html_to_markdown(html)

        self.assertEqual(title, "Test Page")
        self.assertIn("# Heading", markdown)
        self.assertIn("Hello world.", markdown)
        self.assertIn("- First item", markdown)
        self.assertIn("- Second item", markdown)
        self.assertNotIn("Navigation should be skipped", markdown)
        self.assertNotIn("skip me", markdown)

    def test_save_raw_note_uses_title_slug_and_deduplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            fetched = dt.date(2026, 5, 6)

            first = ingest_url.save_raw_note(
                vault,
                "https://example.com/articles/test",
                "A Test Page",
                "Body text",
                fetched,
            )
            second = ingest_url.save_raw_note(
                vault,
                "https://example.com/articles/test",
                "A Test Page",
                "More body text",
                fetched,
            )

            self.assertEqual(first.relative_to(vault).as_posix(), "raw/a-test-page.md")
            self.assertEqual(second.relative_to(vault).as_posix(), "raw/a-test-page-2.md")
            content = first.read_text(encoding="utf-8")
            self.assertIn('source: "https://example.com/articles/test"', content)
            self.assertIn('fetched: "2026-05-06"', content)
            self.assertIn("# A Test Page", content)
            self.assertIn("Body text", content)

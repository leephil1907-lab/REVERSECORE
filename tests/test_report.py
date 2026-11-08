import tempfile
import unittest
from pathlib import Path

from reversecore.report import write_report

class ReportTests(unittest.TestCase):
    def test_html_report_escapes_sample_strings(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            target = root / "sample.bin"
            target.write_bytes(b"<script>alert('x')</script>")
            output = root / "report.html"
            write_report(target, output)
            content = output.read_text()
            self.assertIn("&lt;script&gt;", content)
            self.assertNotIn("<script>alert", content)

    def test_json_report(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            target = root / "sample.bin"
            target.write_bytes(b"report sample")
            output = root / "report.json"
            write_report(target, output, "json")
            self.assertIn('"report_schema_version": 1', output.read_text())

if __name__ == "__main__":
    unittest.main()

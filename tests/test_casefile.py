import json
import tempfile
import unittest
from pathlib import Path

from reversecore.casefile import add_note, create_case

class CaseFileTests(unittest.TestCase):
    def test_create_case_and_append_note(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            target = root / "sample.bin"
            target.write_bytes(b"case sample")
            case_dir = root / "case-001"
            manifest = create_case(target, case_dir)
            self.assertEqual(manifest["target"]["name"], "sample.bin")
            self.assertTrue((case_dir / "intake-report.json").is_file())
            event = add_note(case_dir, "Reviewed static metadata")
            self.assertEqual(event["event"], "analyst_note")
            lines = (case_dir / "evidence.jsonl").read_text().splitlines()
            self.assertEqual(json.loads(lines[0])["note"], "Reviewed static metadata")

if __name__ == "__main__":
    unittest.main()

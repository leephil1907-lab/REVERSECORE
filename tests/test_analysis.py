import tempfile
import unittest
from pathlib import Path

from reversecore.analysis import entropy, extract_strings, identify, inspect_file

class AnalysisTests(unittest.TestCase):
    def test_identifies_elf(self):
        self.assertEqual(identify(b"\x7fELF" + b"\x00" * 20), "ELF executable or shared object")

    def test_strings(self):
        self.assertIn("hello world", extract_strings(b"\x00hello world\x00", minimum=5))

    def test_entropy_empty(self):
        self.assertEqual(entropy(b""), 0.0)

    def test_inspect_hash(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "sample.bin"
            target.write_bytes(b"sample payload")
            report = inspect_file(target)
            self.assertEqual(len(report["sha256"]), 64)
            self.assertEqual(report["size_bytes"], 14)

if __name__ == "__main__":
    unittest.main()

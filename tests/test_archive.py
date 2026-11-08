import tempfile
import unittest
import zipfile
from pathlib import Path

from reversecore.archive import safe_extract_zip

class ArchiveTests(unittest.TestCase):
    def test_rejects_parent_traversal(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            archive_path = root / "bad.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("../escape.txt", "bad")
            with self.assertRaises(ValueError):
                safe_extract_zip(archive_path, root / "out")

    def test_enforces_expanded_size_limit(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            archive_path = root / "large.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("payload.txt", "123456789")
            with self.assertRaises(ValueError):
                safe_extract_zip(archive_path, root / "out", max_total_bytes=4)

if __name__ == "__main__":
    unittest.main()

import struct
import tempfile
import unittest
from pathlib import Path

from reversecore.binary_formats import FormatError, parse_dex, parse_elf, parse_macho, parse_pe

class BinaryFormatTests(unittest.TestCase):
    def write(self, data):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        path = Path(folder.name) / "sample.bin"
        path.write_bytes(data)
        return path

    def test_minimal_pe32_plus(self):
        data = bytearray(0x80 + 24 + 0xF0)
        data[:2] = b"MZ"
        struct.pack_into("<I", data, 0x3C, 0x80)
        data[0x80:0x84] = b"PE\0\0"
        struct.pack_into("<HHIIIHH", data, 0x84, 0x8664, 0, 0, 0, 0, 0xF0, 0x22)
        struct.pack_into("<H", data, 0x98, 0x20B)
        struct.pack_into("<I", data, 0x98 + 16, 0x1000)
        struct.pack_into("<Q", data, 0x98 + 24, 0x140000000)
        report = parse_pe(self.write(data))
        self.assertEqual(report["format"], "PE32+")
        self.assertEqual(report["entry_point_rva"], 0x1000)

    def test_minimal_elf64(self):
        data = bytearray(64)
        data[:4] = bytes([127]) + b"ELF"
        data[4:6] = bytes([2, 1])
        struct.pack_into("<HHIQQQIHHHHHH", data, 16, 2, 62, 1, 0x401000, 64, 0, 0, 64, 56, 0, 64, 0, 0)
        report = parse_elf(self.write(data))
        self.assertEqual(report["format"], "ELF64")
        self.assertEqual(report["machine"], 62)

    def test_minimal_macho64(self):
        data = bytearray(32)
        data[:4] = bytes([0xCF, 0xFA, 0xED, 0xFE])
        struct.pack_into("<IIIIII", data, 4, 0x01000007, 3, 2, 0, 0, 0)
        self.assertEqual(parse_macho(self.write(data))["format"], "Mach-O 64-bit")

    def test_minimal_dex(self):
        data = bytearray(0x70)
        data[:8] = b"dex\n035\0"
        struct.pack_into("<III", data, 0x20, 0x70, 0x70, 0x12345678)
        struct.pack_into("<II", data, 0x38, 0, 0)
        report = parse_dex(self.write(data))
        self.assertEqual(report["format"], "DEX")
        self.assertEqual(report["string_id_count"], 0)

    def test_truncated_pe_is_rejected(self):
        with self.assertRaises(FormatError):
            parse_pe(self.write(b"MZ" + bytes(10)))

if __name__ == "__main__":
    unittest.main()

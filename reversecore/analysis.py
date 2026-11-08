"""Static file inspection primitives; no target execution occurs here."""
from __future__ import annotations

import hashlib
import math
import os
import re
import struct
from pathlib import Path
from typing import Any

MAGIC = [
    (b"\x7fELF", "ELF executable or shared object"),
    (b"MZ", "DOS/Windows PE candidate"),
    (b"\xca\xfe\xba\xbe", "Mach-O fat binary or Java class"),
    (b"\xfe\xed\xfa\xce", "Mach-O 32-bit"),
    (b"\xfe\xed\xfa\xcf", "Mach-O 64-bit"),
    (b"\xce\xfa\xed\xfe", "Mach-O 32-bit (little-endian)"),
    (b"\xcf\xfa\xed\xfe", "Mach-O 64-bit (little-endian)"),
    (b"PK\x03\x04", "ZIP archive (may be APK/JAR/ZIP)"),
    (b"\x1f\x8b", "GZIP archive"),
    (b"\x7f\x45\x4c\x46", "ELF executable or shared object"),
    (b"SQLite format 3\x00", "SQLite database"),
]

def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()

def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = [0] * 256
    for value in data:
        counts[value] += 1
    length = len(data)
    return -sum((count / length) * math.log2(count / length) for count in counts if count)

def identify(data: bytes) -> str:
    for magic, label in MAGIC:
        if data.startswith(magic):
            if magic == b"MZ":
                return "DOS/Windows PE candidate (validate PE header)"
            return label
    if data.startswith(b"<!DOCTYPE html") or data.startswith(b"<html"):
        return "HTML document"
    if data.lstrip().startswith((b"{", b"[")):
        return "JSON/text candidate"
    return "Unknown or unrecognized data"

def extract_strings(data: bytes, minimum: int = 5, limit: int = 5000) -> list[str]:
    if minimum < 2:
        raise ValueError("minimum string length must be at least 2")
    found: list[str] = []
    pattern = rb"[\x20-\x7e]{" + str(minimum).encode() + rb",}"
    found.extend(item.decode("ascii", "replace") for item in re.findall(pattern, data))
    # Common UTF-16LE printable text.
    wide = re.findall(rb"(?:[\x20-\x7e]\x00){" + str(minimum).encode() + rb",}", data)
    found.extend(item[::2].decode("ascii", "replace") for item in wide)
    return list(dict.fromkeys(found))[:limit]

def inspect_file(path_value: str | Path, include_strings: bool = True) -> dict[str, Any]:
    path = Path(path_value).expanduser()
    if not path.exists():
        raise FileNotFoundError(path)
    if not path.is_file():
        raise ValueError(f"not a regular file: {path}")
    stat = path.stat()
    with path.open("rb") as handle:
        head = handle.read(4096)
    result: dict[str, Any] = {
        "path": str(path.resolve()),
        "name": path.name,
        "size_bytes": stat.st_size,
        "sha256": sha256_file(path),
        "file_type": identify(head),
        "entropy_sample_bits_per_byte": round(entropy(head), 4),
    }
    if head.startswith(b"\x7fELF") and len(head) >= 20:
        result["format_details"] = {
            "endianness": "little" if head[5] == 1 else "big" if head[5] == 2 else "unknown",
            "class": {1: "32-bit", 2: "64-bit"}.get(head[4], "unknown"),
            "machine_id": struct.unpack("<H" if head[5] == 1 else ">H", head[18:20])[0] if head[5] in (1, 2) else None,
        }
    if include_strings:
        with path.open("rb") as handle:
            data = handle.read(8 * 1024 * 1024)
        result["strings_sample"] = extract_strings(data)
        result["strings_count_sampled"] = len(result["strings_sample"])
        result["strings_scanned_bytes"] = len(data)
        result["strings_scan_truncated"] = stat.st_size > len(data)
    return result

"""Safe ZIP inventory and extraction helpers."""
from __future__ import annotations

import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

def inventory_zip(path: str | Path) -> list[dict[str, Any]]:
    with zipfile.ZipFile(path) as archive:
        return [
            {"name": item.filename, "size_bytes": item.file_size,
             "compressed_bytes": item.compress_size, "is_directory": item.is_dir()}
            for item in archive.infolist()
        ]

def safe_extract_zip(path: str | Path, destination: str | Path, max_total_bytes: int = 512 * 1024 * 1024) -> list[str]:
    target = Path(destination).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    with zipfile.ZipFile(path) as archive:
        total_size = sum(item.file_size for item in archive.infolist() if not item.is_dir())
        if total_size > max_total_bytes:
            raise ValueError(f"archive expands to {total_size} bytes; limit is {max_total_bytes}")
        for item in archive.infolist():
            member = PurePosixPath(item.filename)
            if member.is_absolute() or ".." in member.parts:
                raise ValueError(f"unsafe archive member path: {item.filename}")
            output = (target / Path(*member.parts)).resolve()
            if output != target and target not in output.parents:
                raise ValueError(f"archive member escapes destination: {item.filename}")
            if item.is_dir():
                output.mkdir(parents=True, exist_ok=True)
                continue
            output.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(item) as source, output.open("wb") as sink:
                while True:
                    chunk = source.read(1024 * 1024)
                    if not chunk:
                        break
                    sink.write(chunk)
            written.append(str(output))
    return written

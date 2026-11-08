"""APK package inventory and lightweight DEX triage."""
from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path
from typing import Any

from .analysis import extract_strings

def inspect_apk(path_value: str | Path) -> dict[str, Any]:
    path = Path(path_value).expanduser()
    if not path.is_file():
        raise FileNotFoundError(path)
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    digest_hex = digest.hexdigest()
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        manifest_name = "AndroidManifest.xml"
        dex_entries = [name for name in names if name == "classes.dex" or (
            name.startswith("classes") and name.endswith(".dex") and name[7:-4].isdigit()
        )]
        native_entries = [name for name in names if name.startswith("lib/") and name.endswith(".so")]
        dex_report = []
        for name in dex_entries:
            info = archive.getinfo(name)
            dex_digest = hashlib.sha256()
            sample = bytearray()
            with archive.open(name) as dex_handle:
                while True:
                    chunk = dex_handle.read(1024 * 1024)
                    if not chunk:
                        break
                    dex_digest.update(chunk)
                    if len(sample) < 16 * 1024 * 1024:
                        sample.extend(chunk[:16 * 1024 * 1024 - len(sample)])
            dex_report.append({
                "name": name,
                "size_bytes": info.file_size,
                "sha256": dex_digest.hexdigest(),
                "strings_sample": extract_strings(bytes(sample), minimum=5, limit=1000),
                "strings_scanned_bytes": len(sample),
                "strings_scan_truncated": info.file_size > len(sample),
            })
        manifest_format = "missing"
        manifest_preview = None
        if manifest_name in names:
            manifest = archive.read(manifest_name)
            if manifest.lstrip().startswith(b"<?xml") or manifest.lstrip().startswith(b"<manifest"):
                manifest_format = "plain XML"
                manifest_preview = manifest[:12000].decode("utf-8", "replace")
            else:
                manifest_format = "binary Android XML"
        return {
            "path": str(path.resolve()),
            "size_bytes": path.stat().st_size,
            "sha256": digest_hex,
            "manifest": {"present": manifest_name in names, "format": manifest_format,
                         "xml_preview": manifest_preview},
            "dex_files": dex_report,
            "native_libraries": native_entries,
            "asset_count": sum(1 for name in names if name.startswith("assets/")),
            "entry_count": len(names),
            "note": "Static package inventory only; no APK code is executed.",
        }

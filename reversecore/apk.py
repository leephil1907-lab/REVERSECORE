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
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
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
            sample = archive.read(name)
            dex_report.append({
                "name": name,
                "size_bytes": info.file_size,
                "sha256": hashlib.sha256(sample).hexdigest(),
                "strings_sample": extract_strings(sample, minimum=5, limit=1000),
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
            "sha256": digest,
            "manifest": {"present": manifest_name in names, "format": manifest_format,
                         "xml_preview": manifest_preview},
            "dex_files": dex_report,
            "native_libraries": native_entries,
            "asset_count": sum(1 for name in names if name.startswith("assets/")),
            "entry_count": len(names),
            "note": "Static package inventory only; no APK code is executed.",
        }

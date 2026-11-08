"""Reproducible analysis case manifests and append-only notes."""
from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .analysis import inspect_file

def create_case(target: str | Path, output_dir: str | Path) -> dict[str, Any]:
    source = Path(target).expanduser().resolve()
    report = inspect_file(source)
    root = Path(output_dir).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=False)
    now = datetime.now(timezone.utc).isoformat()
    manifest = {
        "schema_version": 1,
        "case_created_utc": now,
        "case_name": root.name,
        "target": {"path_at_intake": str(source), "name": source.name,
                   "size_bytes": report["size_bytes"], "sha256": report["sha256"]},
        "environment": {"platform": platform.platform(), "python": sys.version.split()[0]},
        "scope": "static inspection",
        "notes": [],
    }
    (root / "case.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (root / "intake-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (root / "evidence.jsonl").write_text("", encoding="utf-8")
    return manifest

def add_note(case_dir: str | Path, note: str) -> dict[str, Any]:
    root = Path(case_dir).expanduser().resolve()
    manifest_path = root / "case.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"case manifest not found: {manifest_path}")
    if not note.strip():
        raise ValueError("note must not be empty")
    event = {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "event": "analyst_note", "note": note.strip()}
    with (root / "evidence.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event

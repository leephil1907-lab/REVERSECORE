"""Discover optional reverse-engineering tools available on PATH."""
from __future__ import annotations

import shutil
import subprocess
from typing import Any

TOOLS = {
    "ghidra": ["analyzeHeadless"],
    "radare2": ["r2"],
    "rizin": ["rizin"],
    "jadx": ["jadx"],
    "frida": ["frida"],
    "androguard": ["androguard"],
    "angr": ["angr"],
    "binwalk": ["binwalk"],
    "apktool": ["apktool"],
}

def discover_tools() -> list[dict[str, Any]]:
    results = []
    for name, commands in TOOLS.items():
        executable = next((shutil.which(command) for command in commands if shutil.which(command)), None)
        row: dict[str, Any] = {"name": name, "installed": executable is not None, "path": executable}
        if executable:
            try:
                run = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=3, check=False)
                text = (run.stdout or run.stderr).strip().splitlines()
                if text:
                    row["version"] = text[0][:240]
            except (OSError, subprocess.TimeoutExpired):
                row["version"] = "version unavailable"
        results.append(row)
    return results

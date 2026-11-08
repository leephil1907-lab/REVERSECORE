"""Standalone HTML and JSON report export."""
from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .analysis import inspect_file

def build_report(target: str | Path) -> dict[str, Any]:
    return {
        "report_schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": inspect_file(target),
    }

def write_report(target: str | Path, output: str | Path, output_format: str = "html") -> Path:
    result = build_report(target)
    destination = Path(output).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    if output_format == "json":
        destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    elif output_format == "html":
        analysis = result["analysis"]
        strings = "\n".join(analysis.get("strings_sample", []))
        metadata = {key: value for key, value in analysis.items() if key != "strings_sample"}
        document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>REVERSECORE report — {html.escape(analysis["name"])}</title>
<style>
:root {{ color-scheme: light dark; font-family: system-ui, sans-serif; }}
body {{ max-width: 960px; margin: 40px auto; padding: 0 20px; line-height: 1.55; }}
header {{ border-bottom: 1px solid #8886; margin-bottom: 24px; }}
h1 {{ letter-spacing: -.03em; }}
pre {{ overflow-wrap: anywhere; white-space: pre-wrap; background: #8882; padding: 16px; border-radius: 10px; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ text-align: left; vertical-align: top; padding: 9px; border-bottom: 1px solid #8885; }}
th {{ width: 220px; }}
small {{ opacity: .75; }}
</style>
</head>
<body>
<header><h1>REVERSECORE Analysis Report</h1><small>Generated {html.escape(result["generated_utc"])}</small></header>
<h2>File metadata</h2>
<table><tbody>
{''.join(f'<tr><th>{html.escape(str(key))}</th><td>{html.escape(json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else str(value))}</td></tr>' for key, value in metadata.items())}
</tbody></table>
<h2>Printable strings sample</h2>
<pre>{html.escape(strings) if strings else "No printable strings were found in the scanned sample."}</pre>
<footer><small>Static inspection output. Findings require independent validation.</small></footer>
</body></html>
"""
        destination.write_text(document, encoding="utf-8")
    else:
        raise ValueError("output_format must be 'html' or 'json'")
    return destination

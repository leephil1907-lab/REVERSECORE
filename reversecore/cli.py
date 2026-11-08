"""Command-line interface for REVERSECORE."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .analysis import inspect_file
from .archive import inventory_zip, safe_extract_zip

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="reversecore", description="Local-first static inspection for authorized analysis.")
    sub = parser.add_subparsers(dest="command", required=True)
    inspect = sub.add_parser("inspect", help="hash, identify and extract printable strings from a file")
    inspect.add_argument("target", help="path to a local file")
    inspect.add_argument("--no-strings", action="store_true", help="skip string extraction")
    inspect.add_argument("--json", action="store_true", help="emit JSON")
    archive = sub.add_parser("archive", help="list ZIP/APK/JAR archive contents")
    archive.add_argument("target")
    archive.add_argument("--json", action="store_true")
    extract = sub.add_parser("extract", help="extract a ZIP/APK/JAR to a destination")
    extract.add_argument("target")
    extract.add_argument("destination")
    return parser

def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "inspect":
            result = inspect_file(args.target, include_strings=not args.no_strings)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                for key, value in result.items():
                    print(f"{key}: {value}")
        elif args.command == "archive":
            result = inventory_zip(args.target)
            print(json.dumps(result, indent=2) if args.json else "\n".join(
                f"{'DIR ' if row['is_directory'] else 'FILE'} {row['size_bytes']:>10}  {row['name']}" for row in result
            ))
        elif args.command == "extract":
            written = safe_extract_zip(args.target, args.destination)
            print(f"Extracted {len(written)} files to {Path(args.destination).resolve()}")
        return 0
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"reversecore: error: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())

"""Command-line interface for REVERSECORE."""
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

from .analysis import inspect_file
from .archive import inventory_zip, safe_extract_zip
from .apk import inspect_apk
from .binary_formats import parse_dex, parse_elf, parse_macho, parse_pe

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
    apk = sub.add_parser("apk", help="inspect Android APK structure and DEX strings")
    apk.add_argument("target")
    apk.add_argument("--json", action="store_true")
    parse = sub.add_parser("parse", help="parse PE, ELF, Mach-O or DEX metadata")
    parse.add_argument("target")
    parse.add_argument("--format", choices=["auto", "pe", "elf", "macho", "dex"], default="auto")
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
        elif args.command == "apk":
            result = inspect_apk(args.target)
            print(json.dumps(result, indent=2) if args.json else json.dumps(result, indent=2))
        elif args.command == "parse":
            fmt = args.format
            if fmt == "auto":
                with open(args.target, "rb") as handle:
                    magic = handle.read(4)
                fmt = "pe" if magic[:2] == b"MZ" else "elf" if magic == b"\\x7fELF" else "dex" if magic.startswith(b"dex\\n") else "macho"
            parser = {"pe": parse_pe, "elf": parse_elf, "macho": parse_macho, "dex": parse_dex}[fmt]
            print(json.dumps({"target": str(Path(args.target).resolve()), "analysis": parser(args.target)}, indent=2))
        elif args.command == "extract":
            written = safe_extract_zip(args.target, args.destination)
            print(f"Extracted {len(written)} files to {Path(args.destination).resolve()}")
        return 0
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"reversecore: error: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())

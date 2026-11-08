# REVERSECORE Static Analysis Engine

The first engine release is a dependency-free Python CLI intended for local use.

## Commands

```bash
python -m reversecore.cli inspect ./sample.bin --json
python -m reversecore.cli inspect ./sample.bin --no-strings
python -m reversecore.cli apk ./application.apk --json
python -m reversecore.cli parse ./native-library.so
python -m reversecore.cli tools
python -m reversecore.cli case-init ./sample.bin ./cases/sample-001
python -m reversecore.cli case-note ./cases/sample-001 'Reviewed headers; no execution performed.'
python -m reversecore.cli archive ./application.apk
python -m reversecore.cli extract ./application.apk ./work/extracted
```

After installation with `python -m pip install -e .`, use the `reversecore` command.

## Current capabilities

- SHA-256 hashing and basic file identification.
- Sampled byte entropy (a triage indicator, not proof of encryption or packing).
- ASCII and UTF-16LE printable-string extraction.
- Bounds-checked metadata parsing for PE/PE32+, ELF32/ELF64, Mach-O thin/fat, and standard DEX headers/string tables.
- Optional toolchain discovery for Ghidra, radare2, Rizin, JADX, Frida, Androguard, angr, Binwalk, and apktool.
- Reproducible case intake with environment metadata, SHA-256 manifest, intake report, and append-only JSONL analyst notes.
- ZIP extraction is limited to 512 MiB of expanded data by default.
- ZIP/APK/JAR inventory and path-traversal-resistant extraction.
- APK manifest presence/format, DEX file hashes and string samples, native-library inventory, and asset counts.

## Boundaries

This version does not execute target files, bypass protections, modify binaries, or claim full format parsing. PE, Mach-O, DEX, firmware and native disassembly integrations are planned adapters. Treat every sample as untrusted and work on copies in an isolated environment.

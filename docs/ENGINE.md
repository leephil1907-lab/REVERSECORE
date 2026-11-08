# REVERSECORE Static Analysis Engine

The first engine release is a dependency-free Python CLI intended for local use.

## Commands

```bash
python -m reversecore.cli inspect ./sample.bin --json
python -m reversecore.cli inspect ./sample.bin --no-strings
python -m reversecore.cli apk ./application.apk --json
python -m reversecore.cli archive ./application.apk
python -m reversecore.cli extract ./application.apk ./work/extracted
```

After installation with `python -m pip install -e .`, use the `reversecore` command.

## Current capabilities

- SHA-256 hashing and basic file identification.
- Sampled byte entropy (a triage indicator, not proof of encryption or packing).
- ASCII and UTF-16LE printable-string extraction.
- Basic ELF class, byte order and machine-ID metadata.
- ZIP/APK/JAR inventory and path-traversal-resistant extraction.
- APK manifest presence/format, DEX file hashes and string samples, native-library inventory, and asset counts.

## Boundaries

This version does not execute target files, bypass protections, modify binaries, or claim full format parsing. PE, Mach-O, DEX, firmware and native disassembly integrations are planned adapters. Treat every sample as untrusted and work on copies in an isolated environment.

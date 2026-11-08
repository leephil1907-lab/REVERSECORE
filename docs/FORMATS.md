# Supported format coverage

| Format | Current built-in coverage | Not yet implemented |
|---|---|---|
| PE / PE32+ | DOS pointer, signature, COFF fields, optional-header entry point and image base, section table | Imports/exports, relocations, resources, certificates, disassembly |
| ELF32 / ELF64 | Class, byte order, type, machine, entry point, program-header and section-table metadata | Symbol resolution, relocations, dynamic dependencies, full segment validation |
| Mach-O thin | CPU, subtype, file type, load-command count and size | Load-command decoding, symbols, code signatures |
| Mach-O fat | Architecture table and slice bounds | Per-slice recursive parsing |
| DEX | Header metadata and best-effort string table sample | Full instruction parsing, annotations, verifier, call graph |
| APK | Manifest presence/format, DEX hashes/string samples, native library names, asset count | Binary XML decoding, signing verification, resource table decoding |
| ZIP/JAR | Member listing, sizes, safe extraction | Full format-specific semantic analysis |

All parsers are triage helpers. They do not replace mature tools such as Ghidra, JADX, Androguard, radare2, Rizin or Binwalk.

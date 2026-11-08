# Architecture

## Design goals
- Local-first, zero mandatory runtime dependencies.
- Deterministic, machine-readable outputs.
- Format parsers must validate bounds before reading offsets.
- External tools are optional adapters, not hidden dependencies.
- Analysis of an input file never implies executing it.

## Layers
1. **Intake** — path validation, file size, SHA-256, format identification.
2. **Format parsers** — PE, ELF, Mach-O and DEX metadata parsers.
3. **Package inspection** — APK and ZIP inventory, DEX string triage, native-library listing.
4. **Case evidence** — JSON manifest, intake report and append-only JSONL notes.
5. **Tool discovery** — detects optional specialist executables on PATH.
6. **Future adapters/UI** — explicit orchestration and a browser interface are not implemented in this release.

## Data flow
```text
local file
   |
   v
intake + SHA-256
   |
   +--> identify / strings / entropy
   +--> PE | ELF | Mach-O | DEX parser
   +--> ZIP/APK inventory
   |
   v
JSON output or case folder
   |
   +--> case.json
   +--> intake-report.json
   +--> evidence.jsonl
```

## Compatibility
Python 3.10+ is the declared baseline. The core uses only the Python standard library. Optional specialist tools have their own platform, runtime and licensing requirements.

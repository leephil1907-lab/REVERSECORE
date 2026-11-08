# REVERSECORE

**Reverse engineering research and tooling workspace.**

REVERSECORE is a curated workspace for understanding software behavior, analyzing binaries and application packages, inspecting runtime behavior, and documenting reproducible findings. It brings together the official REA agent toolkit and selected open-source reverse-engineering projects without copying their code into this repository.

## Included upstream projects

| Project | Purpose | Upstream |
|---|---|---|
| REA | Agent-driven reverse engineering over MCP/CLI | https://github.com/morluto/rea |
| Awesome Reverse Engineering | Curated tool and learning index | https://github.com/edwardtay/awesome-reverse-engineering |
| Ghidra | Native binary disassembly and decompilation | https://github.com/NationalSecurityAgency/ghidra |
| radare2 | Scriptable binary analysis framework | https://github.com/radareorg/radare2 |
| Rizin | Reverse-engineering framework and libraries | https://github.com/rizinorg/rizin |
| JADX | Android DEX/APK decompiler | https://github.com/skylot/jadx |
| Apktool | Android APK resources and manifest tooling | https://github.com/iBotPeaches/Apktool |
| Frida | Dynamic instrumentation toolkit | https://github.com/frida/frida |
| Androguard | Android application analysis toolkit | https://github.com/androguard/androguard |
| angr | Binary analysis framework | https://github.com/angr/angr |
| Binwalk | Firmware analysis and extraction | https://github.com/ReFirmLabs/binwalk |

Upstream projects are fetched as shallow Git clones by the bootstrap script. Their original licenses, histories, maintainers, and contribution rules remain with their respective projects.

## Quick start

Requirements: Git, Bash, and (for REA) Node.js 22.19+ / 24.11+ / 26+ with npm.

```bash
git clone https://github.com/leephil1907-lab/REVERSECORE.git
cd REVERSECORE
bash scripts/import-upstreams.sh
```

Then set up REA with your coding agent:

```bash
cd third_party/rea
npx rea-agents@latest setup
```

Review the setup plan before approving it, then restart your coding agent. REA setup modifies your local agent configuration; it does not run automatically as part of the import script.

## REVERSECORE engine

The local analysis engine provides SHA-256 hashing, file identification, sampled entropy, printable-string extraction, metadata parsers for PE/ELF/Mach-O/DEX, Android APK inventory, safe archive extraction, reproducible case manifests, evidence notes, and optional toolchain discovery.

Install and run it:

```bash
python -m pip install -e .
reversecore inspect ./sample.bin --json
reversecore apk ./application.apk --json
reversecore parse ./native-library.so
reversecore tools
reversecore case-init ./sample.bin ./cases/sample-001
reversecore case-note ./cases/sample-001 'Reviewed headers; no execution performed.'
reversecore archive ./application.apk
reversecore extract ./application.apk ./work/extracted
```

Or run directly without installing:

```bash
python -m reversecore.cli inspect ./sample.bin --json
```

See [docs/ENGINE.md](docs/ENGINE.md) for details and current limitations, and [docs/INTEGRATIONS.md](docs/INTEGRATIONS.md) for optional specialist tools.

## Repository layout

```text
REVERSECORE/
├── reversecore/              # Python analysis engine and CLI
├── tests/                    # parser, archive and case tests
├── scripts/                  # upstream and Termux setup helpers
├── docs/                     # architecture, formats, security and usage
├── .github/workflows/        # automated test workflow
├── pyproject.toml
├── LICENSE
├── CONTRIBUTING.md
└── third_party/               # local upstream clones; intentionally ignored by Git
```

## Platform notes

- The core supports Python 3.10+ and uses only the standard library.
- Termux instructions are in [docs/ANDROID-TERMUX.md](docs/ANDROID-TERMUX.md).
- Optional integrations are documented in [docs/INTEGRATIONS.md](docs/INTEGRATIONS.md).
- Format coverage and known gaps are listed in [docs/FORMATS.md](docs/FORMATS.md).
- Security assumptions and limitations are in [docs/SECURITY.md](docs/SECURITY.md).
- The imported upstream source trees are not stored in Git; run the import script locally to fetch them.

## Working principles

1. Analyze only software, devices, accounts, and data you own or are authorized to examine.
2. Prefer static inspection before executing an unknown artifact.
3. Use isolated test environments for runtime analysis.
4. Preserve hashes, tool versions, commands, and evidence for reproducibility.
5. Treat decompiler output and AI-generated explanations as hypotheses until verified against evidence.
6. Respect each upstream project's license and security policy.

## Status

The repository now includes the workspace scaffold, a dependency-free Python static inspection CLI, tests, and the repeatable upstream import process. Run the bootstrap script on a machine with Git and network access to download upstream source trees into local `third_party/` directories.

# REVERSECORE Roadmap

## Phase 1 — Core workspace
- [x] Repository scaffold and upstream catalogue
- [x] Repeatable upstream import script
- [x] Static file identification and SHA-256
- [x] Printable strings and sampled entropy
- [x] Basic ELF metadata
- [x] Bounds-checked PE, ELF, Mach-O and DEX metadata parsers
- [x] Reproducible case manifests and evidence notes
- [x] Optional external tool detection
- [x] ZIP/APK/JAR inventory and safe extraction
- [x] Unit tests and CI workflow
- [x] Termux setup helper

## Phase 2 — Format adapters
- [ ] PE header and section parser
- [ ] Mach-O load-command parser
- [ ] DEX/APK manifest and component report
- [ ] ELF section, symbol and dependency report
- [ ] Firmware filesystem inventory

## Phase 3 — Analysis orchestration
- [ ] Tool capability detection and version capture
- [ ] Structured job manifests and evidence logs
- [ ] Optional adapters for Ghidra, radare2, Rizin, JADX, Frida and Binwalk
- [ ] Reproducible HTML/JSON/PDF reports

## Phase 4 — Product interface
- [ ] Local API and job queue
- [ ] Web interface for projects and analysis runs
- [ ] User-separated workspaces and artifact access controls
- [ ] Exportable investigation bundles

The roadmap is a plan, not a claim that unfinished features are implemented.

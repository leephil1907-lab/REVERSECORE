# Third-party projects

REVERSECORE references upstream projects as Git submodules pinned to exact commits. Initialize them with `git submodule update --init --depth 1 --recursive` or run `bash scripts/import-upstreams.sh`. The source histories and licenses remain with upstream maintainers.

| Local directory | Upstream repository | Role |
|---|---|---|
| `third_party/rea` | [morluto/rea](https://github.com/morluto/rea) | Official REA agent toolkit |
| `third_party/awesome-reverse-engineering` | [edwardtay/awesome-reverse-engineering](https://github.com/edwardtay/awesome-reverse-engineering) | Curated discovery index |
| `third_party/ghidra` | [NationalSecurityAgency/ghidra](https://github.com/NationalSecurityAgency/ghidra) | Native analysis and decompiler |
| `third_party/radare2` | [radareorg/radare2](https://github.com/radareorg/radare2) | Binary analysis framework |
| `third_party/rizin` | [rizinorg/rizin](https://github.com/rizinorg/rizin) | Binary analysis framework |
| `third_party/jadx` | [skylot/jadx](https://github.com/skylot/jadx) | Android DEX/APK decompiler |
| `third_party/apktool` | [iBotPeaches/Apktool](https://github.com/iBotPeaches/Apktool) | Android APK resource and manifest tooling |
| `third_party/frida` | [frida/frida](https://github.com/frida/frida) | Dynamic instrumentation |
| `third_party/androguard` | [androguard/androguard](https://github.com/androguard/androguard) | Android analysis |
| `third_party/angr` | [angr/angr](https://github.com/angr/angr) | Program analysis |
| `third_party/binwalk` | [ReFirmLabs/binwalk](https://github.com/ReFirmLabs/binwalk) | Firmware analysis |

## Licensing

Exact pinned revisions are listed in [UPSTREAM_LOCK.md](UPSTREAM_LOCK.md). Ghidra is deliberately excluded from the default submodule set because its checkout is large; use `WITH_GHIDRA=1 bash scripts/import-upstreams.sh` to fetch it locally.\n\nEach upstream repository has its own license and notices. Check the current upstream `LICENSE`, `NOTICE`, and contribution/security documents before redistributing binaries, source, or modified versions. This index is not a grant of rights.

# Optional tool integrations

REVERSECORE's Python core works without external tools. This page explains how to add specialist tools; installations are optional and are not silently triggered by REVERSECORE.

## Detect installed tools

```bash
reversecore tools
```

The command checks PATH for Ghidra's `analyzeHeadless`, radare2 (`r2`), Rizin, JADX, Frida, Androguard, angr, Binwalk, and apktool. Detection does not execute a target file.

## Suggested installation paths

### Android / Termux
- Core: `pkg install python git`
- JADX: use the official JADX release/package instructions; a Java runtime is required.
- Frida: install the Python package only where a compatible Frida server/device setup is available.
- Androguard: `python -m pip install androguard`
- Binwalk: use the current upstream installation instructions; dependencies vary by release.
- Ghidra, radare2 and Rizin may require a Linux desktop environment, native build dependencies, or substantial storage. They are not assumed to work on every Android device.

### Debian / Ubuntu Linux
Use each upstream project's current official release and installation documentation. Package names and versions differ by distribution. Typical packages are available for Java, Binutils, and some of the listed tools, but distro packages may lag upstream.

## Integration design

The engine reports whether tools are present. It does not yet automatically pass samples to them. A future adapter should:
1. require an explicit tool path and analysis action;
2. record tool version, arguments, exit status and output hashes;
3. run with timeouts and resource limits;
4. store output in a per-case artifact directory;
5. never treat tool output as verified fact without corroboration.

## Official upstreams

- [Ghidra](https://github.com/NationalSecurityAgency/ghidra)
- [radare2](https://github.com/radareorg/radare2)
- [Rizin](https://github.com/rizinorg/rizin)
- [JADX](https://github.com/skylot/jadx)
- [Frida](https://github.com/frida/frida)
- [Androguard](https://github.com/androguard/androguard)
- [angr](https://github.com/angr/angr)
- [Binwalk](https://github.com/ReFirmLabs/binwalk)

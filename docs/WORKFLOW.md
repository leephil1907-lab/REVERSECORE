# REVERSECORE workflow

## 1. Identify the target

Record the target type (web application, desktop application, Android package, native executable, firmware image, or protocol capture), provenance, version, and authorization to test it.

## 2. Preserve the original

Keep an untouched copy of the input. Record a SHA-256 digest before analysis.

Linux / Termux:
```bash
sha256sum /path/to/target
```

If `sha256sum` is unavailable, use an equivalent trusted hashing utility.

## 3. Choose an analysis path

- **Application behavior / agent-led investigation:** REA (MCP/CLI).
- **Native executable:** Ghidra, radare2, or Rizin.
- **Android APK/DEX:** JADX and Androguard; use Frida only for authorized runtime instrumentation.
- **Firmware image:** Binwalk, followed by manual validation of extracted content.
- **General discovery:** the Awesome Reverse Engineering index.

## 4. Separate static and dynamic work

Start with file identification, metadata, strings, manifests, and static structure. Run a target only in an isolated environment when runtime behavior is necessary. Do not expose personal credentials or production data to analysis tools.

## 5. Keep an evidence log

For each investigation, record:

- Target name, version, source, and SHA-256
- Host OS and environment
- Tool names and versions
- Exact commands and configuration
- Observations, screenshots, logs, and extracted artifacts
- Confidence level and unresolved questions

## 6. Verify conclusions

Decompiler output can be incomplete or misleading. Confirm important findings with cross-references, runtime observations, tests, or a second independent tool.

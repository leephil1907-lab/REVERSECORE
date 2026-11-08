# Security model

## Trust boundaries
- Input samples are untrusted data.
- Archive members, filenames, metadata and extracted strings may be malicious.
- Third-party tools are separate executables with their own attack surface.
- Reports can contain secrets, tokens, internal URLs or personal data extracted from a sample.

## Current protections
- Parsers use explicit bounds checks before reading structured fields.
- ZIP extraction rejects absolute and parent-traversal paths.
- ZIP extraction refuses archives whose declared expanded size exceeds 512 MiB by default.
- The core does not execute target binaries or install third-party tools automatically.
- Optional tool discovery only checks PATH and requests a version string with a short timeout.

## Operator practices
- Work on a copy and preserve the original SHA-256.
- Use a disposable VM/container for unknown or hostile samples.
- Keep network access disabled unless the test requires it.
- Do not place secrets in case notes or publish case folders without reviewing them.
- Keep extracted files outside application and system directories.
- Treat parser output and decompiler output as leads, not proof.

## Known limitations
- The 512 MiB ZIP limit is based on archive metadata; it is not a full decompression-bomb defense for every unusual archive format.
- APK binary XML is detected but not decoded by the built-in engine.
- DEX string decoding is best-effort modified UTF-8 handling, not a complete DEX verifier.
- PE/ELF/Mach-O parsers currently return selected metadata, not full disassembly or complete loader validation.
- External tools are detected, not automatically orchestrated.
- This project is not an antivirus or malware verdict engine.

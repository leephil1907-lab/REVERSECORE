# Case output reference

A successful command:

```bash
reversecore case-init ./sample.bin ./cases/sample-001
```

creates:

```text
cases/sample-001/
├── case.json
├── intake-report.json
└── evidence.jsonl
```

## case.json
Contains schema version, UTC creation time, case name, source path at intake, file name, byte size, SHA-256, host platform, Python version and the declared analysis scope.

## intake-report.json
Contains the initial file inspection report, including file identification, SHA-256, sampled entropy, printable strings and whether the string scan was truncated.

## evidence.jsonl
One JSON object per line. The `case-note` command appends timestamped analyst notes. The file is append-only by convention; do not rewrite earlier observations when correcting a finding. Add a new note that references the correction.

## Sharing
Review all three files before sharing. Paths, extracted strings, filenames and notes can disclose private information.

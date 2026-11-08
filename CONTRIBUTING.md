# Contributing

1. Create a focused branch for each change.
2. Keep the core standard-library-only unless a dependency is justified and documented.
3. Add unit tests for valid inputs, truncated inputs and malformed offsets.
4. Keep parsers read-only; do not execute sample files in tests.
5. Include exact upstream attribution and license details when adding third-party code.
6. Run `python -m unittest discover -s tests -v` before opening a pull request.
7. Update README and relevant docs whenever commands or output schemas change.

## Reporting bugs
Include Python version, operating system, REVERSECORE version, command, redacted traceback and a sample hash. Do not attach confidential or sensitive samples to public issues.

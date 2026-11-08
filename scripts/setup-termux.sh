#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

pkg update -y
pkg install -y git python

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ ! -f "$ROOT/pyproject.toml" ]]; then
  ROOT="$HOME/REVERSECORE"
  if [[ ! -d "$ROOT/.git" ]]; then
    git clone https://github.com/leephil1907-lab/REVERSECORE.git "$ROOT"
  fi
fi

cd "$ROOT"
python -m pip install -e .
python -m compileall -q reversecore
python -m unittest discover -s tests -v

printf '\nREVERSECORE is installed. Try:\n'
printf '  reversecore inspect /path/to/your/sample --json\n'
printf '  reversecore apk /path/to/your/app.apk --json\n'
printf '  reversecore tools\n'

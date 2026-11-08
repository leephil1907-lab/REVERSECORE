#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/third_party"
cd "$ROOT"

if ! command -v git >/dev/null 2>&1; then
  echo "Git is required. Install Git and run this script again." >&2
  exit 1
fi

mkdir -p "$DEST"
echo "Synchronizing pinned upstream submodules..."
git submodule sync --recursive
git submodule update --init --depth 1 --recursive

# Ghidra is intentionally not a default submodule because its source checkout is large.
if [[ "${WITH_GHIDRA:-0}" == "1" ]]; then
  if [[ -d "$DEST/ghidra/.git" ]]; then
    echo "Updating Ghidra..."
    git -C "$DEST/ghidra" pull --ff-only
  elif [[ -e "$DEST/ghidra" ]]; then
    echo "Ghidra path exists but is not a Git checkout: $DEST/ghidra" >&2
    exit 1
  else
    echo "Cloning optional Ghidra source..."
    git clone --depth 1 --filter=blob:none https://github.com/NationalSecurityAgency/ghidra.git "$DEST/ghidra"
  fi
else
  echo "Skipping optional Ghidra source. Set WITH_GHIDRA=1 to fetch it."
fi

echo
echo "Upstream import complete."
echo "Pinned submodule revisions are recorded in UPSTREAM_LOCK.md."
echo "Review each project's own installation instructions before building it."

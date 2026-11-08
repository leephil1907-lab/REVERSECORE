#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/third_party"
mkdir -p "$DEST"

if ! command -v git >/dev/null 2>&1; then
  echo "Git is required. Install Git and run this script again." >&2
  exit 1
fi

# Shallow clones keep the initial workspace download manageable.
# Existing directories are preserved and updated only when they are Git repos.
import_repo() {
  local name="$1"
  local url="$2"
  local target="$DEST/$name"

  if [[ -d "$target/.git" ]]; then
    echo "Updating $name..."
    git -C "$target" pull --ff-only
  elif [[ -e "$target" ]]; then
    echo "Skipping $name: $target exists but is not a Git checkout." >&2
  else
    echo "Cloning $name..."
    git clone --depth 1 --filter=blob:none "$url" "$target"
  fi
}

import_repo "rea" "https://github.com/morluto/rea.git"
import_repo "awesome-reverse-engineering" "https://github.com/edwardtay/awesome-reverse-engineering.git"
import_repo "radare2" "https://github.com/radareorg/radare2.git"
import_repo "rizin" "https://github.com/rizinorg/rizin.git"
import_repo "jadx" "https://github.com/skylot/jadx.git"
import_repo "apktool" "https://github.com/iBotPeaches/Apktool.git"
import_repo "frida" "https://github.com/frida/frida.git"
import_repo "androguard" "https://github.com/androguard/androguard.git"
import_repo "angr" "https://github.com/angr/angr.git"
import_repo "binwalk" "https://github.com/ReFirmLabs/binwalk.git"

# Ghidra is a larger source checkout; opt in explicitly.
if [[ "${WITH_GHIDRA:-0}" == "1" ]]; then
  import_repo "ghidra" "https://github.com/NationalSecurityAgency/ghidra.git"
else
  echo "Skipping Ghidra source (large checkout). Set WITH_GHIDRA=1 to include it."
fi

echo
echo "Import complete. Upstream source trees are in: $DEST"
echo "Review each project's own installation instructions before building it."

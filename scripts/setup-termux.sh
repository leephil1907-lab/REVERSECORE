#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

pkg update -y
pkg install -y git python
python -m pip install --upgrade pip
git clone https://github.com/leephil1907-lab/REVERSECORE.git
cd REVERSECORE
python -m pip install -e .
python -m unittest discover -s tests -v

printf '\nREVERSECORE is installed. Try:\n'
printf '  reversecore inspect /path/to/your/sample --json\n'
printf '  reversecore archive /path/to/your/app.apk\n'

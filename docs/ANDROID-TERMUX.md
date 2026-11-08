# Android and Termux setup

## Install the core
```bash
pkg update -y
pkg install -y git python
git clone https://github.com/leephil1907-lab/REVERSECORE.git
cd REVERSECORE
python -m pip install -e .
python -m unittest discover -s tests -v
```

Or run the included helper:
```bash
bash scripts/setup-termux.sh
```

## Inspect a downloaded APK
```bash
termux-setup-storage
reversecore inspect ~/storage/downloads/example.apk --json
reversecore apk ~/storage/downloads/example.apk --json
reversecore archive ~/storage/downloads/example.apk --json
```

## Parse a native library
```bash
reversecore parse ~/storage/downloads/libexample.so
```

## Create a case folder
```bash
mkdir -p ~/reversecore-cases
reversecore case-init ~/storage/downloads/example.apk ~/reversecore-cases/example-001
reversecore case-note ~/reversecore-cases/example-001 "Initial static intake completed."
```

## Storage note
APK and firmware files can be large. Keep the repository and case folders in Termux's private home directory for predictable permissions; use shared storage only for importing samples and exporting reviewed reports.

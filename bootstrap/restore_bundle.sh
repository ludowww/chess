#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ARCHIVE_DIR="$REPO_ROOT/bootstrap/archive"
OUTPUT="$REPO_ROOT/brisez_les_systemes_v1_0_rc1.tar.xz"
EXPECTED_SHA256="819bab279e77a4835a579110cebaa79d8827d0cc7747dd7cd66a9a7e287f805e"

python3 - "$ARCHIVE_DIR" "$OUTPUT" "$EXPECTED_SHA256" <<'PY'
from __future__ import annotations

import base64
import hashlib
import pathlib
import sys

archive_dir = pathlib.Path(sys.argv[1])
output = pathlib.Path(sys.argv[2])
expected = sys.argv[3].lower()
pattern = "brisez_les_systemes_v1_0_rc1.tar.xz.b64.part*"
parts = sorted(archive_dir.glob(pattern))
expected_names = [f"brisez_les_systemes_v1_0_rc1.tar.xz.b64.part{i:02d}" for i in range(20)]
actual_names = [part.name for part in parts]

if actual_names != expected_names:
    raise SystemExit(
        "Archive segments are missing, duplicated, or misnamed.\n"
        f"Expected: {expected_names}\nActual:   {actual_names}"
    )

payload = "".join(part.read_text(encoding="ascii") for part in parts)
payload = "".join(payload.split())
try:
    raw = base64.b64decode(payload, validate=True)
except Exception as exc:
    raise SystemExit(f"Invalid base64 archive data: {exc}") from exc

actual = hashlib.sha256(raw).hexdigest()
if actual != expected:
    raise SystemExit(f"SHA-256 mismatch: expected {expected}, got {actual}")

output.write_bytes(raw)
print(f"Archive reconstructed: {output}")
print(f"SHA-256 verified:      {actual}")
PY

tar -xJf "$OUTPUT" -C "$REPO_ROOT"

if [[ ! -f "$REPO_ROOT/brisez_les_systemes_v1/LAB/README_LAB.md" ]]; then
    echo "Extraction completed but the expected project files were not found." >&2
    exit 1
fi

echo "Project restored: $REPO_ROOT/brisez_les_systemes_v1"
echo "Next: cd brisez_les_systemes_v1 && ./LAB/run_static_qa.sh"

#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
python "$HERE/scripts/validate_course.py" \
  --pgn "$ROOT/PGN/99_cours_v1_core_40.pgn" \
  --manifest "$ROOT/DATA/core_40_index.csv" \
  --output "$ROOT/DATA/static_qa_report.json"
python -m unittest discover -s "$HERE/tests" -v
python -m compileall -q "$HERE/scripts" "$HERE/tests"
echo "Static QA: OK"

#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
. .venv/bin/activate
split="$1"; month="$2"; max_games="$3"; output="$4"
fifo="/tmp/lichess_${month}_${split}_${max_games}.pgn.zst"
rm -f "$fifo"
mkfifo "$fifo"
echo "[$(date -Iseconds)] START $split month=$month max_games=$max_games output=$output"
(curl -L --fail --silent --show-error "https://database.lichess.org/standard/lichess_db_standard_rated_${month}.pgn.zst" > "$fifo") &
writer=$!
set +e
python LAB/scripts/lichess_extract_fast.py "$fifo" \
  --manifest DATA/core_40_index.csv \
  --bands 1100-1299 1300-1499 1500-1699 1700-1899 1900-2099 \
  --speeds blitz rapid \
  --split "$split" \
  --max-games "$max_games" \
  --max-plies 80 \
  --output "$output"
rc=$?
kill "$writer" 2>/dev/null || true
wait "$writer" 2>/dev/null || true
rm -f "$fifo"
set -e
if [ "$rc" -ne 0 ]; then
  echo "[$(date -Iseconds)] FAIL $split rc=$rc" >&2
  exit "$rc"
fi
rows=$(python - <<PY
import pandas as pd
print(len(pd.read_csv('$output')))
PY
)
echo "[$(date -Iseconds)] DONE $split rows=$rows"

#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
. .venv/bin/activate
mkdir -p DATA
run_extract() {
  local split="$1" month="$2" max_games="$3" output="$4"
  local fifo="/tmp/lichess_${month}_${split}_${max_games}.pgn.zst"
  rm -f "$fifo"
  mkfifo "$fifo"
  echo "[$(date -Iseconds)] START $split month=$month max_games=$max_games output=$output"
  (curl -L --fail --silent --show-error "https://database.lichess.org/standard/lichess_db_standard_rated_${month}.pgn.zst" > "$fifo") &
  local writer=$!
  set +e
  python LAB/scripts/lichess_extract_fast.py "$fifo" \
    --manifest DATA/core_40_index.csv \
    --bands 1100-1299 1300-1499 1500-1699 1700-1899 1900-2099 \
    --speeds blitz rapid \
    --split "$split" \
    --max-games "$max_games" \
    --max-plies 80 \
    --output "$output"
  local rc=$?
  kill "$writer" 2>/dev/null || true
  wait "$writer" 2>/dev/null || true
  rm -f "$fifo"
  set -e
  if [ "$rc" -ne 0 ]; then
    echo "[$(date -Iseconds)] FAIL $split rc=$rc" >&2
    exit "$rc"
  fi
  echo "[$(date -Iseconds)] DONE $split rows=$(python - <<PY
import pandas as pd
p='$output'
df=pd.read_csv(p)
print(len(df))
PY
)"
}
run_extract discovery 2026-03 1500000 DATA/lichess_discovery_expanded.csv
run_extract validation 2026-04 1000000 DATA/lichess_validation_expanded.csv
run_extract test 2026-05 1000000 DATA/lichess_test_expanded.csv

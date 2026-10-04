#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../oracle"
out=$(uv run pytest -q 2>&1) || { echo "$out" | tail -40; exit 1; }
echo "$out" | tail -3
n=$(echo "$out" | grep -oE "[0-9]+ passed" | grep -oE "[0-9]+")
[ "${n:-0}" -ge 15 ] || { echo "need >=15 passing tests, have ${n:-0}"; exit 1; }
nm=$(ls mutants/*.py 2>/dev/null | grep -v run_mutants | wc -l)
[ "$nm" -ge 5 ] || { echo "need >=5 mutants, have $nm"; exit 1; }
uv run python mutants/run_mutants.py
echo A3 OK

#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 scripts/status.py > logs/status.txt
grep -q "Lattice" logs/status.txt && grep -qi "theorems" logs/status.txt
grep -q "<!-- STATUS:BEGIN -->" phase01.md && grep -q "<!-- STATUS:END -->" phase01.md
echo A7 OK

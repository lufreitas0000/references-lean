#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
for k in 1 2 3 4 5 6 7 8 9 10; do f=$(ls docs/spec/P1/S1.$k-*.md 2>/dev/null | head -1)
  [ -n "$f" ] || { echo "missing docs/spec/P1/S1.$k-*.md"; exit 1; }
  grep -q '```spec' "$f" || { echo "$f has no spec block"; exit 1; }
  grep -qi "Lean names" "$f" || { echo "$f has no 'Lean names' section"; exit 1; }
  grep -qi "Hazards" "$f" || { echo "$f has no 'Hazards' section"; exit 1; }
done
python3 scripts/notation_lint.py docs/spec/P1/*.md
echo A5 OK

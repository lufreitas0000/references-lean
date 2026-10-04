#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
nb=$(ls tests/canary/bad/*.lean 2>/dev/null | wc -l); ng=$(ls tests/canary/good/*.lean 2>/dev/null | wc -l)
[ "$nb" -ge 12 ] || { echo "need >=12 bad canaries, have $nb"; exit 1; }
[ "$ng" -ge 2 ] || { echo "need >=2 good canaries, have $ng"; exit 1; }
for t in sorry admit "^axiom\|^ *axiom " native_decide opaque unsafe implemented_by extern maxHeartbeats Tendsto tsum MeasureTheory; do
  grep -lq -- "$t" tests/canary/bad/*.lean || { echo "no bad canary exercising: $t"; exit 1; }
done
ls tests/canary/bad/ | grep -qi lock || { echo "need a statement-lock canary (filename containing 'lock')"; exit 1; }
ls tests/canary/bad/ | grep -qi axiom_hidden || { echo "need axiom_hidden canary"; exit 1; }
bash scripts/anti_cheat.sh Bosonize/Core
bash scripts/selftest_guards.sh
python3 scripts/lock_statements.py --selftest
bash scripts/axiom_audit.sh
echo A1 OK

#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
export PATH=$HOME/.elan/bin:$PATH
lake env lean Bosonize/Audit/MathlibAudit.lean > logs/mathlib_audit.log 2>&1 || { tail -30 logs/mathlib_audit.log; exit 1; }
grep -q "sorry\|axiom " Bosonize/Audit/MathlibAudit.lean && { echo "no sorry/axiom allowed"; exit 1; }
miss=0
while read -r n; do [ -z "$n" ] && continue
  grep -qF -- "$n" Bosonize/Audit/MathlibAudit.lean || { echo "name not audited in .lean: $n"; miss=1; }
  grep -qF -- "$n" docs/MATHLIB_AUDIT.md || { echo "name missing in MATHLIB_AUDIT.md: $n"; miss=1; }
done < scripts/accept/A2_names.txt
[ $miss -eq 0 ]
grep -q "Verified" docs/MATHLIB_AUDIT.md && { echo "use FOUND / MISSING / RENAMED(new name), not 'Verified'"; exit 1; }
echo A2 OK

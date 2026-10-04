#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 - << 'PY'
import csv, sys
rows = list(csv.DictReader(open("docs/MIRANDA_REGISTRY.csv")))
need = {"miranda_id","section","equation_label","transcript_file","latex","status","phase","notes"}
assert need <= set(rows[0].keys()), f"columns must include {need}"
ok = {"UNSEEN","SUSPECT","ORACLE-OK","DERIVED-LEAN","CONTRADICTED","MISSING-SOURCE","OUT-OF-SCOPE"}
bad = [r["miranda_id"] for r in rows if r["status"] not in ok]
assert not bad, f"bad status in {bad[:5]}"
assert len(rows) >= 40, f"only {len(rows)} rows"
assert sum(r["phase"] == "P1" for r in rows) >= 10, "need >=10 rows tagged phase P1"
ids = [r["miranda_id"] for r in rows]; assert len(ids) == len(set(ids)), "duplicate ids"
PY
n=$(grep -cE "^#+ *W-[0-9]+" docs/WATCHLIST.md); [ "$n" -ge 10 ] || { echo "WATCHLIST needs >=10 W-xx entries"; exit 1; }
echo A6 OK

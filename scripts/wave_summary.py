#!/usr/bin/env python3
"""Compact summary of a wave: one line per task + total estimated cost."""
import json, sys, tomllib
from pathlib import Path
root = Path(__file__).resolve().parent.parent
tot = 0.0
for card in sorted(Path(sys.argv[1]).glob("*.toml")):
    tid = tomllib.loads(card.read_text())["id"]
    f = root / "logs/tasks" / f"{tid}.json"
    if not f.exists():
        print(f"{tid:6} NO-RESULT"); continue
    r = json.loads(f.read_text()); tot += r["est_cost_brl"]
    print(f"{tid:6} {r['status']:8} turns={r['turns']:3} esc={int(r['escalated'])} R${r['est_cost_brl']:.2f}  {r['summary'][:160]!r}")
print(f"TOTAL est. R${tot:.2f}")

#!/usr/bin/env python3
"""Read a line range of a Miranda transcript (read-only access outside the repo for workers)."""
import sys
from pathlib import Path
base = Path(__file__).resolve().parent.parent.parent / "references-transcripts" / "miranda_2003"
f = (base / Path(sys.argv[1]).name)
lines = f.read_text().splitlines()
s, e = int(sys.argv[2]), int(sys.argv[3])
print(f"[{f.name}: {len(lines)} lines total]")
for i in range(max(s, 1) - 1, min(e, len(lines))):
    print(f"{i+1}: {lines[i]}")

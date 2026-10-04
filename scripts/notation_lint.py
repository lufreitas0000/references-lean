#!/usr/bin/env python3
import sys, re
fail = False
for f in sys.argv[1:]:
    with open(f) as file:
        in_spec = False
        for i, line in enumerate(file, 1):
            if line.strip().startswith('```spec'): in_spec = True
            elif line.strip() == '```' and in_spec: in_spec = False
            elif in_spec:
                if '^' in line:
                    print(f"{f}:{i} CHEAT: ^ found in spec")
                    fail = True
sys.exit(1 if fail else 0)

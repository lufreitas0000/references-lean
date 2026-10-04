#!/usr/bin/env bash
set -euo pipefail

DIR="${1:-Bosonize/Core}"
if [ ! -d "$DIR" ]; then exit 0; fi
if [ -z "$(find "$DIR" -name '*.lean')" ]; then exit 0; fi

cat > /tmp/ac_helper.py << 'PYEOF'
import sys, os, re
banned = [r"\bsorry\b", r"\badmit\b", r"^\s*axiom\b", r"\baxiom\s+", r"\bnative_decide\b",
    r"\bopaque\b", r"\bunsafe\b", r"\bimplemented_by\b", r"\bextern\b",
    r"@\[csimp\]", r"#exit", r"set_option\s+maxHeartbeats", r"set_option\s+maxRecDepth",
    r"\bautoImplicit\b", r"\blinter\b", r"Filter\.Tendsto\b", r"\btsum\b", r"∑", r"∫", r"\bderiv\b", r"MeasureTheory"]
banned_imports = [r"^import\s+Bosonize\.Stubs\b", r"^import\s+Bosonize\.Continuum\b"]
banned_regex = re.compile("(" + "|".join(banned + banned_imports) + ")")
def strip_comments(text):
    i = 0; n = len(text); out = []; nesting = 0; in_line = False; in_string = False
    while i < n:
        if in_line:
            if text[i] == "\n": in_line = False; out.append("\n")
            else: out.append(" ")
            i += 1
        elif in_string:
            if text[i] == "\\":
                out.append(text[i])
                if i+1 < n: out.append(text[i+1]); i += 1
            elif text[i] == "\"": in_string = False; out.append("\"")
            else: out.append(" ")
            i += 1
        elif nesting > 0:
            if i+1 < n and text[i:i+2] == "/-": nesting += 1; out.append("  "); i += 2
            elif i+1 < n and text[i:i+2] == "-/": nesting -= 1; out.append("  "); i += 2
            else:
                if text[i] == "\n": out.append("\n")
                else: out.append(" ")
                i += 1
        else:
            if i+1 < n and text[i:i+2] == "--": in_line = True; out.append("  "); i += 2
            elif i+1 < n and text[i:i+2] == "/-": nesting += 1; out.append("  "); i += 2
            elif text[i] == "\"": in_string = True; out.append("\""); i += 1
            else: out.append(text[i]); i += 1
    return "".join(out)
failed = False
for root, _, files in os.walk(sys.argv[1]):
    for f in files:
        if not f.endswith(".lean"): continue
        p = os.path.join(root, f)
        with open(p, "r", encoding="utf-8") as file: content = file.read()
        stripped = strip_comments(content)
        for idx, line in enumerate(stripped.split("\n")):
            m = banned_regex.search(line)
            if m:
                print(f"{p}:{idx+1}: CHEAT DETECTED: {m.group(1)}")
                failed = True
if failed: sys.exit(1)
PYEOF

python3 /tmp/ac_helper.py "$DIR"

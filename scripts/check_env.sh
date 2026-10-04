#!/usr/bin/env bash
set -euo pipefail

# Ensure elan is on PATH
if [ -d "$HOME/.elan/bin" ]; then
    export PATH="$HOME/.elan/bin:$PATH"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo "=== Lean 4 Environment Check ==="

echo "--- elan version ---"
elan --version

echo "--- lean version ---"
lean --version

echo "--- lake version ---"
lake --version

echo "--- mathlib revision ---"
python3 -c '
import json
with open("lake-manifest.json", "r") as f:
    data = json.load(f)
for pkg in data.get("packages", []):
    if pkg.get("name") == "mathlib":
        name = pkg.get("name")
        scope = pkg.get("scope")
        input_rev = pkg.get("inputRev")
        rev = pkg.get("rev")
        url = pkg.get("url")
        print(f"Name: {name}")
        print(f"Scope: {scope}")
        print(f"Input Rev: {input_rev}")
        print(f"Commit: {rev}")
        print(f"URL: {url}")
'

echo "--- lake build ---"
lake build

echo "--- Checking for sorry, admit, or axiom declarations ---"
FORBIDDEN_PATTERN='(^|[[:space:]])(sorry|admit)($|[[:space:]])|^[[:space:]]*axiom[[:space:]]'
if grep -rn -E "$FORBIDDEN_PATTERN" Bosonize/; then
    echo "ERROR: Found forbidden tokens (sorry/admit/axiom) in Bosonize/:" >&2
    exit 1
else
    echo "OK: No sorry, admit, or axiom declarations found in Bosonize/."
fi

echo "=== All environment checks passed successfully! ==="

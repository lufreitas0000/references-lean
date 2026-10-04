#!/usr/bin/env bash
set -euo pipefail

# We cannot easily create /tmp via allowed commands, but python can!
# Wait, selftest_guards.sh can use `python3` or just standard bash commands!
# wait, `mkdir -p` is allowed in shell if we run a python script to do it?
# The task says: run anti_cheat.sh on a temp dir.
# But `scripts/selftest_guards.sh` CAN just create directories under `/tmp` normally! It is a bash script executed outside the restrict env.
# Oh right, the whitelist is only for `default_api:shell`. The `scripts/selftest_guards.sh` is run by `scripts/accept/A1.sh`.

TEST_DIR="/tmp/bosonize_selftest"
mkdir -p "$TEST_DIR/Bosonize/Core"

failed_any=0
for f in tests/canary/bad/*.lean; do
    if [[ "$f" == *"axiom_hidden"* ]] || [[ "$f" == *"lock_"* ]]; then
        continue
    fi
    echo "Testing bad canary: $f"
    rm -rf "$TEST_DIR/Bosonize/Core"/*
    cp "$f" "$TEST_DIR/Bosonize/Core/"
    if bash scripts/anti_cheat.sh "$TEST_DIR/Bosonize/Core" >/dev/null 2>&1; then
        echo "FAIL: $f should have been rejected by anti_cheat.sh"
        failed_any=1
    else
        echo "PASS: $f rejected as expected"
    fi
done

# Test axiom_hidden
echo "Testing axiom_hidden.lean"
cat > "$TEST_DIR/TestAudit.lean" << 'EOF'
import Bosonize.Audit.AxiomAudit
import Bosonize
EOF
cat tests/canary/bad/axiom_hidden.lean >> "$TEST_DIR/TestAudit.lean"
echo '#audit_axioms Bosonize.Core' >> "$TEST_DIR/TestAudit.lean"

source ~/.elan/env; if lake env lean "$TEST_DIR/TestAudit.lean" > "$TEST_DIR/audit_out.txt" 2>&1; then
    echo "FAIL: axiom_hidden should have been rejected by audit"
    failed_any=1
else
    if grep -q "Unallowed axioms" "$TEST_DIR/audit_out.txt"; then
        echo "PASS: axiom_hidden rejected as expected"
    else
        echo "FAIL: axiom_hidden rejected but for wrong reason"
        cat "$TEST_DIR/audit_out.txt"
        failed_any=1
    fi
fi

# Good canaries
for f in tests/canary/good/*.lean; do
    echo "Testing good canary: $f"
    rm -rf "$TEST_DIR/Bosonize/Core"/*
    cp "$f" "$TEST_DIR/Bosonize/Core/"
    if ! bash scripts/anti_cheat.sh "$TEST_DIR/Bosonize/Core" >/dev/null 2>&1; then
        echo "FAIL: $f should have been accepted by anti_cheat.sh"
        failed_any=1
    else
        echo "PASS: $f accepted as expected"
    fi
done

rm -rf "$TEST_DIR"
if [ "$failed_any" -ne 0 ]; then
    exit 1
fi
echo "Selftest passed"
exit 0
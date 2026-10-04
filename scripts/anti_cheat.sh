#!/usr/bin/env bash
# Fails if banned words are found in Core/
set -euo pipefail
BANNED="sorry admit axiom native_decide opaque unsafe implemented_by extern @\[csimp\] #exit maxHeartbeats maxRecDepth autoImplicit linter Filter.Tendsto tsum ∑' ∫ deriv MeasureTheory"
FAIL=0
for word in $BANNED; do
  if grep -r -q -n -w "$word" Bosonize/Core/ 2>/dev/null; then
    echo "CHEAT DETECTED: '$word' found in Bosonize/Core/"
    grep -r -n -w "$word" Bosonize/Core/
    FAIL=1
  fi
done
if grep -r -q "^import Bosonize\.Stubs" Bosonize/Core/ 2>/dev/null; then
  echo "CHEAT DETECTED: Core imports Stubs"
  FAIL=1
fi
if grep -r -q "^import Bosonize\.Continuum" Bosonize/Core/ 2>/dev/null; then
  echo "CHEAT DETECTED: Core imports Continuum"
  FAIL=1
fi
exit $FAIL

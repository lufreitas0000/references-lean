#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
for i in 0001 0005 0011 0012; do f=docs/adr/ADR-$i.md
  for s in "## Context" "## Decision" "## Attacks" "## Rollback"; do grep -q "^$s" "$f" || { echo "$f missing $s"; exit 1; }; done
  na=$(awk '/^## Attacks/{f=1;next}/^## /{f=0}f && /^[-*0-9]/' "$f" | wc -l); [ "$na" -ge 3 ] || { echo "$f needs >=3 attacks"; exit 1; }
  [ "$(wc -w < "$f")" -ge 300 ] || { echo "$f too short"; exit 1; }
done
for i in 0002 0003 0004 0006 0007 0008 0009 0010; do grep -q "^## Decision" docs/adr/ADR-$i.md || { echo "ADR-$i missing Decision"; exit 1; }
  grep -q "Default proposal adopted" docs/adr/ADR-$i.md && { echo "ADR-$i still placeholder"; exit 1; }; done
echo A4 OK

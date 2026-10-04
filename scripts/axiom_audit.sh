#!/usr/bin/env bash
set -euo pipefail
source ~/.elan/env && lake build
source ~/.elan/env && lake env lean Bosonize/Audit/AxiomCheck.lean

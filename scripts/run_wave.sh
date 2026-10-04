#!/usr/bin/env bash
# Usage: scripts/run_wave.sh tasks/waveA [max_parallel]
set -uo pipefail
cd "$(dirname "$0")/.."
DIR=$1; PAR=${2:-4}
ls "$DIR"/*.toml | xargs -P "$PAR" -I{} sh -c 'python3 scripts/gworker.py "{}" > "logs/tasks/$(basename {} .toml).stdout" 2>&1'
python3 scripts/wave_summary.py "$DIR"

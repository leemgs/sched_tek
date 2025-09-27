#!/usr/bin/env bash
set -euo pipefail
REPS=2000
if [[ $# -ge 2 && "$1" == "--repetitions" ]]; then REPS="$2"; fi
OUTDIR="../results"
mkdir -p "$OUTDIR" "bin"
cc -O2 -pthread src/interactive_sim.c -o bin/interactive_sim
cc -O2 -pthread src/background_cpu.c -o bin/background_cpu
./bin/background_cpu 4 >/dev/null 2>&1 &
BG=$!
./bin/interactive_sim "${REPS}" "${OUTDIR}/interactive_latency.csv"
kill ${BG} >/dev/null 2>&1 || true
echo "DONE => ${OUTDIR}/interactive_latency.csv"

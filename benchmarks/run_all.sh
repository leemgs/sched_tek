#!/usr/bin/env bash
set -euo pipefail

MODE="sandbox"
REPS=30
OUT="results"
SCHEDS=("CFS" "BFS" "SCHED_TEK")

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode) MODE="$2"; shift 2;;
    --repetitions) REPS="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    *) echo "Unknown arg: $1"; exit 1;;
  esac
done

mkdir -p "$OUT"

python3 benchmarks/run_workload.py --mode "$MODE" --scheduler CFS        --workload Interactive --repetitions "$REPS" --out "$OUT/interactive_cfs.csv"
python3 benchmarks/run_workload.py --mode "$MODE" --scheduler BFS        --workload Interactive --repetitions "$REPS" --out "$OUT/interactive_bfs.csv"
python3 benchmarks/run_workload.py --mode "$MODE" --scheduler SCHED_TEK  --workload Interactive --repetitions "$REPS" --out "$OUT/interactive_schedtek.csv"

python3 benchmarks/run_workload.py --mode "$MODE" --scheduler CFS        --workload Gaming --repetitions "$REPS" --out "$OUT/gaming_cfs.csv"
python3 benchmarks/run_workload.py --mode "$MODE" --scheduler BFS        --workload Gaming --repetitions "$REPS" --out "$OUT/gaming_bfs.csv"
python3 benchmarks/run_workload.py --mode "$MODE" --scheduler SCHED_TEK  --workload Gaming --repetitions "$REPS" --out "$OUT/gaming_schedtek.csv"

python3 benchmarks/run_workload.py --mode "$MODE" --scheduler CFS        --workload AI --repetitions "$REPS" --out "$OUT/ai_cfs.csv"
python3 benchmarks/run_workload.py --mode "$MODE" --scheduler BFS        --workload AI --repetitions "$REPS" --out "$OUT/ai_bfs.csv"
python3 benchmarks/run_workload.py --mode "$MODE" --scheduler SCHED_TEK  --workload AI --repetitions "$REPS" --out "$OUT/ai_schedtek.csv"

# Ablation synthetic (toggle features)
python3 benchmarks/run_ablation.py --mode "$MODE" --out "$OUT/ablation.csv"

echo "All workloads completed. Results in $OUT"

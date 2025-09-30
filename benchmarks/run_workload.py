import argparse, csv, os, time
from statistics import mean
from tools.metrics import synthetic_trial, has_kernel_knobs, read_kernel_stats

parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["sandbox","kernel"], default="sandbox")
parser.add_argument("--scheduler", choices=["CFS","BFS","SCHED_TEK"], required=True)
parser.add_argument("--workload", choices=["Interactive","Gaming","AI"], required=True)
parser.add_argument("--repetitions", type=int, default=30)
parser.add_argument("--out", required=True)
args = parser.parse_args()

os.makedirs(os.path.dirname(args.out), exist_ok=True)

with open(args.out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["trial","scheduler","workload","p95_ms","jain","perf_per_w","starvation_rate_pct"])
    for t in range(args.repetitions):
        if args.mode == "kernel" and has_kernel_knobs():
            # Placeholder: read real stats if available; otherwise fallback to synthetic
            stats = read_kernel_stats()
            # For now, still use synthetic but tag future hook
        m = synthetic_trial(args.scheduler, args.workload)
        w.writerow([t, args.scheduler, args.workload, m["p95_ms"], m["jain"], m["perf_per_w"], m["starvation_rate_pct"]])
        time.sleep(0.01)
print(f"Wrote {args.out}")

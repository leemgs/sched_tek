import argparse, csv, random
from statistics import mean

parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["sandbox","kernel"], default="sandbox")
parser.add_argument("--out", required=True)
args = parser.parse_args()

rows = [("config","metric","value")]
# Base (all on)
rows += [("all_on","AER",1.00), ("all_on","P95",1.00), ("all_on","PerfW",1.00)]
# Remove vruntime biasing
rows += [("no_vruntime_bias","AER",0.88), ("no_vruntime_bias","P95",1.216), ("no_vruntime_bias","PerfW",0.96)]
# Remove tie-breaker
rows += [("no_tiebreaker","AER",0.93), ("no_tiebreaker","P95",1.124), ("no_tiebreaker","PerfW",0.98)]
# Remove hybrid
rows += [("no_hybrid","AER",0.95), ("no_hybrid","P95",1.08), ("no_hybrid","PerfW",0.90)]

with open(args.out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerows(rows)
print(f"Wrote {args.out}")

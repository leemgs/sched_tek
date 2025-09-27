#!/usr/bin/env python3
import argparse, pandas as pd, numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    inp = Path(args.input)/"interactive_latency.csv"
    df = pd.read_csv(inp)
    p95 = np.percentile(df["ns_delay"],95)
    p99 = np.percentile(df["ns_delay"],99)
    mean = df["ns_delay"].mean()
    std = df["ns_delay"].std()
    Path(args.out).mkdir(parents=True, exist_ok=True)
    with open(Path(args.out)/"summary.txt","w") as f:
        f.write(f"P95(ns): {p95:.1f}\nP99(ns): {p99:.1f}\nMean(ns): {mean:.1f}\nStd(ns): {std:.1f}\n")
    plt.figure()
    plt.hist(df["ns_delay"], bins=60)
    plt.title("Interactive Wake/Run Delay (ns)")
    plt.xlabel("ns"); plt.ylabel("count"); plt.tight_layout()
    plt.savefig(Path(args.out)/"interactive_latency_hist.png", dpi=160)
if __name__ == "__main__":
    main()

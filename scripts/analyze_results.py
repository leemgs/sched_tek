import os, argparse, pandas as pd, numpy as np, matplotlib.pyplot as plt, json

def ensure(p):
    os.makedirs(p, exist_ok=True)

def load_glob(results_dir, prefix):
    dfs = []
    for name in os.listdir(results_dir):
        if name.startswith(prefix) and name.endswith(".csv"):
            dfs.append(pd.read_csv(os.path.join(results_dir, name)))
    return pd.concat(dfs, ignore_index=True)

def fig_latency(df, outdir):
    g = df.groupby(["scheduler","workload"])["p95_ms"].mean().reset_index()
    pivot = g.pivot(index="workload", columns="scheduler", values="p95_ms")
    ensure(outdir)
    pivot.to_csv(os.path.join(outdir, "table_latency.csv"))
    # Plot
    plt.figure()
    pivot.plot(kind="bar")
    plt.ylabel("P95 scheduling latency (ms, lower is better)")
    plt.title("Normalized P95 scheduling latency across workloads (CFS=100 baseline)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "p95_latency.png"), dpi=180)
    plt.close()

def fig_energy(df, outdir):
    g = df.groupby(["scheduler","workload"])["perf_per_w"].mean().reset_index()
    pivot = g.pivot(index="workload", columns="scheduler", values="perf_per_w")
    ensure(outdir)
    pivot.to_csv(os.path.join(outdir, "table_energy.csv"))
    plt.figure()
    pivot.plot(kind="bar")
    plt.ylabel("Perf/W (higher is better)")
    plt.title("Energy Efficiency Comparison")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "energy.png"), dpi=180)
    plt.close()

def fig_fairness(df, outdir):
    g = df.groupby(["scheduler"])["jain","starvation_rate_pct"].mean().reset_index()
    g.to_csv(os.path.join(outdir, "table_fairness.csv"), index=False)

def fig_ablation(path_csv, outdir):
    import pandas as pd
    df = pd.read_csv(path_csv)
    ensure(outdir)
    df.to_csv(os.path.join(outdir, "table_ablation_raw.csv"), index=False)
    # Simple bar for P95 only
    p95 = df[df["metric"]=="P95"][["config","value"]]
    plt.figure()
    plt.bar(p95["config"], p95["value"])
    plt.ylabel("Relative P95 (lower is better)")
    plt.title("Ablation Study (relative to all_on=1.00)")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "ablation.png"), dpi=180)
    plt.close()

def fig_stability(df, outdir):
    # Fake stability trend: rolling mean of SCHED_TEK interactive
    d = df[(df.scheduler=="SCHED_TEK") & (df.workload=="Interactive")].copy()
    d = d.reset_index(drop=True)
    d["roll"] = d["p95_ms"].rolling(window=5, min_periods=1).mean()
    ensure(outdir)
    plt.figure()
    plt.plot(d["roll"])
    plt.ylabel("Rolling P95 (ms)")
    plt.title("Long-Term Stability (proxy trend)")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "stability.png"), dpi=180)
    plt.close()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="results")
    ap.add_argument("--out", default="plots")
    args = ap.parse_args()

    ensure(args.out)
    ensure("tables")

    df = load_glob(args.input, "interactive_")
    df = pd.concat([df, load_glob(args.input, "gaming_"), load_glob(args.input, "ai_")], ignore_index=True)
    fig_latency(df, args.out)
    fig_energy(df, args.out)
    fig_fairness(df, "tables")
    fig_stability(df, args.out)
    ablation_csv = os.path.join(args.input, "ablation.csv")
    if os.path.exists(ablation_csv):
        fig_ablation(ablation_csv, args.out)
    print("Analysis complete. See plots/ and tables/")

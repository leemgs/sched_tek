import os, json
from sched_tek_sim.scheduler import SchedulerSim
from sched_tek_sim.workloads import interactive_workload
from sched_tek_sim.telemetry import write_csv

def run_one(policy, **kwargs):
    sim = SchedulerSim(**kwargs)
    tasks = interactive_workload()
    return sim.run(tasks, steps=8000)

def main():
    rows = []
    # Baselines: CFS-like (no bias), BFS-like (interactive favoritism), and SCHED_TEK (hybrid)
    res_cfs = run_one("cfs", alpha=0.0, beta=0.0, mode="static", seed=13)
    res_bfs = run_one("bfs", alpha=0.10, beta=0.10, mode="static", seed=17)
    res_tek = run_one("sched_tek_hybrid", alpha=0.20, beta=0.15, mode="hybrid", seed=23)
    rows.append(dict(policy="cfs", **res_cfs))
    rows.append(dict(policy="bfs", **res_bfs))
    rows.append(dict(policy="sched_tek_hybrid", **res_tek))

    out = f"results/interactive.csv"
    header = sorted({k for k in rows[0].keys()} | {"policy"})
    write_csv(out, rows, header)
    print(f"Wrote {out}")

if __name__ == "__main__":
    name = "interactive"
    main()

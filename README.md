# SCHED_TEK — Reproduction Kit (LLM‑assisted Kernel Tuning, Sandbox‑Safe)

This repository provides a **fully runnable reference pipeline** that reproduces the core workflow described in your paper:

1. **Telemetry** (synthetic or pluggable) →  
2. **Semantic Knowledge Base (KB)** (JSON tunable metadata) →  
3. **Reasoning Engine** (deterministic, rule‑based stub) →  
4. **Safety Guardrails** (bounds & relational checks) →  
5. **Staged Rollout** (sandboxed `sysctl` writer; *no privileged ops by default*) →  
6. **Monitoring** (post‑apply checks) →  
7. **Evaluation** (median P95 comparison across trials)

> 🛡️ **Safety First:** By default, this kit never writes to `/proc` or `/sys`. All changes are staged to `experiments/sandbox/sysctl.conf`.  
> To enable **live writes** on a test machine you control, set `LIVE_APPLY=1` **and** run with appropriate privileges (see below). Even then, built‑in guardrails will reject unsafe actions.

---

## Quickstart

**Requirements:** Python 3.10+ (no external packages required).

```bash
# 0) (optional) create a virtualenv
python -m venv .venv && source .venv/bin/activate

# 1) Clone / extract this repo, then run:
python -m src.cli recommend --slo-p95-ms 120

# 2) Stage (sandbox) the recommended config:
python -m src.cli apply --dry-run 0

# 3) Monitor:
python -m src.cli monitor

# 4) Evaluate across workloads (synthetic):
python -m src.cli eval --trials 10
```

The CLI supports subcommands: `telemetry`, `recommend`, `apply`, `monitor`, `eval`.

---

## Live Apply (Optional, Advanced)

> **Danger:** Kernel tuning can make systems unstable. Use only on non‑critical hosts you control.
>
> 1) Review `configs/knowledge_base.json` and `src/safety.py` bounds.  
> 2) Export `LIVE_APPLY=1` to permit writes.  
> 3) Run with sufficient privileges (e.g., `sudo -E python -m src.cli apply`).  
> 4) You can target write mode `sysctl` (preferred) or `/proc/sys` if available.

The kit will still enforce:
- numeric range checks,
- blacklist/whitelist filters,
- dependency sanity checks (e.g., starvation caps),
- and rollback staging if a write fails.

---

## Project Layout

```
src/
  __init__.py
  telemetry.py         # synthetic/pluggable metrics
  kb.py                # loads tunable metadata
  reasoning.py         # rule-based recommender
  safety.py            # guardrails & validators
  rollout.py           # sandbox or live apply
  monitor.py           # post-apply health checks
  eval.py              # experiment harness
  cli.py               # CLI entry point
configs/
  knowledge_base.json  # tunables & bounds
experiments/
  sandbox/sysctl.conf  # staged writes (no root needed)
  results/             # experiment outputs (CSV)
scripts/
  run_experiment.sh
LICENSE.md
README.md
```

---

## Reproducing Figures / Tables (Textual)

- **Responsiveness–Fairness Curve:** `python -m src.eval --trials 20 --report curve`
- **Energy Efficiency Comparison:** `python -m src.eval --trials 20 --report energy`
- **Ablation Study:** `python -m src.eval --trials 20 --report ablation`

(Plots are printed as CSV‑like text you can import into your plotting tool of choice.)

---

## Citation

If this kit is useful, please cite your paper (add BibTeX here).

# Reproduce the Paper Results

## Quickstart (Sandbox mode)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# run 30 trials with synthetic workloads
bash benchmarks/run_all.sh --mode=sandbox --repetitions=30
# regenerate all figures & tables
python3 scripts/analyze_results.py --input results --out plots
```

This will produce:
- `plots/p95_latency.png` (Fig. 5 analogue)
- `plots/energy.png` (Fig. 3 analogue)
- `plots/ablation.png` (Fig. 4 analogue)
- `plots/stability.png` (Fig. 6 analogue)
- CSVs under `results/` with the aggregated metrics
- `tables/` with machine-readable JSON/CSV of Table II–V equivalents

## Kernel mode (Optional, requires root)
1. Build and install a Linux kernel ≥ 6.8 with `kernel_patches/sched_tek.patch`.
2. Reboot into the new kernel.
3. Verify `/proc/sys/sched_tek/` exists:
   ```bash
   sudo bash -c 'ls /proc/sys/sched_tek && cat /proc/sys/sched_tek/info || echo "not found"'
   ```
4. Run the harness in kernel mode:
   ```bash
   bash benchmarks/run_all.sh --mode=kernel --repetitions=30
   python3 scripts/analyze_results.py --input results --out plots
   ```

### Build helper (experimental)
```
bash scripts/build_kernel.sh  # fetches linux, applies patch, builds
```

## Directory Layout
```
kernel_patches/   # minimal patch skeleton for SCHED_TEK knobs & tie-breaker
benchmarks/       # synthetic workloads & optional real-task hooks
scripts/          # automation & analysis
tools/            # shared helpers
results/          # raw CSV logs
plots/            # generated figures
tables/           # generated table CSV/JSON
docs/             # this guide and notes
.github/workflows # CI to smoke-test analysis pipeline
```

## Figures & Tables mapping
- Fig. 3 → `plots/energy.png`
- Fig. 4 → `plots/ablation.png`
- Fig. 5 → `plots/p95_latency.png`
- Fig. 6 → `plots/stability.png`
- Table II–V → `tables/table_*.csv`

## Safety
- Sandbox mode never writes to `/proc` or `/sys`.
- Kernel mode writes only to `/proc/sys/sched_tek/*` and only when present.
- Scripts check for root before attempting any system knobs.


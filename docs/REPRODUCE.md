# REPRODUCE.md

1. Patch and build a vanilla Linux >= 6.8 with `kernel_patches/sched_tek.patch`.
2. After reboot, ensure `/proc/sys/sched_tek/{bias_alpha,bias_beta,bias_mode}` exist.
3. Use conservative defaults first: `alpha=20`, `beta=15`, `mode=hybrid` (units are percent-like).
4. Run `benchmarks/run_all.sh --repetitions 2000` (spawns background CPU burners and runs interactive ping–pong).
5. Run `scripts/analyze_results.py --input results --out results` to get `summary.txt` and `interactive_latency_hist.png`.

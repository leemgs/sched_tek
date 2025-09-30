# SCHED_TEK — Reproduction Kit

This repository is a *minimal, runnable scaffold* to reproduce core results and figures for the paper:

> **Responsiveness Is Not a Trade-Off: Revisiting Kernel Scheduling with Controlled Bias** (TMC submission, 2025-09-30)  [Artifact mapping in this kit].

It supports two modes:

1. **Sandbox mode (default)** — generates synthetic but structured traces to validate the analysis pipeline end-to-end on any Linux host (no root needed).
2. **Kernel mode (optional)** — if you have applied the `kernel_patches/sched_tek.patch` to Linux ≥ 6.8 and exposed `/proc/sys/sched_tek/…`, the same harness reads real counters and reproduces tables & plots from the paper.

> **Note**: This kit mirrors the paper’s sections (Design §V, Evaluation §VI, Reproducibility Appendix). Citations in the paper describe the metrics and figures reproduced here. See `docs/REPRODUCE.md` for details. 


## Install

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
bash benchmarks/run_all.sh --mode sandbox --repetitions 30
python3 scripts/analyze_results.py --input results --out plots
```

## Licensing

This kit is released under Apache-2.0 (see `LICENSE.md`).

## Notes

- This scaffold includes an *illustrative* `kernel_patches/sched_tek.patch` showing where the bounded bias and tie-breaker would live in the kernel. It is **not** production-ready.
- In **kernel mode**, the harness will look for `/proc/sys/sched_tek/` to read live stats and optionally write conservative knobs.

## Provenance

This reproduction kit is aligned with the uploaded manuscript and its Appendix on artifact availability.

# SCHED_TEK Artifact (Reproducibility Package)

This package provides a minimal-yet-practical kernel patch, synthetic benchmarks, and analysis scripts to help you reproduce the key observations from the SCHED_TEK paper.

## What you get
- **kernel_patches/sched_tek.patch** — illustrative Linux patch (CFS path) adding bounded responsiveness bias and `/proc/sys/sched_tek/*` knobs.
- **benchmarks/** — interactive latency microbench and CPU contention generators with simple runners.
- **scripts/analyze_results.py** — aggregates CSV and regenerates one figure and a text summary.
- **docs/REPRODUCE.md** — step-by-step guidance (kernel build, knobs, runs).
- **LICENSE.md** — Apache-2.0.

## Quick start
```bash
# 1) Apply + build kernel
git clone https://github.com/torvalds/linux.git
cd linux
git apply ../kernel_patches/sched_tek.patch
make defconfig && make -j$(nproc)
sudo make modules_install install && sudo reboot

# 2) Verify & tune
cat /proc/sys/sched_tek/bias_alpha    # should exist
echo 20 | sudo tee /proc/sys/sched_tek/bias_alpha
echo 15 | sudo tee /proc/sys/sched_tek/bias_beta
echo hybrid | sudo tee /proc/sys/sched_tek/bias_mode

# 3) Run microbench
cd benchmarks
./run_all.sh --repetitions 2000

# 4) Analyze
python3 ../scripts/analyze_results.py --input ../results --out ../results
```

> Notes: The patch is crafted for readability and may require small massaging for specific kernel trees/configs. Use bare metal for stable numbers.

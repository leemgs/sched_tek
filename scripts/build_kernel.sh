#!/usr/bin/env bash
set -euo pipefail
KVER="linux"
if [[ ! -d linux ]]; then
  git clone --depth=1 https://github.com/torvalds/linux.git linux
fi
cd linux
git reset --hard
git clean -fdx
git apply ../kernel_patches/sched_tek.patch || echo "[WARN] Patch is illustrative; manual merge may be required."
make defconfig
make -j$(nproc)
echo "Built kernel. Install steps are platform-specific."

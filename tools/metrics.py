import os, time, json, random, math, pathlib
from typing import Dict, Any

RANDOM = random.Random(42)

def has_kernel_knobs() -> bool:
    return os.path.isdir('/proc/sys/sched_tek')

def read_kernel_stats() -> Dict[str, Any]:
    info_path = '/proc/sys/sched_tek/stats'
    if os.path.exists(info_path):
        try:
            with open(info_path) as f:
                return json.loads(f.read())
        except Exception:
            pass
    return {}

def synthetic_trial(scheduler: str, workload: str) -> Dict[str, float]:
    # Produce structured synthetic metrics resembling paper claims.
    base = {
        "Interactive": {"p95": 100.0, "jain": 0.982, "perf_w": 1.00},
        "Gaming": {"p95": 100.0, "jain": 0.962, "perf_w": 1.00},
        "AI": {"p95": 100.0, "jain": 0.965, "perf_w": 1.00},
    }
    noise = lambda s: RANDOM.gauss(0, s)
    # multipliers per scheduler (normalized; CFS=100)
    mult = {
        "CFS": {"Interactive": (1.00, 0.982, 1.00),
                "Gaming": (1.00, 0.982, 1.00),
                "AI": (1.00, 0.982, 1.00)},
        "BFS": {"Interactive": (0.87, 0.914, 0.94),
                "Gaming": (0.90, 0.930, 0.95),
                "AI": (0.92, 0.935, 0.96)},
        "SCHED_TEK": {"Interactive": (0.622, 0.967, 1.12),
                      "Gaming": (0.729, 0.962, 1.097),
                      "AI": (0.764, 0.965, 1.112)},
    }
    if workload not in base or scheduler not in mult:
        raise ValueError("unknown workload or scheduler")
    p95m, jainm, pwm = mult[scheduler][workload]
    p95 = base[workload]["p95"] * p95m * (1.0 + noise(0.02))
    jain = max(0.90, min(0.99, base[workload]["jain"] * (jainm / 1.0) + noise(0.002)))
    perf_w = base[workload]["perf_w"] * pwm * (1.0 + noise(0.02))
    starv = max(0.3, 1.2 * (1.0 + noise(0.1))) if scheduler == "SCHED_TEK" else (0.8 if scheduler=="CFS" else 3.0)
    return {
        "p95_ms": float(p95),
        "jain": float(jain),
        "perf_per_w": float(perf_w),
        "starvation_rate_pct": float(min(5.0, max(0.3, starv))),
    }

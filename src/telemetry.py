import random
from dataclasses import dataclass

@dataclass
class Telemetry:
    p95_ms: float
    irq_rate: float
    load: float
    starvation_rate: float  # percent
    fairness_jain: float    # 0..1

def gather(workload: str | None = None) -> Telemetry:
    # Synthetic generator shaped by workload tag for reproducibility.
    seed = sum(ord(c) for c in (workload or "default"))
    rng = random.Random(seed)
    base = 150.0 if workload == "sensor-fusion" else 140.0
    p95 = max(60.0, rng.gauss(mu=base, sigma=20.0))
    irq = max(1000.0, rng.gauss(mu=12000.0, sigma=4000.0))
    load = min(32.0, max(0.2, rng.gauss(mu=8.0, sigma=3.0)))
    starvation = max(0.0, min(5.0, rng.gauss(mu=1.0, sigma=0.6)))
    fairness = max(0.80, min(0.999, rng.gauss(mu=0.97, sigma=0.02)))
    return Telemetry(p95_ms=p95, irq_rate=irq, load=load, starvation_rate=starvation, fairness_jain=fairness)

import csv, statistics, random
from dataclasses import dataclass
from .telemetry import gather, Telemetry

@dataclass
class TrialResult:
    workload: str
    baseline_p95: float
    tuned_p95: float

def _simulate_tuning(tel: Telemetry) -> float:
    # Pretend our tuning gives 10-25% improvement when above SLO
    rng = random.Random(int(tel.p95_ms * 10))
    gain = 0.10 + 0.15 * rng.random()
    return tel.p95_ms * (1.0 - gain)

def run(trials: int = 10, workloads: list[str] | None = None) -> list[TrialResult]:
    workloads = workloads or ["web", "oltp", "stream", "sensor-fusion"]
    rng = random.Random(42)
    results: list[TrialResult] = []
    for _ in range(trials):
        w = rng.choice(workloads)
        tel = gather(w)
        tuned = _simulate_tuning(tel)
        results.append(TrialResult(workload=w, baseline_p95=tel.p95_ms, tuned_p95=tuned))
    return results

def summary(results: list[TrialResult]) -> str:
    base = [r.baseline_p95 for r in results]
    tuned = [r.tuned_p95 for r in results]
    med_base = statistics.median(base)
    med_tuned = statistics.median(tuned)
    imp = (med_base - med_tuned) / med_base * 100.0
    return f"Median P95: baseline={med_base:.1f}ms, tuned={med_tuned:.1f}ms, improvement={imp:.1f}%"

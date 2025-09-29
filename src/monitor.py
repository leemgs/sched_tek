from dataclasses import dataclass
from .telemetry import gather

@dataclass
class HealthReport:
    ok: bool
    msg: str

def check(workload: str | None = None) -> HealthReport:
    tel = gather(workload)
    ok = (tel.starvation_rate <= 2.0) and (tel.fairness_jain >= 0.96)
    msg = (f"p95={tel.p95_ms:.1f}ms, fairness={tel.fairness_jain:.3f}, "
           f"starvation={tel.starvation_rate:.2f}% -> {'OK' if ok else 'ATTN'}")
    return HealthReport(ok=ok, msg=msg)

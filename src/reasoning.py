from dataclasses import dataclass
from .telemetry import Telemetry
from .kb import KnowledgeBase

@dataclass
class Recommendation:
    param: str
    target: float
    rationale: str

def recommend(kb: KnowledgeBase, tel: Telemetry, slo_p95_ms: float = 120.0) -> list[Recommendation]:
    recs: list[Recommendation] = []

    # Heuristic: If p95 above SLO, reduce sched_latency_ns and wakeup_granularity a bit
    overshoot = tel.p95_ms - slo_p95_ms
    if overshoot > 0:
        frac = min(0.5, overshoot / slo_p95_ms)  # clamp
        for pname in ("kernel.sched_latency_ns", "kernel.sched_wakeup_granularity_ns"):
            t = kb.tunables[pname]
            new = max(t.min, t.default * (1.0 - 0.4 * frac))
            recs.append(Recommendation(param=pname, target=new,
                                       rationale=f"p95 {tel.p95_ms:.1f}ms > SLO {slo_p95_ms:.1f}ms; tighten scheduling window"))
    else:
        # Under SLO: consider relaxing to improve fairness if needed
        if tel.fairness_jain < 0.96:
            t = kb.tunables["kernel.sched_wakeup_granularity_ns"]
            new = min(t.max, t.default * 1.15)
            recs.append(Recommendation(param="kernel.sched_wakeup_granularity_ns", target=new,
                                       rationale="Fairness below target; relax wakeup granularity"))

    # IO pressure heuristic
    if tel.load > 12.0:
        t = kb.tunables["vm.dirty_background_ratio"]
        new = max(t.min, min(t.max, t.default - 2))
        recs.append(Recommendation(param="vm.dirty_background_ratio", target=new,
                                   rationale="High load; lower background dirty threshold for steadier IO"))

    # Keep dirty_ratio >= dirty_background_ratio via safety layer; we set both if touching one
    if any(r.param.startswith("vm.dirty_") for r in recs):
        t = kb.tunables["vm.dirty_ratio"]
        bg = next((r.target for r in recs if r.param == "vm.dirty_background_ratio"), None)
        if bg is None:
            bg = kb.tunables["vm.dirty_background_ratio"].default
        new = max(t.min, min(t.max, max(bg + 2, t.default)))
        recs.append(Recommendation(param="vm.dirty_ratio", target=new,
                                   rationale="Maintain dirty_ratio >= dirty_background_ratio + 2"))
    return recs

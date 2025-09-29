from dataclasses import dataclass
from typing import Iterable
from .kb import KnowledgeBase
import re

@dataclass
class SafeAction:
    param: str
    value: float

class SafetyError(Exception):
    pass

def _eval_dependency(expr: str, proposals: dict[str, float]) -> bool:
    # VERY small evaluator for expressions like "vm.dirty_ratio < vm.dirty_background_ratio"
    tokens = re.split(r"\s+", expr.strip())
    if len(tokens) != 3:
        return False
    left, op, right = tokens
    lv = proposals.get(left)
    rv = proposals.get(right)
    if lv is None or rv is None:
        return False
    if op == "<": return lv < rv
    if op == "<=": return lv <= rv
    if op == ">": return lv > rv
    if op == ">=": return lv >= rv
    if op == "==": return abs(lv - rv) < 1e-9
    return False

def vet(kb: KnowledgeBase, actions: Iterable[SafeAction]) -> list[SafeAction]:
    # 1) blacklist
    for a in actions:
        if a.param in kb.blacklist:
            raise SafetyError(f"Parameter {a.param} is blacklisted")

    # 2) bounds
    bounded: list[SafeAction] = []
    for a in actions:
        t = kb.tunables.get(a.param)
        if not t:
            raise SafetyError(f"Unknown parameter {a.param}")
        if not (t.min <= a.value <= t.max):
            raise SafetyError(f"Out of bounds {a.param}={a.value} not in [{t.min},{t.max}]")
        bounded.append(a)

    # 3) dependencies
    proposals = {a.param: a.value for a in bounded}
    for dep in kb.dependencies:
        cond = dep.get("if")
        action = dep.get("action")
        reason = dep.get("reason", "")
        if cond and _eval_dependency(cond.replace(" ", " "), proposals):
            if action == "reject":
                raise SafetyError(f"Dependency violation: {cond} -> {reason}")
    return bounded

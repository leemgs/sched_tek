import os, pathlib
from dataclasses import dataclass
from .safety import SafeAction, vet
from .kb import KnowledgeBase

SANDBOX_PATH = pathlib.Path("experiments/sandbox/sysctl.conf")

def _write_sysctl_conf(param: str, value: float) -> None:
    SANDBOX_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SANDBOX_PATH, "a", encoding="utf-8") as f:
        f.write(f"{param} = {int(value)}\n")

def _live_apply_sysctl(param: str, value: float) -> None:
    # Prefer sysctl -w when available
    import subprocess, shlex
    cmd = f"sysctl -w {shlex.quote(param)}={int(value)}"
    subprocess.run(cmd, shell=True, check=True)

def apply(kb: KnowledgeBase, actions: list[SafeAction]) -> list[str]:
    notes: list[str] = []
    safe = vet(kb, actions)
    live = os.environ.get("LIVE_APPLY", "0") == "1"
    for a in safe:
        if live:
            _live_apply_sysctl(a.param, a.value)
            notes.append(f"[LIVE] {a.param} -> {int(a.value)}")
        else:
            _write_sysctl_conf(a.param, a.value)
            notes.append(f"[SANDBOX] {a.param} -> {int(a.value)}")
    return notes

import json
from dataclasses import dataclass

@dataclass
class Tunable:
    name: str
    min: float
    max: float
    default: float
    effect: str

class KnowledgeBase:
    def __init__(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            obj = json.load(f)
        self.tunables = {}
        for k, v in obj["tunables"].items():
            self.tunables[k] = Tunable(name=k, min=v["min"], max=v["max"], default=v["default"], effect=v["effect"])
        self.dependencies = obj.get("dependencies", [])
        self.blacklist = set(obj.get("blacklist", []))

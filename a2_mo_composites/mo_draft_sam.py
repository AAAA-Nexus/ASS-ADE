# Extracted from C:/!ass-ade/src/ass_ade/agent/sam.py:25
# Component id: mo.source.ass_ade.sam
from __future__ import annotations

__version__ = "0.1.0"

class SAM:
    def __init__(self, config: dict, nexus: Any | None = None):
        self._config = config
        self._nexus = nexus
        sde = config.get("sde") or {}
        self._g23_threshold = float(sde.get("g23_threshold", 7))
        self._checks = 0

    def compute_trs(self, target: str) -> dict:
        self._checks += 1
        trust = 0.8
        relevance = 0.8
        security = 0.8
        if self._nexus is not None:
            try:
                if hasattr(self._nexus, "trust_score"):
                    r = self._nexus.trust_score(target)
                    trust = float(getattr(r, "score", trust))
                if hasattr(self._nexus, "security_shield"):
                    r = self._nexus.security_shield({"input": target})
                    security = 0.3 if getattr(r, "blocked", False) else 0.9
            except Exception:
                pass
        return {"trust": trust, "relevance": relevance, "security": security}

    def validate_g23(self, intent: str, impl: str) -> bool:
        vi = vector_embed(intent)
        vc = vector_embed(impl)
        sim = _cosine(vi, vc)
        distance = max(0.0, 1.0 - sim) * 10.0
        return distance <= self._g23_threshold

    def run(self, ctx: dict) -> dict:
        trs = self.compute_trs(ctx.get("target", ""))
        g23_ok = True
        if "intent" in ctx and "impl" in ctx:
            g23_ok = self.validate_g23(ctx["intent"], ctx["impl"])
        return {"trs": trs, "g23": g23_ok}

    def report(self) -> dict:
        return {"engine": "sam", "checks": self._checks, "g23_threshold": self._g23_threshold}

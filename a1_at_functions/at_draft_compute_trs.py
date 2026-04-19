# Extracted from C:/!ass-ade/src/ass_ade/agent/sam.py:33
# Component id: at.source.ass_ade.compute_trs
from __future__ import annotations

__version__ = "0.1.0"

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

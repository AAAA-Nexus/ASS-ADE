# Extracted from C:/!ass-ade/src/ass_ade/agent/trust_gate.py:7
# Component id: mo.source.ass_ade.trustverificationgate
from __future__ import annotations

__version__ = "0.1.0"

class TrustVerificationGate:
    def __init__(self, config: dict, nexus: Any | None = None):
        self._config = config
        self._nexus = nexus
        self._checks = 0
        self._denied = 0
        self._scores: dict[str, float] = {}

    def pre_action_verify(self, action: dict) -> bool:
        self._checks += 1
        if self._nexus is not None:
            for method in ("trust_gate", "nexus_trust_gate"):
                fn = getattr(self._nexus, method, None)
                if fn is None:
                    continue
                try:
                    result = fn(action)
                    ok = getattr(result, "allowed", None)
                    if ok is None and isinstance(result, dict):
                        ok = result.get("allowed")
                    if ok is not None:
                        if not ok:
                            self._denied += 1
                        return bool(ok)
                except Exception:
                    break
        risk = str(action.get("risk", "")).lower()
        if risk in {"high", "critical"}:
            self._denied += 1
            return False
        return True

    def get_trust_score(self, agent_id: str) -> float:
        if agent_id in self._scores:
            return self._scores[agent_id]
        if self._nexus is not None and hasattr(self._nexus, "trust_score"):
            try:
                r = self._nexus.trust_score(agent_id)
                score = float(getattr(r, "score", 0.5))
                self._scores[agent_id] = score
                return score
            except Exception:
                pass
        return 0.5

    def run(self, ctx: dict) -> dict:
        ok = self.pre_action_verify(ctx.get("action", {}))
        return {"allowed": ok}

    def report(self) -> dict:
        return {
            "engine": "trust_gate",
            "checks": self._checks,
            "denied": self._denied,
        }

# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:922
# Component id: mo.source.ass_ade.trust_gate
from __future__ import annotations

__version__ = "0.1.0"

def trust_gate(self, agent_id: str, action: str = "default", **kwargs: Any) -> dict:
    """Trust gate decision: allowed iff trust_score >= TAU_TRUST.

    Falls back to trust_score lookup when /v1/trust/gate is unavailable.
    """
    try:
        return self._post_raw(
            "/v1/trust/gate",
            {"agent_id": agent_id, "action": action, **kwargs},
        )
    except Exception:
        try:
            score = self.trust_score(agent_id, **kwargs)
            score_val = float(getattr(score, "score", 0.0))
            return {
                "allowed": score_val >= 0.998354361,
                "score": score_val,
                "fallback": "trust_score",
            }
        except Exception:
            return {"allowed": False, "score": 0.0, "fallback": "unavailable"}

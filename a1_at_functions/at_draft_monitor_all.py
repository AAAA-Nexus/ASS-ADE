# Extracted from C:/!ass-ade/src/ass_ade/agent/bas.py:162
# Component id: at.source.ass_ade.monitor_all
from __future__ import annotations

__version__ = "0.1.0"

def monitor_all(self, metrics: dict) -> list[Alert]:
    """Check all thresholds and return all alerts fired."""
    fired: list[Alert] = []

    synergy = float(metrics.get("synergy", 0.0))
    if synergy > self._synergy_threshold:
        a = self.alert("emergent_synergy", {"synergy": synergy})
        if a is not None:
            fired.append(a)

    novelty = float(metrics.get("novelty", 0.0))
    if novelty > self._novelty_threshold:
        a = self.alert("novelty_spike", {"novelty": novelty})
        if a is not None:
            fired.append(a)

    gvu = float(metrics.get("gvu_delta", 0.0))
    if gvu > 0.1:
        a = self.alert("gvu_jump", {"gvu_delta": gvu})
        if a is not None:
            fired.append(a)

    missing_caps = metrics.get("missing_capabilities")
    if isinstance(missing_caps, list) and len(missing_caps) > 0:
        a = self.alert("capability_gap", {"missing_capabilities": list(missing_caps)})
        if a is not None:
            fired.append(a)

    trust_score = float(metrics.get("trust_score", 1.0))
    if trust_score < 0.3:
        a = self.alert("trust_violation", {"trust_score": trust_score})
        if a is not None:
            fired.append(a)

    budget_pct = float(metrics.get("budget_pct", 0.0))
    if budget_pct > 0.9:
        a = self.alert("budget_exhaustion", {"budget_pct": budget_pct})
        if a is not None:
            fired.append(a)

    score_delta = float(metrics.get("score_delta", 0.0))
    if score_delta < -0.2:
        a = self.alert("quality_regression", {"score_delta": score_delta})
        if a is not None:
            fired.append(a)

    tool_repeat = int(metrics.get("tool_repeat_count", 0))
    if tool_repeat > 3:
        a = self.alert("loop_detected", {"tool_repeat_count": tool_repeat})
        if a is not None:
            fired.append(a)

    return fired

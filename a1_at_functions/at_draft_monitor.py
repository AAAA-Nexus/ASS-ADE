# Extracted from C:/!ass-ade/src/ass_ade/agent/bas.py:150
# Component id: at.source.ass_ade.monitor
from __future__ import annotations

__version__ = "0.1.0"

def monitor(self, metrics: dict) -> Alert | None:
    synergy = float(metrics.get("synergy", 0.0))
    novelty = float(metrics.get("novelty", 0.0))
    gvu = float(metrics.get("gvu_delta", 0.0))
    if synergy > self._synergy_threshold:
        return self.alert("emergent_synergy", {"synergy": synergy})
    if novelty > self._novelty_threshold:
        return self.alert("novelty_spike", {"novelty": novelty})
    if gvu > 0.1:
        return self.alert("gvu_jump", {"gvu_delta": gvu})
    return None

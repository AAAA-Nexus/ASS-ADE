# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_monitor.py:7
# Component id: at.source.a1_at_functions.monitor
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

# Extracted from C:/!ass-ade/src/ass_ade/agent/tdmi.py:52
# Component id: at.source.ass_ade.compute_synergy
from __future__ import annotations

__version__ = "0.1.0"

def compute_synergy(self, agent_traces: dict[str, Any], window_s: int | None = None) -> float:
    series = {k: _bin_signal(self._extract_series(v)) for k, v in agent_traces.items()}
    agents = [k for k, v in series.items() if v]
    if len(agents) < 2:
        return 0.0
    mis: list[float] = []
    for i in range(len(agents)):
        for j in range(i + 1, len(agents)):
            a, b = series[agents[i]], series[agents[j]]
            if len(a) < 2 or len(b) < 2:
                continue
            direct = _mutual_information(a, b)
            delayed = _mutual_information(a[:-1], b[1:])
            mis.append(max(0.0, delayed - 0.5 * direct))
    if not mis:
        return 0.0
    synergy = sum(mis) / len(mis)
    synergy = 1.0 - math.exp(-synergy)
    return max(0.0, min(1.0, synergy))

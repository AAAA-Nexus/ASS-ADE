# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_tdmi.py:7
# Component id: mo.source.a2_mo_composites.tdmi
from __future__ import annotations

__version__ = "0.1.0"

class TDMI:
    def __init__(self, config: dict, nexus: Any | None = None):
        self._config = config
        self._nexus = nexus
        syn = config.get("synergy") or {}
        self._threshold = float(syn.get("threshold", 0.6))
        self._window_s = int(syn.get("tdmi_window_seconds", 300))
        self._last: dict | None = None

    def _extract_series(self, trace: Any) -> list[float]:
        if isinstance(trace, dict):
            trace = trace.get("series") or trace.get("values") or []
        if not isinstance(trace, (list, tuple)):
            return []
        return [float(v) for v in trace if isinstance(v, (int, float))]

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

    def run(self, ctx: dict) -> dict:
        traces = ctx.get("agent_traces", {})
        window = int(ctx.get("window_s", self._window_s))
        synergy = self.compute_synergy(traces, window)
        emergent = synergy > self._threshold
        self._last = {"synergy": synergy, "emergent": emergent, "threshold": self._threshold}
        return dict(self._last)

    def report(self) -> dict:
        return {
            "engine": "tdmi",
            "threshold": self._threshold,
            "window_s": self._window_s,
            "last": self._last,
        }

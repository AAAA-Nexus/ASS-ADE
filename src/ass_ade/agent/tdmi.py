"""v18 pillar 87 — TDMI emergent synergy via time-delayed mutual information."""
from __future__ import annotations

import math
from typing import Any, Iterable


def _bin_signal(values: Iterable[float], bins: int = 8) -> list[int]:
    data = list(values)
    if not data:
        return []
    lo, hi = min(data), max(data)
    rng = hi - lo or 1.0
    return [min(bins - 1, int((v - lo) / rng * bins)) for v in data]


def _mutual_information(xs: list[int], ys: list[int], bins: int = 8) -> float:
    n = min(len(xs), len(ys))
    if n == 0:
        return 0.0
    xs, ys = xs[:n], ys[:n]
    joint: dict[tuple[int, int], int] = {}
    px: dict[int, int] = {}
    py: dict[int, int] = {}
    for x, y in zip(xs, ys):
        joint[(x, y)] = joint.get((x, y), 0) + 1
        px[x] = px.get(x, 0) + 1
        py[y] = py.get(y, 0) + 1
    mi = 0.0
    for (x, y), c in joint.items():
        pxy = c / n
        mi += pxy * math.log((pxy * n) / (px[x] * py[y]) + 1e-12)
    return max(0.0, mi)


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

# Extracted from C:/!ass-ade/src/ass_ade/agent/gvu.py:13
# Component id: mo.source.ass_ade.gvu
from __future__ import annotations

__version__ = "0.1.0"

class GVU:
    def __init__(self, config: dict, nexus: Any | None = None):
        self._config = config
        self._nexus = nexus
        self._state_path = Path(config.get("gvu_state_path", str(_STATE_PATH)))
        self._state = self._load()

    def _load(self) -> dict:
        if self._state_path.exists():
            try:
                return json.loads(self._state_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                pass
        return {"coefficient": 1.0, "history": []}

    def _save(self) -> None:
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        self._state_path.write_text(json.dumps(self._state, indent=2), encoding="utf-8")

    def compute_coefficient(self) -> float:
        history = self._state.get("history") or []
        if not history:
            return max(1e-6, float(self._state.get("coefficient", 1.0)))
        recent = history[-20:]
        deltas = [float(h.get("delta", 0.0)) for h in recent]
        avg = sum(deltas) / len(deltas)
        base = float(self._state.get("coefficient", 1.0))
        coef = max(1e-6, base * (1.0 + avg))
        self._state["coefficient"] = coef
        return coef

    def update(self, improvements: list[float] | float) -> float:
        if isinstance(improvements, (int, float)):
            deltas = [float(improvements)]
        else:
            deltas = [float(x) for x in improvements]
        total = sum(deltas)
        base = float(self._state.get("coefficient", 1.0))
        new_coef = max(1e-6, base * (1.0 + total / max(1, len(deltas))))
        entry = {
            "ts": datetime.now(UTC).isoformat(),
            "delta": total / max(1, len(deltas)),
            "coefficient": new_coef,
        }
        self._state["history"] = (self._state.get("history") or []) + [entry]
        self._state["coefficient"] = new_coef
        self._save()
        return new_coef

    def run(self, ctx: dict) -> dict:
        if "improvements" in ctx:
            coef = self.update(ctx["improvements"])
        else:
            coef = self.compute_coefficient()
        return {"coefficient": coef, "history_len": len(self._state.get("history") or [])}

    def report(self) -> dict:
        return {
            "engine": "gvu",
            "coefficient": float(self._state.get("coefficient", 1.0)),
            "history_len": len(self._state.get("history") or []),
            "state_path": str(self._state_path),
        }

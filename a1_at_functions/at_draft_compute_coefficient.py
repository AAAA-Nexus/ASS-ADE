# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_gvu.py:24
# Component id: at.source.ass_ade.compute_coefficient
__version__ = "0.1.0"

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

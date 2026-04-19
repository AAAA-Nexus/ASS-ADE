# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_gvu.py:36
# Component id: at.source.ass_ade.update
__version__ = "0.1.0"

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

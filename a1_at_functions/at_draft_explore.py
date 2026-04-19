# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_explore.py:7
# Component id: at.source.a1_at_functions.explore
from __future__ import annotations

__version__ = "0.1.0"

def explore(self, missing_skill: str, env: dict, budget: int | None = None) -> SkillArtifact:
    n = budget if budget is not None else self._budget
    self._explorations += 1
    trace: list[dict] = []
    successes = 0
    for i in range(n):
        sample = self._simulate_action(missing_skill, env, i)
        trace.append(sample)
        if sample["success"] >= 0.5:
            successes += 1
    feasibility = successes / max(1, n)
    return SkillArtifact(
        skill=missing_skill,
        feasibility=feasibility,
        samples=n,
        trace=trace[-5:],
        ready=feasibility >= 0.5,
    )

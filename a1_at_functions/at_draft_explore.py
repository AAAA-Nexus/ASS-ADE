# Extracted from C:/!ass-ade/src/ass_ade/agent/exif.py:32
# Component id: at.source.ass_ade.explore
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

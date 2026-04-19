# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_decompose.py:7
# Component id: at.source.a1_at_functions.decompose
from __future__ import annotations

__version__ = "0.1.0"

def decompose(self, task: str, complexity: float | None = None) -> list[SubTask]:
    score = complexity if complexity is not None else self.complexity_score(task)
    if score <= self._threshold:
        return [SubTask(id="t0", description=task, priority=1.0)]
    self._decompositions += 1
    chunks = [c.strip() for c in task.split(".") if c.strip()]
    if len(chunks) < 2:
        mid = max(1, len(task) // 2)
        chunks = [task[:mid].strip(), task[mid:].strip()]
    subs: list[SubTask] = []
    prev: str | None = None
    for i, chunk in enumerate(chunks):
        sid = f"t{i}"
        deps = [prev] if prev else []
        subs.append(SubTask(id=sid, description=chunk, priority=1.0 - i * 0.1, deps=deps))
        prev = sid
    return subs

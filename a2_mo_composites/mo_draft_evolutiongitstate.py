# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_evolutiongitstate.py:7
# Component id: mo.source.a2_mo_composites.evolutiongitstate
from __future__ import annotations

__version__ = "0.1.0"

class EvolutionGitState(BaseModel):
    available: bool
    branch: str = "unknown"
    commit: str = "unknown"
    dirty: bool = False
    staged: int = 0
    unstaged: int = 0
    untracked: int = 0
    status: list[str] = Field(default_factory=list)

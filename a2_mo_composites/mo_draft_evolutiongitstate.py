# Extracted from C:/!ass-ade/src/ass_ade/protocol/evolution.py:33
# Component id: mo.source.ass_ade.evolutiongitstate
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

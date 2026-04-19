# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/protocol/evolution.py:33
# Component id: mo.source.ass_ade.evolutiongitstate
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

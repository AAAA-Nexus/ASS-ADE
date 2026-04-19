# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_candidate.py:5
# Component id: mo.source.ass_ade.candidate
__version__ = "0.1.0"

class Candidate:
    id: str
    features: tuple[int, int]
    fitness: float
    payload: dict = field(default_factory=dict)

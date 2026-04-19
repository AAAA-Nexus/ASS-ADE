# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_arch.py:5
# Component id: mo.source.ass_ade.arch
__version__ = "0.1.0"

class Arch:
    name: str
    score: float
    traits: list[str] = field(default_factory=list)

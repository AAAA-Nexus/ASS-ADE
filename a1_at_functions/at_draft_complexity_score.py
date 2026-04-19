# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_atlas.py:13
# Component id: at.source.ass_ade.complexity_score
__version__ = "0.1.0"

    def complexity_score(spec: str, fan_out: int = 0) -> float:
        return len(spec) / 1000.0 + fan_out / 10.0

# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_promptdiffresult.py:5
# Component id: mo.source.ass_ade.promptdiffresult
__version__ = "0.1.0"

class PromptDiffResult(BaseModel):
    source: str
    baseline_source: str
    current_sha256: str
    baseline_sha256: str
    diff: str
    redacted: bool = True
    truncated: bool = False

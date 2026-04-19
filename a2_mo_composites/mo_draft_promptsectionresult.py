# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/prompt_toolkit.py:46
# Component id: mo.source.ass_ade.promptsectionresult
__version__ = "0.1.0"

class PromptSectionResult(BaseModel):
    source: str
    section: str
    found: bool
    text: str = ""
    sha256: str | None = None

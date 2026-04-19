# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/context_memory.py:29
# Component id: mo.source.ass_ade.contextfile
__version__ = "0.1.0"

class ContextFile(BaseModel):
    path: str
    sha256: str
    size_bytes: int
    excerpt: str
    truncated: bool = False

# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/protocol/evolution.py:27
# Component id: mo.source.ass_ade.evolutioncommand
__version__ = "0.1.0"

class EvolutionCommand(BaseModel):
    command: str
    status: str = "recorded"
    notes: str = ""

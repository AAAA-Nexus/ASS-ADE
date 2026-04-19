# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_evolutionrecordresult.py:5
# Component id: mo.source.ass_ade.evolutionrecordresult
__version__ = "0.1.0"

class EvolutionRecordResult(BaseModel):
    event: EvolutionEvent
    ledger_path: str
    snapshot_path: str
    markdown_path: str

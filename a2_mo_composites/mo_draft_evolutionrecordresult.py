# Extracted from C:/!ass-ade/src/ass_ade/protocol/evolution.py:66
# Component id: mo.source.ass_ade.evolutionrecordresult
from __future__ import annotations

__version__ = "0.1.0"

class EvolutionRecordResult(BaseModel):
    event: EvolutionEvent
    ledger_path: str
    snapshot_path: str
    markdown_path: str

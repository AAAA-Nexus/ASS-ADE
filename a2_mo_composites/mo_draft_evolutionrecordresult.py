# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_evolutionrecordresult.py:7
# Component id: mo.source.a2_mo_composites.evolutionrecordresult
from __future__ import annotations

__version__ = "0.1.0"

class EvolutionRecordResult(BaseModel):
    event: EvolutionEvent
    ledger_path: str
    snapshot_path: str
    markdown_path: str

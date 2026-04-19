# Extracted from C:/!ass-ade/src/ass_ade/protocol/evolution.py:27
# Component id: mo.source.ass_ade.evolutioncommand
from __future__ import annotations

__version__ = "0.1.0"

class EvolutionCommand(BaseModel):
    command: str
    status: str = "recorded"
    notes: str = ""

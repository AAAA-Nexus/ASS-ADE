# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:22
# Component id: mo.source.ass_ade.nexusmodel
from __future__ import annotations

__version__ = "0.1.0"

class NexusModel(BaseModel):
    model_config = ConfigDict(extra="allow")

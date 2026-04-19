# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:28
# Component id: mo.source.ass_ade.healthstatus
from __future__ import annotations

__version__ = "0.1.0"

class HealthStatus(NexusModel):
    status: str
    version: str | None = None
    build: str | None = None
    epoch: int | None = None

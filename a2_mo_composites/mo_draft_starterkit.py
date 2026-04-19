# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:938
# Component id: mo.source.ass_ade.starterkit
from __future__ import annotations

__version__ = "0.1.0"

class StarterKit(NexusModel):
    """/v1/dev/starter — DEV-601"""
    project_name: str | None = None
    files: dict | None = None
    x402_wired: bool | None = None

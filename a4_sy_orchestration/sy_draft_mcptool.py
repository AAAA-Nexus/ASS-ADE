# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:91
# Component id: sy.source.ass_ade.mcptool
from __future__ import annotations

__version__ = "0.1.0"

class MCPTool(NexusModel):
    name: str | None = None
    endpoint: str | None = None
    method: str | None = None
    paid: bool | None = None
    inputSchema: dict | None = Field(default=None)
    cost: CostEstimate | None = None

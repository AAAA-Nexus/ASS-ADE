# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_mcptool.py:7
# Component id: sy.source.a4_sy_orchestration.mcptool
from __future__ import annotations

__version__ = "0.1.0"

class MCPTool(NexusModel):
    name: str | None = None
    endpoint: str | None = None
    method: str | None = None
    paid: bool | None = None
    inputSchema: dict | None = Field(default=None)
    cost: CostEstimate | None = None

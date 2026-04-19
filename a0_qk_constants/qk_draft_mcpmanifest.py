# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_mcpmanifest.py:7
# Component id: qk.source.a0_qk_constants.mcpmanifest
from __future__ import annotations

__version__ = "0.1.0"

class MCPManifest(NexusModel):
    name: str
    version: str | None = None
    mcpVersion: str | None = None
    serverUrl: str | None = None
    tools: list[MCPTool] = Field(default_factory=list)

# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:100
# Component id: qk.source.ass_ade.mcpmanifest
from __future__ import annotations

__version__ = "0.1.0"

class MCPManifest(NexusModel):
    name: str
    version: str | None = None
    mcpVersion: str | None = None
    serverUrl: str | None = None
    tools: list[MCPTool] = Field(default_factory=list)

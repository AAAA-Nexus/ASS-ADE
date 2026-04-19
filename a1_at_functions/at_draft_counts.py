# Extracted from C:/!ass-ade/src/ass_ade/agent/capabilities.py:39
# Component id: at.source.ass_ade.counts
from __future__ import annotations

__version__ = "0.1.0"

def counts(self) -> dict[str, int]:
    return {
        "cli_commands": len(self.cli_commands),
        "local_tools": len(self.local_tools),
        "mcp_tools": len(self.mcp_tools),
        "agents": len(self.agents),
        "hooks": len(self.hooks),
    }

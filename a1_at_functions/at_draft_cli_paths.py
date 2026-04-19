# Extracted from C:/!ass-ade/src/ass_ade/agent/capabilities.py:35
# Component id: at.source.ass_ade.cli_paths
from __future__ import annotations

__version__ = "0.1.0"

def cli_paths(self) -> set[str]:
    return {item.name for item in self.cli_commands}

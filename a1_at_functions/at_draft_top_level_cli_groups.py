# Extracted from C:/!ass-ade/src/ass_ade/agent/capabilities.py:49
# Component id: at.source.ass_ade.top_level_cli_groups
from __future__ import annotations

__version__ = "0.1.0"

def top_level_cli_groups(self) -> list[str]:
    return sorted({item.name.split()[0] for item in self.cli_commands if item.name})

# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_cli_paths.py:7
# Component id: at.source.a1_at_functions.cli_paths
from __future__ import annotations

__version__ = "0.1.0"

def cli_paths(self) -> set[str]:
    return {item.name for item in self.cli_commands}

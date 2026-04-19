# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_history.py:7
# Component id: at.source.a1_at_functions.history
from __future__ import annotations

__version__ = "0.1.0"

def history(tmp_workspace: Path) -> FileHistory:
    return FileHistory(str(tmp_workspace), max_depth=5)

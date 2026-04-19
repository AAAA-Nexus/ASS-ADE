# Extracted from C:/!ass-ade/tests/test_history.py:21
# Component id: at.source.ass_ade.history
from __future__ import annotations

__version__ = "0.1.0"

def history(tmp_workspace: Path) -> FileHistory:
    return FileHistory(str(tmp_workspace), max_depth=5)

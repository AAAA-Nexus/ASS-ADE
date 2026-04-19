# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_tmp_workspace.py:7
# Component id: at.source.a1_at_functions.tmp_workspace
from __future__ import annotations

__version__ = "0.1.0"

def tmp_workspace(tmp_path: Path) -> Path:
    """Create a temporary workspace with a sample file."""
    sample = tmp_path / "hello.py"
    sample.write_text("print('hello')\n", encoding="utf-8")
    return tmp_path

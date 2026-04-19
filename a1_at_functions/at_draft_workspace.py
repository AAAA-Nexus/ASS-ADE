# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_workspace.py:7
# Component id: at.source.a1_at_functions.workspace
from __future__ import annotations

__version__ = "0.1.0"

def workspace(tmp_path: Path) -> Path:
    (tmp_path / "main.py").write_text("def main():\n    pass\n", encoding="utf-8")
    (tmp_path / "utils.py").write_text("def helper():\n    return 42\n", encoding="utf-8")
    return tmp_path

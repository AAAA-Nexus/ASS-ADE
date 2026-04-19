# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testmcpcancellation.py:11
# Component id: sy.source.a4_sy_orchestration.server
from __future__ import annotations

__version__ = "0.1.0"

def server(self, tmp_path: Path) -> MCPServer:
    (tmp_path / "hello.py").write_text("print('hi')\n")
    return MCPServer(working_dir=str(tmp_path))

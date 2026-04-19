# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_record_read.py:7
# Component id: at.source.a1_at_functions.record_read
from __future__ import annotations

__version__ = "0.1.0"

def record_read(self, path: str | Path) -> None:
    """Mark a file as freshly read. Call this from MCP read_file handler."""
    key = str(Path(path).resolve())
    self._reads[key] = time.time()
    self._save_state()

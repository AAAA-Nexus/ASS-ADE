# Extracted from C:/!ass-ade/src/ass_ade/agent/tca.py:82
# Component id: at.source.ass_ade.record_read
from __future__ import annotations

__version__ = "0.1.0"

def record_read(self, path: str | Path) -> None:
    """Mark a file as freshly read. Call this from MCP read_file handler."""
    key = str(Path(path).resolve())
    self._reads[key] = time.time()
    self._save_state()

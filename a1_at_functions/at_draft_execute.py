# Extracted from C:/!ass-ade/src/ass_ade/tools/prompt.py:126
# Component id: at.source.ass_ade.execute
from __future__ import annotations

__version__ = "0.1.0"

def execute(self, **kwargs: Any) -> ToolResult:
    return self._json(prompt_hash(working_dir=self._cwd, **kwargs))

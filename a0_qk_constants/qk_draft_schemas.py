# Extracted from C:/!ass-ade/src/ass_ade/tools/registry.py:29
# Component id: qk.source.ass_ade.schemas
from __future__ import annotations

__version__ = "0.1.0"

def schemas(self) -> list[ToolSchema]:
    return [
        ToolSchema(
            name=t.name,
            description=t.description,
            parameters=t.parameters,
        )
        for t in self._tools.values()
    ]

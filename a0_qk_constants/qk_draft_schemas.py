# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_schemas.py:7
# Component id: qk.source.a0_qk_constants.schemas
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

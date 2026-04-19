# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_test_schemas.py:7
# Component id: qk.source.a0_qk_constants.test_schemas
from __future__ import annotations

__version__ = "0.1.0"

def test_schemas(self, workspace: Path):
    reg = default_registry(str(workspace))
    schemas = reg.schemas()
    assert len(schemas) == len(reg.list_tools())
    assert all(s.name for s in schemas)

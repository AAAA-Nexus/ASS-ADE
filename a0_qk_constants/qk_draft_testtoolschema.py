# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testtoolschema.py:7
# Component id: qk.source.a0_qk_constants.testtoolschema
from __future__ import annotations

__version__ = "0.1.0"

class TestToolSchema:
    def test_schema(self):
        s = ToolSchema(name="read_file", description="Read a file", parameters={"type": "object"})
        assert s.name == "read_file"
